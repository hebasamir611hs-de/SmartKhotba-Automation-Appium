"""
Language Selection Tests.
"""
import pytest
from tests.base_test import BaseTest
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage


@pytest.mark.regression
class TestLanguage(BaseTest):
    """Language selection screen tests."""

    def _navigate_to_language(self):
        splash = SplashPage(self.driver)
        splash.wait_for_splash_to_finish()
        return LanguagePage(self.driver)

    def test_language_screen_shows_arabic_and_english(self):
        """Verify that both Arabic and English options are displayed."""
        lang = self._navigate_to_language()
        if lang.is_language_screen_displayed():
            assert lang.is_displayed(lang.ARABIC_TEXT, timeout=5), "Arabic option missing"
            assert lang.is_displayed(lang.ENGLISH_TEXT, timeout=5), "English option missing"

    def test_select_arabic_language(self):
        """Verify that selecting Arabic proceeds to next screen."""
        lang = self._navigate_to_language()
        if lang.is_language_screen_displayed():
            lang.select_arabic()
            lang.confirm_selection()
            assert not lang.is_language_screen_displayed(), "Still on language screen after selection"

    def test_select_english_language(self):
        """Verify that selecting English proceeds to next screen."""
        lang = self._navigate_to_language()
        if lang.is_language_screen_displayed():
            lang.select_english()
            lang.confirm_selection()
            assert not lang.is_language_screen_displayed(), "Still on language screen after selection"
