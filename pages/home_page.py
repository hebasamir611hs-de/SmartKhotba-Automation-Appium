"""
HomePage — SmartKhotba Main/Home Screen.
Verified via Appium page_source on real device (2026-06-03).
Compose UI — no resource-ids; uses content-desc and text.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for SmartKhotba home/main screen (alias for MainPage content area)."""

    PAGE_NAME = "home_page"

    # ─── Locators (verified from live app) ───────────────────────
    WELCOME_TEXT = (By.XPATH, "//*[contains(@text, 'أهلا بك')]")
    LOGO = (By.XPATH, "//*[@content-desc='Logo']")
    LIVE_STREAM = (By.XPATH, "//*[@text='البث المباشر']")
    CONCEPTS_CARD = (By.XPATH, "//*[@content-desc='مفاهيم دينية']")

    # ─── Actions ─────────────────────────────────────────────────

    def is_home_displayed(self) -> bool:
        """Verify home screen loaded."""
        return self.is_displayed(self.WELCOME_TEXT, timeout=10) or \
               self.is_displayed(self.LOGO, timeout=5)

    def get_welcome_text(self) -> str:
        """Get welcome/greeting text."""
        return self.get_text(self.WELCOME_TEXT)

    def open_live_stream(self):
        """Tap live stream card."""
        self.click(self.LIVE_STREAM)

    def open_concepts(self):
        """Tap concepts card from home."""
        self.click(self.CONCEPTS_CARD)
