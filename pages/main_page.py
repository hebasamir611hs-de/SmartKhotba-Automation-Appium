"""
MainPage — Main screen with bottom navigation (MainActivity).
Hub for all main features: Khotba, Concepts, Reminders, etc.
Verified via page_source on real device (2026-06-03).
Compose UI — no resource-ids on nav items; text is the only stable identifier.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Main screen — bottom nav, drawer menu, primary content area."""

    PAGE_NAME = "main_page"

    # ─── Content Area (prefer content-desc over text) ────────────
    LOGO = (By.XPATH, "//*[@content-desc='Logo']")
    WELCOME_TEXT = (By.XPATH, "//*[contains(@text, 'أهلا بك')]")
    LIVE_STREAM = (By.XPATH, "//*[@text='البث المباشر']")
    CONCEPTS_CARD = (By.XPATH, "//*[@content-desc='مفاهيم دينية']")

    # ─── Bottom Navigation ───────────────────────────────────────
    # Compose UI exposes no resource-id or content-desc on nav items.
    # Text-based XPath is the only viable strategy (verified 2026-06-03).
    NAV_HOME = (By.XPATH, "//android.widget.TextView[@text='الرئيسية']")
    NAV_KHOTBA = (By.XPATH, "//android.widget.TextView[@text='الخطب السابقة']")
    NAV_CONCEPTS = (By.XPATH, "//android.widget.TextView[@text='مفاهيم دينية']")
    NAV_SEARCH = (By.XPATH, "//android.widget.TextView[@text='بحث']")
    NAV_MORE = (By.XPATH, "//android.widget.TextView[@text='المزيد']")

    # ─── Actions ─────────────────────────────────────────────────

    def is_main_screen_displayed(self) -> bool:
        return self.is_displayed(self.LOGO, timeout=15) or \
               self.is_displayed(self.WELCOME_TEXT, timeout=5)

    def navigate_to_home(self):
        self.click(self.NAV_HOME)

    def navigate_to_khotba(self):
        self.click(self.NAV_KHOTBA)

    def navigate_to_concepts(self):
        self.click(self.NAV_CONCEPTS)

    def navigate_to_search(self):
        self.click(self.NAV_SEARCH)

    def navigate_to_more(self):
        self.click(self.NAV_MORE)
