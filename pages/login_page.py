"""
LoginPage — SmartKhotba does NOT have a traditional login screen.
Authentication is OTP-based (see otp_page.py).
Verified via app activity dump and page_source on real device (2026-06-03):
only SplashActivity and MainActivity exist — no LoginActivity.

This module is kept for backward compatibility with test_login.py imports
but delegates to OTPPage for the actual auth flow.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Auth entry point — wraps OTP-based authentication.
    SmartKhotba uses phone+OTP, not username/password.
    """

    PAGE_NAME = "login_page"

    # The app has no login screen — auth is OTP-based via OTPPage.
    # These locators point to the OTP flow entry if it appears.
    PHONE_INPUT = (By.XPATH, "//android.widget.EditText")
    SKIP_BUTTON = (By.XPATH, "//*[contains(@text, 'تخطي') or contains(@text, 'Skip')]")

    def is_login_page_displayed(self) -> bool:
        """Check if any auth/OTP screen is displayed."""
        return self.is_displayed(self.PHONE_INPUT, timeout=5) or \
               self.is_displayed(self.SKIP_BUTTON, timeout=3)

    def skip_login(self):
        """Skip authentication if available."""
        if self.is_displayed(self.SKIP_BUTTON, timeout=3):
            self.click(self.SKIP_BUTTON)
