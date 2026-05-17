"""
HomePage — SmartKhotba Main/Home Screen.
[PLACEHOLDER — Needs APK inspection for actual locators]
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for SmartKhotba home/main screen."""

    PAGE_NAME = "home_page"

    # ─── Locators (update after APK inspection) ──────────────────
    WELCOME_TEXT = (By.ID, "com.islam.khutba.qa:id/welcome_text")
    MENU_BUTTON = (By.ACCESSIBILITY_ID, "Menu")
    PROFILE_ICON = (By.ID, "com.islam.khutba.qa:id/profile_icon")

    # ─── Actions ─────────────────────────────────────────────────

    def is_home_displayed(self) -> bool:
        """Verify home screen loaded after login."""
        return self.is_displayed(self.WELCOME_TEXT)

    def get_welcome_text(self) -> str:
        """Get welcome/greeting text."""
        return self.get_text(self.WELCOME_TEXT)

    def open_menu(self):
        """Open navigation menu."""
        self.click(self.MENU_BUTTON)
