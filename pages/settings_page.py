"""
SettingsPage — Settings screen.
Change language, font size, share app, about, notifications.
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SettingsPage(BasePage):
    """App settings screen."""

    PAGE_NAME = "settings_page"

    # ─── Locators ────────────────────────────────────────────────
    # Language
    CHANGE_LANGUAGE = (By.XPATH, "//*[contains(@text, 'اللغة') or contains(@text, 'Language')]")
    LANGUAGE_ARABIC = (By.XPATH, "//*[contains(@text, 'العربية')]")
    LANGUAGE_ENGLISH = (By.XPATH, "//*[contains(@text, 'English')]")

    # Font
    CHANGE_FONT = (By.XPATH, "//*[contains(@text, 'الخط') or contains(@text, 'Font')]")
    FONT_SMALL = (By.ID, "com.islam.khutba.qa:id/btn_font_small")
    FONT_MEDIUM = (By.ID, "com.islam.khutba.qa:id/btn_font_medium")
    FONT_LARGE = (By.ID, "com.islam.khutba.qa:id/btn_font_large")
    FONT_SLIDER = (By.ID, "com.islam.khutba.qa:id/seekbar_font")
    FONT_PREVIEW = (By.ID, "com.islam.khutba.qa:id/tv_font_preview")

    # Notifications
    NOTIFICATIONS_TOGGLE = (By.ID, "com.islam.khutba.qa:id/switch_notifications")

    # Share App
    SHARE_APP = (By.XPATH, "//*[contains(@text, 'مشاركة') or contains(@text, 'Share')]")

    # About
    ABOUT_APP = (By.XPATH, "//*[contains(@text, 'عن التطبيق') or contains(@text, 'About')]")
    APP_VERSION = (By.ID, "com.islam.khutba.qa:id/tv_version")

    # Location
    CHANGE_LOCATION = (By.XPATH, "//*[contains(@text, 'الموقع') or contains(@text, 'Location')]")

    # Back
    BACK_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_back")

    # ─── Actions ─────────────────────────────────────────────────

    def is_settings_displayed(self) -> bool:
        return self.is_displayed(self.CHANGE_LANGUAGE, timeout=10)

    def change_language_to_arabic(self):
        self.click(self.CHANGE_LANGUAGE)
        self.click(self.LANGUAGE_ARABIC)

    def change_language_to_english(self):
        self.click(self.CHANGE_LANGUAGE)
        self.click(self.LANGUAGE_ENGLISH)

    def change_font_size(self, size: str = "medium"):
        """Change font size: small, medium, large."""
        self.click(self.CHANGE_FONT)
        size_map = {
            "small": self.FONT_SMALL,
            "medium": self.FONT_MEDIUM,
            "large": self.FONT_LARGE,
        }
        if size not in size_map:
            raise ValueError(f"Invalid font size: {size}. Use: small, medium, large")
        self.click(size_map[size])

    def get_font_preview_text(self) -> str:
        return self.get_text(self.FONT_PREVIEW)

    def toggle_notifications(self):
        self.click(self.NOTIFICATIONS_TOGGLE)

    def tap_share_app(self):
        self.click(self.SHARE_APP)

    def tap_about(self):
        self.click(self.ABOUT_APP)

    def get_app_version(self) -> str:
        self.tap_about()
        return self.get_text(self.APP_VERSION)

    def change_location(self):
        self.click(self.CHANGE_LOCATION)

    def go_back(self):
        self.click(self.BACK_BUTTON)
