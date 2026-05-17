"""
RemindersPage — My Reminders screen (تذكيراتي).
View, create, edit, and delete personal reminders.
"""
from appium.webdriver.common.appiumby import AppiumBy as By
from pages.base_page import BasePage


class RemindersPage(BasePage):
    """Reminders management screen."""

    PAGE_NAME = "reminders_page"

    # ─── Locators ────────────────────────────────────────────────
    REMINDERS_LIST = (By.ID, "com.islam.khutba.qa:id/rv_reminders")
    ADD_REMINDER_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_add_reminder")
    REMINDER_TITLE = (By.ID, "com.islam.khutba.qa:id/tv_reminder_title")
    REMINDER_TIME = (By.ID, "com.islam.khutba.qa:id/tv_reminder_time")
    REMINDER_TOGGLE = (By.ID, "com.islam.khutba.qa:id/switch_reminder")
    DELETE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_delete")
    EDIT_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_edit")
    EMPTY_STATE = (By.ID, "com.islam.khutba.qa:id/tv_empty")

    # ─── Add/Edit Reminder Dialog ────────────────────────────────
    DIALOG_TITLE_INPUT = (By.ID, "com.islam.khutba.qa:id/et_reminder_title")
    DIALOG_TIME_PICKER = (By.ID, "com.islam.khutba.qa:id/time_picker")
    DIALOG_DAYS_SELECTOR = (By.ID, "com.islam.khutba.qa:id/days_selector")
    DIALOG_SAVE_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_save")
    DIALOG_CANCEL_BUTTON = (By.ID, "com.islam.khutba.qa:id/btn_cancel")

    # ─── Confirmation Dialog ─────────────────────────────────────
    CONFIRM_DELETE_YES = (By.ID, "android:id/button1")
    CONFIRM_DELETE_NO = (By.ID, "android:id/button2")

    # ─── Actions ─────────────────────────────────────────────────

    def is_reminders_screen_displayed(self) -> bool:
        return self.is_displayed(self.ADD_REMINDER_BUTTON, timeout=10) or \
               self.is_displayed(self.EMPTY_STATE, timeout=5)

    def has_reminders(self) -> bool:
        return not self.is_displayed(self.EMPTY_STATE, timeout=3)

    def add_reminder(self, title: str):
        """Open add reminder dialog and set title."""
        self.click(self.ADD_REMINDER_BUTTON)
        self.type_text(self.DIALOG_TITLE_INPUT, title)

    def save_reminder(self):
        self.click(self.DIALOG_SAVE_BUTTON)

    def cancel_reminder(self):
        self.click(self.DIALOG_CANCEL_BUTTON)

    def toggle_reminder(self, index: int = 0):
        """Enable/disable a reminder by index."""
        toggles = (By.XPATH, f"(//android.widget.Switch)[{index + 1}]")
        self.click(toggles)

    def delete_reminder(self, index: int = 0, confirm: bool = True):
        """Delete a reminder by index."""
        delete_btns = (By.XPATH, f"(//android.widget.ImageButton[@resource-id='com.islam.khutba.qa:id/btn_delete'])[{index + 1}]")
        self.click(delete_btns)
        if confirm:
            self.click(self.CONFIRM_DELETE_YES)
        else:
            self.click(self.CONFIRM_DELETE_NO)

    def get_reminder_count(self) -> int:
        """Count visible reminders."""
        try:
            items = self.driver.find_elements(By.ID, "com.islam.khutba.qa:id/tv_reminder_title")
            return len(items)
        except Exception:
            return 0
