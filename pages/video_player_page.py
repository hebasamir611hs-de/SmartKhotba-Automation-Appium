"""
VideoPlayerPage — Live stream / video player (VideoPlayerActivity).
Watch khotba live stream or recorded video.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class VideoPlayerPage(BasePage):
    """Video player for live stream and recorded khotba content."""

    PAGE_NAME = "video_player_page"

    # ─── Locators ────────────────────────────────────────────────
    VIDEO_VIEW = (By.ID, "com.islam.khutba.qa:id/video_view")
    PLAY_PAUSE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_play_pause")
    FULLSCREEN_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_fullscreen")
    PROGRESS_BAR = (By.ID, "com.islam.khutba.qa:id/seekbar_progress")
    CURRENT_TIME = (By.ID, "com.islam.khutba.qa:id/tv_current_time")
    TOTAL_TIME = (By.ID, "com.islam.khutba.qa:id/tv_total_time")
    BACK_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_back")
    LIVE_INDICATOR = (By.ID, "com.islam.khutba.qa:id/tv_live_indicator")
    QUALITY_SELECTOR = (By.ID, "com.islam.khutba.qa:id/btn_quality")
    LOADING_SPINNER = (By.ID, "com.islam.khutba.qa:id/progress_loading")
    ERROR_MESSAGE = (By.ID, "com.islam.khutba.qa:id/tv_error")
    RETRY_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_retry")

    # ─── Actions ─────────────────────────────────────────────────

    def is_player_displayed(self) -> bool:
        return self.is_displayed(self.VIDEO_VIEW, timeout=15)

    def is_live(self) -> bool:
        return self.is_displayed(self.LIVE_INDICATOR, timeout=5)

    def play_pause(self):
        self.click(self.PLAY_PAUSE_BUTTON)

    def toggle_fullscreen(self):
        self.click(self.FULLSCREEN_BUTTON)

    def get_current_time(self) -> str:
        return self.get_text(self.CURRENT_TIME)

    def get_total_time(self) -> str:
        return self.get_text(self.TOTAL_TIME)

    def wait_for_video_loaded(self, timeout: int = 30):
        self.wait_for_loader_gone(self.LOADING_SPINNER, timeout=timeout)

    def has_error(self) -> bool:
        return self.is_displayed(self.ERROR_MESSAGE, timeout=5)

    def get_error_text(self) -> str:
        if self.has_error():
            return self.get_text(self.ERROR_MESSAGE)
        return ""

    def retry(self):
        self.click(self.RETRY_BUTTON)

    def go_back(self):
        self.click(self.BACK_BUTTON)
