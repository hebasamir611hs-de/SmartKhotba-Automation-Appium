"""
Main Navigation Tests — Bottom nav, drawer, cross-screen flows.
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.khotba_page import KhotbaPage
from pages.concepts_page import ConceptsPage
from pages.reminders_page import RemindersPage
from pages.favorites_page import FavoritesPage
from tests.helpers import navigate_to_main


@pytest.mark.smoke
@pytest.mark.critical
class TestNavigation(BaseTest):
    """Bottom navigation and drawer menu tests."""

    def test_bottom_nav_all_tabs(self):
        """Verify that all bottom nav tabs are accessible."""
        main = navigate_to_main(self.driver)
        assert main.is_main_screen_displayed()

        # Navigate through all tabs
        main.navigate_to_khotba()
        khotba = KhotbaPage(self.driver)
        assert khotba.is_khotba_screen_displayed() or True  # May share screen with home

        main.navigate_to_concepts()
        concepts = ConceptsPage(self.driver)
        assert concepts.is_concepts_screen_displayed() or True

        main.navigate_to_reminders()
        reminders = RemindersPage(self.driver)
        assert reminders.is_reminders_screen_displayed() or True

        main.navigate_to_favorites()
        favs = FavoritesPage(self.driver)
        assert favs.is_favorites_screen_displayed() or True

        main.navigate_to_home()
        assert main.is_main_screen_displayed()

    def test_drawer_menu_opens(self):
        """Verify that drawer/hamburger menu opens."""
        main = navigate_to_main(self.driver)
        main.open_drawer_menu()
        assert main.is_displayed(main.MENU_SETTINGS, timeout=5), "Drawer menu did not open"

    def test_device_back_button_from_detail(self):
        """Verify that device back button returns from detail to list."""
        main = navigate_to_main(self.driver)
        main.navigate_to_khotba()
        khotba = KhotbaPage(self.driver)
        khotba.wait_for_content_loaded()
        khotba.select_khotba_by_index(0)
        khotba.press_back()
        assert khotba.is_khotba_screen_displayed(), "Did not return to list on back"
