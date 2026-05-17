"""
OTPPage — OTP verification screen (VerifyOtpNumber).
Phone number entry + OTP code verification.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OTPPage(BasePage):
    """OTP / phone verification screen."""

    PAGE_NAME = "otp_page"

    # ─── Locators ────────────────────────────────────────────────
    PHONE_INPUT = (By.ID, "com.islam.khutba.qa:id/et_phone")
    COUNTRY_CODE = (By.ID, "com.islam.khutba.qa:id/ccp")
    SEND_OTP_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_send_otp")
    OTP_FIELD_1 = (By.ID, "com.islam.khutba.qa:id/otp_1")
    OTP_FIELD_2 = (By.ID, "com.islam.khutba.qa:id/otp_2")
    OTP_FIELD_3 = (By.ID, "com.islam.khutba.qa:id/otp_3")
    OTP_FIELD_4 = (By.ID, "com.islam.khutba.qa:id/otp_4")
    VERIFY_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_verify")
    RESEND_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_resend")
    TIMER_TEXT = (By.ID, "com.islam.khutba.qa:id/tv_timer")
    ERROR_TEXT = (By.ID, "com.islam.khutba.qa:id/tv_error")
    SKIP_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_skip")

    # ─── Actions ─────────────────────────────────────────────────

    def is_otp_screen_displayed(self) -> bool:
        return self.is_displayed(self.PHONE_INPUT, timeout=10) or \
               self.is_displayed(self.OTP_FIELD_1, timeout=5)

    def enter_phone_number(self, phone: str):
        """Enter phone number."""
        self.type_text(self.PHONE_INPUT, phone)

    def tap_send_otp(self):
        """Send OTP to entered phone number."""
        self.hide_keyboard()
        self.click(self.SEND_OTP_BUTTON)

    def enter_otp_code(self, code: str):
        """Enter 4-digit OTP code across fields."""
        if len(code) != 4:
            raise ValueError(f"OTP must be 4 digits, got: {code}")
        fields = [self.OTP_FIELD_1, self.OTP_FIELD_2, self.OTP_FIELD_3, self.OTP_FIELD_4]
        for i, digit in enumerate(code):
            self.type_text(fields[i], digit, clear_first=True)

    def tap_verify(self):
        """Verify OTP code."""
        self.click(self.VERIFY_BUTTON)

    def tap_resend(self):
        """Resend OTP code."""
        self.click(self.RESEND_BUTTON)

    def is_resend_enabled(self) -> bool:
        """Check if resend button is clickable (timer finished)."""
        return self.is_displayed(self.RESEND_BUTTON, timeout=3)

    def get_error_message(self) -> str:
        if self.is_displayed(self.ERROR_TEXT, timeout=3):
            return self.get_text(self.ERROR_TEXT)
        return ""

    def skip_otp(self):
        """Skip OTP if available."""
        if self.is_displayed(self.SKIP_BUTTON, timeout=3):
            self.click(self.SKIP_BUTTON)

    def full_otp_flow(self, phone: str, otp_code: str):
        """Complete phone + OTP verification flow."""
        self.enter_phone_number(phone)
        self.tap_send_otp()
        self.enter_otp_code(otp_code)
        self.tap_verify()
