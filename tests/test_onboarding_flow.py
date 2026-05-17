"""
Onboarding Flow Tests — First launch experience.
Splash → Language → Location → Onboarding → OTP → Main
"""
import pytest
from tests.base_test import BaseTest
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage
from pages.location_page import LocationPage
from pages.onboarding_page import OnboardingPage
from pages.otp_page import OTPPage
from pages.main_page import MainPage


@pytest.mark.smoke
@pytest.mark.critical
class TestOnboardingFlow(BaseTest):
    """E2E: Complete first-launch onboarding flow."""

    def test_complete_onboarding_arabic(self):
        """Verify that first launch completes full onboarding flow in Arabic."""
        splash = SplashPage(self.driver)
        assert splash.is_splash_displayed(), "Splash screen not shown"
        splash.wait_for_splash_to_finish()

        lang = LanguagePage(self.driver)
        if lang.is_language_screen_displayed():
            lang.select_arabic()
            lang.confirm_selection()

        location = LocationPage(self.driver)
        if location.is_location_screen_displayed():
            location.skip_location()

        onboarding = OnboardingPage(self.driver)
        if onboarding.is_onboarding_displayed():
            onboarding.complete_onboarding_by_swiping()

        otp = OTPPage(self.driver)
        if otp.is_otp_screen_displayed():
            otp.skip_otp()

        main = MainPage(self.driver)
        assert main.is_main_screen_displayed(), "Main screen not reached after onboarding"

    def test_complete_onboarding_english(self):
        """Verify that first launch completes full onboarding flow in English."""
        splash = SplashPage(self.driver)
        splash.wait_for_splash_to_finish()

        lang = LanguagePage(self.driver)
        if lang.is_language_screen_displayed():
            lang.select_english()
            lang.confirm_selection()

        location = LocationPage(self.driver)
        if location.is_location_screen_displayed():
            location.skip_location()

        onboarding = OnboardingPage(self.driver)
        if onboarding.is_onboarding_displayed():
            onboarding.complete_onboarding_by_swiping()

        otp = OTPPage(self.driver)
        if otp.is_otp_screen_displayed():
            otp.skip_otp()

        main = MainPage(self.driver)
        assert main.is_main_screen_displayed(), "Main screen not reached after English onboarding"

    def test_onboarding_swipe_shows_all_pages(self):
        """Verify that all onboarding pages can be viewed by swiping."""
        splash = SplashPage(self.driver)
        splash.wait_for_splash_to_finish()

        lang = LanguagePage(self.driver)
        if lang.is_language_screen_displayed():
            lang.select_arabic()
            lang.confirm_selection()

        location = LocationPage(self.driver)
        if location.is_location_screen_displayed():
            location.skip_location()

        onboarding = OnboardingPage(self.driver)
        if onboarding.is_onboarding_displayed():
            pages_seen = []
            for i in range(5):
                title = onboarding.get_page_title()
                if title:
                    pages_seen.append(title)
                if onboarding.is_displayed(onboarding.DONE_BUTTON, timeout=2):
                    break
                onboarding.swipe_to_next()

            assert len(pages_seen) >= 2, f"Expected multiple onboarding pages, saw: {len(pages_seen)}"
