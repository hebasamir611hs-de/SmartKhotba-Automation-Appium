"""
Splash Screen Tests.
"""
import pytest
from tests.base_test import BaseTest
from pages.splash_page import SplashPage


@pytest.mark.smoke
class TestSplash(BaseTest):
    """Splash screen behavior."""

    def test_app_launches_to_splash(self):
        """Verify that app launches and shows splash screen."""
        splash = SplashPage(self.driver)
        assert splash.is_splash_displayed(), "Splash screen not shown on app launch"

    def test_splash_auto_transitions(self):
        """Verify that splash screen auto-transitions to next screen."""
        splash = SplashPage(self.driver)
        assert splash.is_splash_displayed()
        splash.wait_for_splash_to_finish(timeout=15)
        # After splash, should see language or main screen
        assert not splash.is_displayed(splash.APP_LOGO, timeout=2), "Splash stuck — did not transition"
