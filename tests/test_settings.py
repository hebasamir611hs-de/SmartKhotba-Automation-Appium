"""
Settings Tests — Language, Font, Notifications, Share, About.
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.settings_page import SettingsPage
from pages.language_page import LanguagePage
from tests.helpers import navigate_to_main


@pytest.mark.regression
@pytest.mark.usefixtures("clear_app_state")
class TestSettings(BaseTest):
    """Settings screen tests — uses clear_app_state for isolation."""

    def _go_to_settings(self):
        main = navigate_to_main(self.driver)
        main.go_to_settings()
        return SettingsPage(self.driver)

    def test_settings_screen_loads(self):
        """Verify that settings screen loads with all options."""
        settings = self._go_to_settings()
        assert settings.is_settings_displayed(), "Settings screen not loaded"

    def test_change_language_to_english(self):
        """Verify that language can be changed to English."""
        settings = self._go_to_settings()
        settings.change_language_to_english()
        # App should restart or refresh in English
        # Verify by checking for English text somewhere

    def test_change_language_to_arabic(self):
        """Verify that language can be changed to Arabic."""
        settings = self._go_to_settings()
        settings.change_language_to_arabic()

    def test_change_font_size_small(self):
        """Verify that font can be changed to small."""
        settings = self._go_to_settings()
        settings.change_font_size("small")

    def test_change_font_size_large(self):
        """Verify that font can be changed to large."""
        settings = self._go_to_settings()
        settings.change_font_size("large")

    def test_change_font_size_medium(self):
        """Verify that font can be changed back to medium."""
        settings = self._go_to_settings()
        settings.change_font_size("medium")

    def test_toggle_notifications(self):
        """Verify that notifications can be toggled."""
        settings = self._go_to_settings()
        settings.toggle_notifications()
        # Toggle back
        settings.toggle_notifications()

    def test_share_app(self):
        """Verify that share app opens share sheet."""
        settings = self._go_to_settings()
        settings.tap_share_app()
        # Android share sheet should appear

    def test_about_shows_version(self):
        """Verify that about screen shows correct app version."""
        settings = self._go_to_settings()
        version = settings.get_app_version()
        assert "1.1.0" in version, f"Expected version 1.1.0, got: {version}"

    def test_change_location_from_settings(self):
        """Verify that location can be changed from settings."""
        settings = self._go_to_settings()
        settings.change_location()
        from pages.location_page import LocationPage
        location = LocationPage(self.driver)
        assert location.is_location_screen_displayed(), "Location screen not opened from settings"

    def test_back_from_settings(self):
        """Verify that back returns to main screen."""
        settings = self._go_to_settings()
        settings.go_back()
        main = MainPage(self.driver)
        assert main.is_main_screen_displayed(), "Did not return to main from settings"
