"""
KhotbaPage — Khotba (sermon) screen.
View khotba content, listen to audio, watch live stream.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class KhotbaPage(BasePage):
    """Khotba (Friday sermon) content screen."""

    PAGE_NAME = "khotba_page"

    # ─── Locators ────────────────────────────────────────────────
    KHOTBA_LIST = (By.ID, "com.islam.khutba.qa:id/rv_khotba")
    KHOTBA_TITLE = (By.ID, "com.islam.khutba.qa:id/tv_khotba_title")
    KHOTBA_DATE = (By.ID, "com.islam.khutba.qa:id/tv_khotba_date")
    KHOTBA_CONTENT = (By.ID, "com.islam.khutba.qa:id/tv_khotba_content")
    PLAY_AUDIO_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_play_audio")
    LIVE_STREAM_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_live_stream")
    SHARE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_share")
    FAVORITE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_favorite")
    SEARCH_ICON = (By.ID, "com.islam.khutba.qa:id/btn_search")
    SEARCH_FIELD = (By.ID, "com.islam.khutba.qa:id/et_search")
    EMPTY_STATE = (By.ID, "com.islam.khutba.qa:id/tv_empty")
    LOADING = (By.ID, "com.islam.khutba.qa:id/progress_bar")

    # ─── Tab/Filter ──────────────────────────────────────────────
    TAB_ALL = (By.XPATH, "//*[contains(@text, 'الكل') or contains(@text, 'All')]")
    TAB_FRIDAY = (By.XPATH, "//*[contains(@text, 'الجمعة') or contains(@text, 'Friday')]")

    # ─── Actions ─────────────────────────────────────────────────

    def is_khotba_screen_displayed(self) -> bool:
        return self.is_displayed(self.KHOTBA_LIST, timeout=10) or \
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
        self.wait_for_loader_gone(self.LOADING, timeout=20)
