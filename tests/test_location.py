"""
Location Screen Tests.
"""
import pytest
from tests.base_test import BaseTest
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage
from pages.location_page import LocationPage


@pytest.mark.regression
class TestLocation(BaseTest):
    """Location permission and selection tests."""

    def _navigate_to_location(self):
        splash = SplashPage(self.driver)
        splash.wait_for_splash_to_finish()
        lang = LanguagePage(self.driver)
        if lang.is_language_screen_displayed():
            lang.select_arabic()
            lang.confirm_selection()
        return LocationPage(self.driver)

    def test_skip_location_proceeds(self):
        """Verify that skipping location goes to next screen."""
        location = self._navigate_to_location()
        if location.is_location_screen_displayed():
            location.skip_location()
            assert not location.is_location_screen_displayed(), "Stuck on location screen after skip"

    def test_allow_location_permission(self):
        """Verify that allowing location proceeds after system dialog."""
        location = self._navigate_to_location()
        if location.is_location_screen_displayed():
            location.allow_location()
            assert not location.is_location_screen_displayed(), "Stuck on location after allowing"

    def test_search_location_manually(self):
        """Verify that manual location search works."""
        location = self._navigate_to_location()
        if location.is_location_screen_displayed():
            if location.is_displayed(location.SEARCH_FIELD, timeout=5):
                location.search_location("القاهرة")
                # Should show results
                assert location.is_displayed(location.LOCATION_LIST, timeout=10)
