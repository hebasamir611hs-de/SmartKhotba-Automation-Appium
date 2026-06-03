"""
KhotbaPage — Khotba (sermon) screen.
View khotba content, listen to audio, watch live stream.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class KhotbaPage(BasePage):
    """Khotba (Friday sermon) content screen."""

    PAGE_NAME = "khotba_page"

    # ─── Locators (verified from live device 2026-06-03) ────────────
    KHOTBA_TITLE = (By.XPATH, "//android.widget.TextView[@text='الخطب السابقة']")
    MOSQUE_SELECTOR = (By.XPATH, "//*[@text='اختر المسجد']")
    SEARCH_ICON = (By.XPATH, "//*[@content-desc='بحث']")
    LOADING = (By.CLASS_NAME, "android.widget.ProgressBar")

    # ─── Actions ─────────────────────────────────────────────────

    def is_khotba_screen_displayed(self) -> bool:
        return self.is_displayed(self.MOSQUE_SELECTOR, timeout=15) or \
               self.is_displayed(self.KHOTBA_TITLE, timeout=5)

    def select_khotba_by_index(self, index: int = 0):
        """Select a khotba from the list by position."""
        items = (By.XPATH, f"(//androidx.recyclerview.widget.RecyclerView//android.widget.LinearLayout)[{index + 1}]")
        self.click(items)

    def select_khotba_by_title(self, title: str):
        """Select a khotba by its title text."""
        locator = (By.XPATH, f"//*[contains(@text, '{title}')]")
        self.scroll_to_element(locator)
        self.click(locator)

    def play_audio(self):
        self.click(self.PLAY_AUDIO_BUTTON)

    def open_live_stream(self):
        self.click(self.LIVE_STREAM_BUTTON)

    def share_khotba(self):
        self.click(self.SHARE_BUTTON)

    def toggle_favorite(self):
        self.click(self.FAVORITE_BUTTON)

    def search_khotba(self, query: str):
        self.click(self.SEARCH_ICON)
        self.type_text(self.SEARCH_FIELD, query)

    def get_khotba_title(self) -> str:
        return self.get_text(self.KHOTBA_TITLE)

    def get_khotba_content(self) -> str:
        return self.get_text(self.KHOTBA_CONTENT)

    def is_empty_state(self) -> bool:
        return self.is_displayed(self.EMPTY_STATE, timeout=5)

    def wait_for_content_loaded(self):
        self.wait_for_loader_gone(self.LOADING, timeout=10)
        from utils.wait_helpers import wait_for_element
        wait_for_element(self.driver, self.MOSQUE_SELECTOR, timeout=15)
