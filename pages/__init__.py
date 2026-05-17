"""SmartKhotba Page Objects — all app screens."""

from pages.base_page import BasePage
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage
from pages.location_page import LocationPage
from pages.onboarding_page import OnboardingPage
from pages.otp_page import OTPPage
from pages.main_page import MainPage
from pages.khotba_page import KhotbaPage
from pages.concepts_page import ConceptsPage
from pages.reminders_page import RemindersPage
from pages.favorites_page import FavoritesPage
from pages.settings_page import SettingsPage
from pages.video_player_page import VideoPlayerPage

__all__ = [
    "BasePage", "SplashPage", "LanguagePage", "LocationPage",
    "OnboardingPage", "OTPPage", "MainPage", "KhotbaPage",
    "ConceptsPage", "RemindersPage", "FavoritesPage",
    "SettingsPage", "VideoPlayerPage",
]
