"""
FavoritesPage — Favorites screen (المفضلة).
View and manage saved khotbas and concepts.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class FavoritesPage(BasePage):
    """Favorites / bookmarked items screen."""

    PAGE_NAME = "favorites_page"

    # ─── Locators ────────────────────────────────────────────────
    FAVORITES_LIST = (By.ID, "com.islam.khutba.qa:id/rv_favorites")
    FAVORITE_ITEM_TITLE = (By.ID, "com.islam.khutba.qa:id/tv_title")
    REMOVE_FAVORITE = (By.ID, "com.islam.khutba.qa:id/btn_remove_favorite")
    EMPTY_STATE = (By.ID, "com.islam.khutba.qa:id/tv_empty")
    TAB_KHOTBA = (By.XPATH, "//*[contains(@text, 'خطب') or contains(@text, 'Khotba')]")
    TAB_CONCEPTS = (By.XPATH, "//*[contains(@text, 'مفاهيم') or contains(@text, 'Concepts')]")

    # ─── Actions ─────────────────────────────────────────────────

    def is_favorites_screen_displayed(self) -> bool:
        return self.is_displayed(self.FAVORITES_LIST, timeout=10) or \
               self.is_displayed(self.EMPTY_STATE, timeout=5)

    def is_empty(self) -> bool:
        return self.is_displayed(self.EMPTY_STATE, timeout=3)

    def get_favorites_count(self) -> int:
        try:
            items = self.driver.find_elements(By.ID, "com.islam.khutba.qa:id/tv_title")
            return len(items)
        except Exception:
            return 0

    def remove_favorite_by_index(self, index: int = 0):
        locator = (By.XPATH, f"(//android.widget.ImageButton[@resource-id='com.islam.khutba.qa:id/btn_remove_favorite'])[{index + 1}]")
        self.click(locator)

    def open_favorite_by_index(self, index: int = 0):
        locator = (By.XPATH, f"(//android.widget.TextView[@resource-id='com.islam.khutba.qa:id/tv_title'])[{index + 1}]")
        self.click(locator)

    def filter_by_khotba(self):
        self.click(self.TAB_KHOTBA)

    def filter_by_concepts(self):
        self.click(self.TAB_CONCEPTS)
