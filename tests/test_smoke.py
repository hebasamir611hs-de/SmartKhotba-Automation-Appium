"""
Smoke Tests — Quick post-deploy validation.
Covers: app launch, onboarding, main screen, key features accessible.
"""
import pytest
from tests.base_test import BaseTest
from pages.main_page import MainPage
from pages.khotba_page import KhotbaPage
from pages.concepts_page import ConceptsPage
from tests.helpers import navigate_to_main


@pytest.mark.smoke
@pytest.mark.critical
class TestSmoke(BaseTest):
    """Fast smoke tests — run after every deploy."""

    def test_app_launches(self):
        """Verify that app launches and reaches main screen."""
        main = MainPage(self.driver)
        assert main.is_main_screen_displayed(), \
            "App failed to reach main screen after launch"

    def test_reaches_main_screen(self):
        """Verify that main screen is reachable through onboarding."""
        main = navigate_to_main(self.driver)
        assert main.is_main_screen_displayed(), "Main screen not reached"

    def test_khotba_section_accessible(self):
        """Verify that khotba section loads."""
        main = navigate_to_main(self.driver)
        main.navigate_to_khotba()
        khotba = KhotbaPage(self.driver)
        khotba.wait_for_content_loaded()
        assert khotba.is_khotba_screen_displayed()

    def test_concepts_section_accessible(self):
        """Verify that concepts section loads."""
        main = navigate_to_main(self.driver)
        main.navigate_to_concepts()
        concepts = ConceptsPage(self.driver)
        concepts.wait_for_content_loaded()
        assert concepts.is_concepts_screen_displayed()
