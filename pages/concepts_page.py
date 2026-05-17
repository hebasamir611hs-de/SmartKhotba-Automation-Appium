"""
ConceptsPage — Religious concepts screen (مفاهيم دينية).
Browse and read Islamic educational content.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class ConceptsPage(BasePage):
    """Religious concepts / Islamic knowledge section."""

    PAGE_NAME = "concepts_page"

    # ─── Locators ────────────────────────────────────────────────
    CONCEPTS_LIST = (By.ID, "com.islam.khutba.qa:id/rv_concepts")
    CONCEPT_TITLE = (By.ID, "com.islam.khutba.qa:id/tv_concept_title")
    CONCEPT_DESCRIPTION = (By.ID, "com.islam.khutba.qa:id/tv_concept_desc")
    CONCEPT_IMAGE = (By.ID, "com.islam.khutba.qa:id/iv_concept")
    CATEGORY_TABS = (By.ID, "com.islam.khutba.qa:id/tab_layout")
    SHARE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_share")
    FAVORITE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_favorite")
    BACK_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_back")
    LOADING = (By.ID, "com.islam.khutba.qa:id/progress_bar")

    # ─── Actions ─────────────────────────────────────────────────

    def is_concepts_screen_displayed(self) -> bool:
        return self.is_displayed(self.CONCEPTS_LIST, timeout=10)

    def select_concept_by_index(self, index: int = 0):
        items = (By.XPATH, f"(//androidx.recyclerview.widget.RecyclerView//android.widget.LinearLayout)[{index + 1}]")
        self.click(items)

    def select_concept_by_title(self, title: str):
        locator = (By.XPATH, f"//*[contains(@text, '{title}')]")
        self.scroll_to_element(locator)
        self.click(locator)

    def get_concept_title(self) -> str:
        return self.get_text(self.CONCEPT_TITLE)

    def share_concept(self):
        self.click(self.SHARE_BUTTON)

    def toggle_favorite(self):
        self.click(self.FAVORITE_BUTTON)

    def go_back(self):
        self.click(self.BACK_BUTTON)

    def wait_for_content_loaded(self):
        self.wait_for_loader_gone(self.LOADING, timeout=20)
