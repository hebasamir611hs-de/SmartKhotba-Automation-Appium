"""
Test Helpers — Shared navigation shortcuts to avoid duplication.
"""
from appium.webdriver.webdriver import WebDriver
from pages.splash_page import SplashPage
from pages.language_page import LanguagePage
from pages.location_page import LocationPage
from pages.onboarding_page import OnboardingPage
from pages.otp_page import OTPPage
from pages.main_page import MainPage


def navigate_to_main(driver: WebDriver) -> MainPage:
    """Skip through all onboarding steps to reach main screen.
    
    Used by tests that need MainPage as a precondition.
    Handles: Splash → Language → Location → Onboarding → OTP → Main
    """
    splash = SplashPage(driver)
    if splash.is_splash_displayed():
        splash.wait_for_splash_to_finish()

    lang = LanguagePage(driver)
    if lang.is_language_screen_displayed():
        lang.select_arabic()
        lang.confirm_selection()

    location = LocationPage(driver)
    if location.is_location_screen_displayed():
        location.skip_location()

    onboarding = OnboardingPage(driver)
    if onboarding.is_onboarding_displayed():
        onboarding.complete_onboarding_by_swiping()

    otp = OTPPage(driver)
    if otp.is_otp_screen_displayed():
        otp.skip_otp()

    main = MainPage(driver)
    return main
