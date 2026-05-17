"""
BasePage — Foundation for all Page Objects.
Encapsulates common mobile interactions: click, type, wait, swipe, scroll.
"""
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.common.exceptions import NoSuchElementException
from utils.wait_helpers import (
    wait_for_element,
    wait_for_element_clickable,
    wait_for_element_absent
)
from utils.logger import get_logger
from utils.locator_healing import LocatorHealer

logger = get_logger(__name__)


class BasePage:
    """Base class for all page objects. All pages inherit from this."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # ─── Element Interactions ────────────────────────────────────────

    def _extract_element_name(self, locator: tuple) -> str:
        """Derive element_name from locator for registry lookup.
        (By.ID, 'com.islam.khutba.qa:id/btn_login') → 'btn_login'
        Falls back to raw selector string for non-ID strategies.
        """
        strategy, selector = locator
        if ":id/" in selector:
            return selector.split(":id/")[-1]
        return selector

    def find(self, locator: tuple):
        """Find element with explicit wait and healing."""
        try:
            return wait_for_element(self.driver, locator)
        except Exception:
            return LocatorHealer.heal(
                self.driver,
                locator,
                page_name=getattr(self, "PAGE_NAME", None),
                element_name=self._extract_element_name(locator),
            )

    def click(self, locator: tuple):
        """Wait for element to be clickable, then click (with healing)."""
        try:
            element = wait_for_element_clickable(self.driver, locator)
            element.click()
        except Exception:
            element = LocatorHealer.heal(
                self.driver,
                locator,
                page_name=getattr(self, "PAGE_NAME", None),
                element_name=self._extract_element_name(locator),
            )
            element.click()
        logger.debug(f"Clicked: {locator}")

    def type_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Type text into an input field."""
        element = self.find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug(f"Typed '{text}' into {locator}")

    def get_text(self, locator: tuple) -> str:
        """Get text from element."""
        element = self.find(locator)
        return element.text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Get element attribute value."""
        element = self.find(locator)
        return element.get_attribute(attribute)

    def is_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """Check if element is visible (non-throwing)."""
        try:
            wait_for_element(self.driver, locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Check if element exists in DOM (may not be visible)."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    # ─── Gestures ────────────────────────────────────────────────────

    def swipe(self, direction: str = "up", duration: int = 800):
        """Swipe in specified direction.
        
        Args:
            direction: 'up', 'down', 'left', 'right'
            duration: Swipe duration in ms
        """
        size = self.driver.get_window_size()
        w, h = size["width"], size["height"]

        coords = {
            "up":    {"start": (w // 2, int(h * 0.7)), "end": (w // 2, int(h * 0.3))},
            "down":  {"start": (w // 2, int(h * 0.3)), "end": (w // 2, int(h * 0.7))},
            "left":  {"start": (int(w * 0.8), h // 2), "end": (int(w * 0.2), h // 2)},
            "right": {"start": (int(w * 0.2), h // 2), "end": (int(w * 0.8), h // 2)},
        }

        if direction not in coords:
            raise ValueError(f"Invalid direction: {direction}")

        start = coords[direction]["start"]
        end = coords[direction]["end"]
        
        self.driver.swipe(start[0], start[1], end[0], end[1], duration)
        logger.debug(f"Swiped {direction}")

    def scroll_to_text(self, text: str):
        """Scroll until text is visible (Android UiScrollable)."""
        self.driver.find_element(
            By.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().textContains("{text}"))'
        )
        logger.debug(f"Scrolled to text: {text}")

    def scroll_to_element(self, locator: tuple, max_swipes: int = 5) -> bool:
        """Scroll down until element is found or max swipes reached."""
        for i in range(max_swipes):
            if self.is_displayed(locator, timeout=2):
                return True
            self.swipe("up")
        logger.warning(f"Element {locator} not found after {max_swipes} swipes")
        return False

    # ─── Waits ───────────────────────────────────────────────────────

    def wait_for_loader_gone(self, loader_locator: tuple, timeout: int = 30):
        """Wait for loading indicator to disappear."""
        wait_for_element_absent(self.driver, loader_locator, timeout=timeout)

    # ─── App Navigation ──────────────────────────────────────────────

    def press_back(self):
        """Press device back button."""
        self.driver.back()

    def hide_keyboard(self):
        """Hide soft keyboard if visible."""
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass

    def get_toast_message(self) -> str:
        """Get Android toast message text (UiAutomator2)."""
        try:
            toast = self.driver.find_element(
                By.XPATH, "//android.widget.Toast"
            )
            return toast.text
        except NoSuchElementException:
            return ""
