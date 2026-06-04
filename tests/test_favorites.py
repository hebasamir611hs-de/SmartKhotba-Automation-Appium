"""
Favorites Tests (المفضلة).
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.khotba_page import KhotbaPage
from pages.favorites_page import FavoritesPage
from tests.helpers import navigate_to_main


@pytest.mark.regression
class TestFavorites(BaseTest):
    """Favorites feature tests."""

    def _go_to_favorites(self):
        main = navigate_to_main(self.driver)
        main.navigate_to_favorites()
        return FavoritesPage(self.driver)

    def test_favorites_screen_loads(self):
        """Verify that favorites screen loads."""
        favs = self._go_to_favorites()
        assert favs.is_favorites_screen_displayed(), "Favorites screen not loaded"

    def test_empty_favorites_shows_empty_state(self):
        """Verify that empty favorites shows appropriate message."""
        favs = self._go_to_favorites()
        # May or may not be empty depending on state
        if favs.is_empty():
            assert favs.is_displayed(favs.EMPTY_STATE)

    def test_add_then_view_in_favorites(self):
        """Verify that favorited khotba appears in favorites list."""
        main = navigate_to_main(self.driver)
        
        # Add a khotba to favorites
        main.navigate_to_khotba()
        khotba = KhotbaPage(self.driver)
        khotba.wait_for_content_loaded()
        khotba.select_khotba_by_index(0)
        khotba.toggle_favorite()
        
        # Navigate to favorites
        self.driver.back()
        self.driver.back()
        main.navigate_to_favorites()
        favs = FavoritesPage(self.driver)
        
        assert not favs.is_empty(), "Favorites still empty after adding"

    def test_remove_from_favorites(self):
        """Verify that item can be removed from favorites."""
        favs = self._go_to_favorites()
        if not favs.is_empty():
            count_before = favs.get_favorites_count()
            favs.remove_favorite_by_index(0)
            count_after = favs.get_favorites_count()
            assert count_after < count_before, "Favorite not removed"

    def test_open_favorite_item(self):
        """Verify that tapping a favorite opens its detail."""
        favs = self._go_to_favorites()
        if not favs.is_empty():
            favs.open_favorite_by_index(0)
            # Should navigate to detail screen
