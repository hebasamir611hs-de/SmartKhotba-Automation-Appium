"""
LanguagePage — Language selection screen (LanguageActivity).
Shown on first launch or from settings.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class LanguagePage(BasePage):
    """Language selection screen — Arabic / English / other."""

    PAGE_NAME = "language_page"

    # ─── Locators ────────────────────────────────────────────────
    ARABIC_OPTION = (By.ID, "com.islam.khutba.qa:id/btn_arabic")
    ENGLISH_OPTION = (By.ID, "com.islam.khutba.qa:id/btn_english")
    CONFIRM_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_confirm")
    TITLE = (By.ID, "com.islam.khutba.qa:id/tv_title")

    # Alternatives if buttons are text-based
    ARABIC_TEXT = (By.XPATH, "//*[contains(@text, 'العربية')]")
    ENGLISH_TEXT = (By.XPATH, "//*[contains(@text, 'English')]")

    # ─── Actions ─────────────────────────────────────────────────

    def is_language_screen_displayed(self) -> bool:
        return self.is_displayed(self.ARABIC_TEXT, timeout=10) or \
               self.is_displayed(self.ARABIC_OPTION, timeout=3)

    def select_arabic(self):
        """Select Arabic language."""
        try:
            self.click(self.ARABIC_OPTION)
        except Exception:
            self.click(self.ARABIC_TEXT)

    def select_english(self):
        """Select English language."""
        try:
            self.click(self.ENGLISH_OPTION)
        except Exception:
            self.click(self.ENGLISH_TEXT)

    def confirm_selection(self):
        """Tap confirm/continue button if exists."""
        if self.is_displayed(self.CONFIRM_BUTTON, timeout=3):
            self.click(self.CONFIRM_BUTTON)
