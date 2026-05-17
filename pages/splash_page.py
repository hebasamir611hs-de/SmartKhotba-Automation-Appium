"""
SplashPage — App launch / splash screen.
First screen shown when app starts (SplashActivity).
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class SplashPage(BasePage):
    """Splash screen — auto-transitions to Language or Main screen."""

    PAGE_NAME = "splash_page"

    # ─── Locators ────────────────────────────────────────────────
    APP_LOGO = (By.ID, "com.islam.khutba.qa:id/splash_logo")
    LOADING_INDICATOR = (By.ID, "com.islam.khutba.qa:id/progress_bar")

    # ─── Actions ─────────────────────────────────────────────────

    def is_splash_displayed(self) -> bool:
        """Verify splash screen is loaded."""
        return self.is_displayed(self.APP_LOGO, timeout=10)

    def wait_for_splash_to_finish(self, timeout: int = 15):
        """Wait for splash to auto-transition to next screen."""
        from utils.wait_helpers import wait_for_element_absent
        wait_for_element_absent(self.driver, self.APP_LOGO, timeout=timeout)
