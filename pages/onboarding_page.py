"""
OnboardingPage — Info/onboarding pages (InfoPagesActivity).
Swipeable intro screens shown on first launch.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class OnboardingPage(BasePage):
    """Onboarding walkthrough screens."""

    PAGE_NAME = "onboarding_page"

    # ─── Locators ────────────────────────────────────────────────
    NEXT_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_next")
    SKIP_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_skip")
    DONE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_done")
    PAGE_INDICATOR = (By.ID, "com.islam.khutba.qa:id/indicator")
    PAGE_TITLE = (By.ID, "com.islam.khutba.qa:id/tv_title")
    PAGE_DESCRIPTION = (By.ID, "com.islam.khutba.qa:id/tv_description")
    PAGE_IMAGE = (By.ID, "com.islam.khutba.qa:id/iv_image")

    # ─── Actions ─────────────────────────────────────────────────

    def is_onboarding_displayed(self) -> bool:
        return self.is_displayed(self.NEXT_BUTTON, timeout=10) or \
               self.is_displayed(self.SKIP_BUTTON, timeout=3)

    def tap_next(self):
        """Go to next onboarding page."""
        self.click(self.NEXT_BUTTON)

    def tap_skip(self):
        """Skip all onboarding pages."""
        self.click(self.SKIP_BUTTON)

    def tap_done(self):
        """Finish onboarding (last page)."""
        self.click(self.DONE_BUTTON)

    def swipe_to_next(self):
        """Swipe left to go to next page."""
        self.swipe("left")

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def complete_onboarding_by_swiping(self, max_pages: int = 5):
        """Swipe through all onboarding pages until done button appears."""
        for _ in range(max_pages):
            if self.is_displayed(self.DONE_BUTTON, timeout=2):
                self.click(self.DONE_BUTTON)
                return
            self.swipe_to_next()
        # Fallback: try done or skip
        if self.is_displayed(self.DONE_BUTTON, timeout=3):
            self.click(self.DONE_BUTTON)
        elif self.is_displayed(self.SKIP_BUTTON, timeout=3):
            self.click(self.SKIP_BUTTON)
