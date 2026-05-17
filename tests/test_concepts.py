"""
Religious Concepts Tests (مفاهيم دينية).
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.concepts_page import ConceptsPage
from tests.helpers import navigate_to_main


@pytest.mark.regression
class TestConcepts(BaseTest):
    """Religious concepts feature tests."""

    def _go_to_concepts(self):
        main = navigate_to_main(self.driver)
        main.navigate_to_concepts()
        return ConceptsPage(self.driver)

    def test_concepts_list_loads(self):
        """Verify that concepts list loads with content."""
        concepts = self._go_to_concepts()
        concepts.wait_for_content_loaded()
        assert concepts.is_concepts_screen_displayed(), "Concepts list not loaded"

    def test_open_concept_detail(self):
        """Verify that tapping a concept opens detail view."""
        concepts = self._go_to_concepts()
        concepts.wait_for_content_loaded()
        concepts.select_concept_by_index(0)
        title = concepts.get_concept_title()
        assert title != "", "Concept detail has no title"

    def test_share_concept(self):
        """Verify that concept can be shared."""
        concepts = self._go_to_concepts()
        concepts.wait_for_content_loaded()
        concepts.select_concept_by_index(0)
        concepts.share_concept()

    def test_add_concept_to_favorites(self):
        """Verify that concept can be added to favorites."""
        concepts = self._go_to_concepts()
        concepts.wait_for_content_loaded()
        concepts.select_concept_by_index(0)
        concepts.toggle_favorite()

    def test_back_navigation_from_concept(self):
        """Verify that back button returns to concepts list."""
        concepts = self._go_to_concepts()
        concepts.wait_for_content_loaded()
        concepts.select_concept_by_index(0)
        concepts.go_back()
        assert concepts.is_concepts_screen_displayed(), "Did not return to concepts list"
