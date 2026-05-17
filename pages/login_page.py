"""
LoginPage — SmartKhotba Login Screen.
[PLACEHOLDER — Needs APK inspection for actual locators]
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for SmartKhotba login screen."""

    PAGE_NAME = "login_page"

    # ─── Locators (update after APK inspection) ──────────────────
    USERNAME_FIELD = (By.ID, "com.islam.khutba.qa:id/username")
    PASSWORD_FIELD = (By.ID, "com.islam.khutba.qa:id/password")
    LOGIN_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_login")
    ERROR_MESSAGE = (By.ID, "com.islam.khutba.qa:id/error_text")
    FORGOT_PASSWORD = (By.ID, "com.islam.khutba.qa:id/forgot_password")

    # ─── Actions ─────────────────────────────────────────────────

    def login(self, username: str, password: str):
        """Perform login with given credentials."""
        self.type_text(self.USERNAME_FIELD, username)
        self.type_text(self.PASSWORD_FIELD, password)
        self.hide_keyboard()
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Get login error text."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_page_displayed(self) -> bool:
        """Verify login page is loaded."""
        return self.is_displayed(self.LOGIN_BUTTON)
