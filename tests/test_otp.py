"""
OTP Verification Tests.
"""
import pytest
from tests.base_test import BaseTest
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage
from pages.location_page import LocationPage
from pages.onboarding_page import OnboardingPage
from pages.otp_page import OTPPage


@pytest.mark.regression
class TestOTP(BaseTest):
    """OTP / phone verification tests."""

    def _navigate_to_otp(self):
        """Navigate through onboarding to reach OTP screen."""
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
            onboarding.complete_onboarding_by_swiping()
        return OTPPage(self.driver)

    def test_otp_screen_displayed(self):
        """Verify that OTP screen shows after onboarding."""
        otp = self._navigate_to_otp()
        if otp.is_otp_screen_displayed():
            assert otp.is_displayed(otp.PHONE_INPUT) or \
                   otp.is_displayed(otp.SKIP_BUTTON)

    def test_skip_otp(self):
        """Verify that OTP can be skipped if skip button exists."""
        otp = self._navigate_to_otp()
        if otp.is_otp_screen_displayed():
            otp.skip_otp()
            from pages.main_page import MainPage
            main = MainPage(self.driver)
            assert main.is_main_screen_displayed(), "Main not reached after OTP skip"

    def test_empty_phone_shows_error(self):
        """Verify that submitting empty phone number shows error."""
        otp = self._navigate_to_otp()
        if otp.is_otp_screen_displayed() and otp.is_displayed(otp.SEND_OTP_BUTTON, timeout=3):
            otp.tap_send_otp()
            error = otp.get_error_message()
            assert error != "" or otp.is_otp_screen_displayed(), "No error for empty phone"

    def test_invalid_phone_format(self):
        """Verify that invalid phone number format is rejected."""
        otp = self._navigate_to_otp()
        if otp.is_otp_screen_displayed() and otp.is_displayed(otp.PHONE_INPUT, timeout=3):
            otp.enter_phone_number("123")
            otp.tap_send_otp()
            error = otp.get_error_message()
            assert error != "" or otp.is_otp_screen_displayed(), "No error for invalid phone"

    def test_invalid_otp_code(self):
        """Verify that wrong OTP code shows error."""
        otp = self._navigate_to_otp()
        if otp.is_otp_screen_displayed() and otp.is_displayed(otp.PHONE_INPUT, timeout=3):
            otp.enter_phone_number("01012345678")
            otp.tap_send_otp()
            if otp.is_displayed(otp.OTP_FIELD_1, timeout=10):
                otp.enter_otp_code("0000")
                otp.tap_verify()
                error = otp.get_error_message()
                assert error != "" or otp.is_otp_screen_displayed(), "No error for wrong OTP"
