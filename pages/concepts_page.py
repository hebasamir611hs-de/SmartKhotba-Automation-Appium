"""
ConceptsPage — Religious concepts screen (مفاهيم دينية).
Browse and read Islamic educational content.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class ConceptsPage(BasePage):
    """Religious concepts / Islamic knowledge section."""

    PAGE_NAME = "concepts_page"

    # ─── Locators (Compose — text/content-desc based) ─────────────
    CONCEPTS_TITLE = (By.XPATH, "//*[@text='مفاهيم ومصطلحات دينية وردت في خطب الجمعة']")
    CONCEPTS_SEARCH = (By.XPATH, "//*[@text='ادخل كلمة للبحث ..']")
    CONCEPTS_LIST = (By.CLASS_NAME, "android.widget.ScrollView")
    LOADING = (By.CLASS_NAME, "android.widget.ProgressBar")

    # ─── Actions ─────────────────────────────────────────────────

    def is_concepts_screen_displayed(self) -> bool:
        return self.is_displayed(self.CONCEPTS_TITLE, timeout=10) or \
               self.is_displayed(self.CONCEPTS_SEARCH, timeout=5)

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
