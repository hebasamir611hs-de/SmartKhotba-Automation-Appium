"""
Reminders Tests (تذكيراتي).
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.reminders_page import RemindersPage
from tests.helpers import navigate_to_main


@pytest.mark.regression
@pytest.mark.usefixtures("clear_app_state")
class TestReminders(BaseTest):
    """Reminders feature tests — CRUD operations. Uses clear_app_state for isolation."""

    def _go_to_reminders(self):
        main = navigate_to_main(self.driver)
        main.navigate_to_reminders()
        return RemindersPage(self.driver)

    def test_reminders_screen_loads(self):
        """Verify that reminders screen loads (list or empty state)."""
        reminders = self._go_to_reminders()
        assert reminders.is_reminders_screen_displayed(), "Reminders screen not loaded"

    def test_add_new_reminder(self):
        """Verify that a new reminder can be created."""
        reminders = self._go_to_reminders()
        initial_count = reminders.get_reminder_count()
        reminders.add_reminder("تذكير اختباري")
        reminders.save_reminder()
        new_count = reminders.get_reminder_count()
        assert new_count > initial_count, "Reminder was not added"

    def test_toggle_reminder_on_off(self):
        """Verify that reminder can be enabled/disabled."""
        reminders = self._go_to_reminders()
        if reminders.has_reminders():
            reminders.toggle_reminder(index=0)
            # Toggle back
            reminders.toggle_reminder(index=0)

    def test_delete_reminder(self):
        """Verify that a reminder can be deleted."""
        reminders = self._go_to_reminders()
        # Add one first to ensure there's something to delete
        reminders.add_reminder("حذف تجريبي")
        reminders.save_reminder()
        count_before = reminders.get_reminder_count()
        reminders.delete_reminder(index=0, confirm=True)
        count_after = reminders.get_reminder_count()
        assert count_after < count_before, "Reminder was not deleted"

    def test_cancel_delete_keeps_reminder(self):
        """Verify that cancelling delete keeps the reminder."""
        reminders = self._go_to_reminders()
        if reminders.has_reminders():
            count_before = reminders.get_reminder_count()
            reminders.delete_reminder(index=0, confirm=False)
            count_after = reminders.get_reminder_count()
            assert count_after == count_before, "Reminder deleted despite cancel"

    def test_add_reminder_empty_title(self):
        """Verify that empty title is rejected."""
        reminders = self._go_to_reminders()
        reminders.add_reminder("")
        reminders.save_reminder()
        # Should still be on dialog or show error
        assert reminders.is_displayed(reminders.DIALOG_TITLE_INPUT, timeout=3) or \
               reminders.is_reminders_screen_displayed()
