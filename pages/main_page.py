"""
MainPage — Main screen with bottom navigation (MainActivity).
Hub for all main features: Khotba, Concepts, Reminders, etc.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class MainPage(BasePage):
    """Main screen — bottom nav, drawer menu, primary content area."""

    PAGE_NAME = "main_page"

    # ─── Bottom Navigation ───────────────────────────────────────
    NAV_HOME = (By.ID, "com.islam.khutba.qa:id/nav_home")
    NAV_KHOTBA = (By.ID, "com.islam.khutba.qa:id/nav_khotba")
    NAV_CONCEPTS = (By.ID, "com.islam.khutba.qa:id/nav_concepts")
    NAV_REMINDERS = (By.ID, "com.islam.khutba.qa:id/nav_reminders")
    NAV_FAVORITES = (By.ID, "com.islam.khutba.qa:id/nav_favorites")
    NAV_MORE = (By.ID, "com.islam.khutba.qa:id/nav_more")

    # ─── Drawer / Menu ───────────────────────────────────────────
    MENU_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_menu")
    DRAWER_LAYOUT = (By.ID, "com.islam.khutba.qa:id/drawer_layout")
    MENU_SETTINGS = (By.XPATH, "//*[contains(@text, 'الإعدادات') or contains(@text, 'Settings')]")
    MENU_SHARE = (By.XPATH, "//*[contains(@text, 'مشاركة') or contains(@text, 'Share')]")
    MENU_ABOUT = (By.XPATH, "//*[contains(@text, 'عن التطبيق') or contains(@text, 'About')]")

    # ─── Content Area ────────────────────────────────────────────
    TOOLBAR_TITLE = (By.ID, "com.islam.khutba.qa:id/toolbar_title")
    CONTENT_AREA = (By.ID, "com.islam.khutba.qa:id/fragment_container")

    # ─── Actions ─────────────────────────────────────────────────

    def is_main_screen_displayed(self) -> bool:
        return self.is_displayed(self.NAV_HOME, timeout=15) or \
               self.is_displayed(self.MENU_BUTTON, timeout=5)

    def navigate_to_home(self):
        self.click(self.NAV_HOME)

    def navigate_to_khotba(self):
        self.click(self.NAV_KHOTBA)

    def navigate_to_concepts(self):
        self.click(self.NAV_CONCEPTS)

    def navigate_to_reminders(self):
        self.click(self.NAV_REMINDERS)

    def navigate_to_favorites(self):
        self.click(self.NAV_FAVORITES)

    def navigate_to_more(self):
        self.click(self.NAV_MORE)

    def open_drawer_menu(self):
        self.click(self.MENU_BUTTON)

    def go_to_settings(self):
        self.open_drawer_menu()
        self.click(self.MENU_SETTINGS)

    def go_to_share_app(self):
        self.open_drawer_menu()
        self.click(self.MENU_SHARE)

    def get_toolbar_title(self) -> str:
        return self.get_text(self.TOOLBAR_TITLE)
