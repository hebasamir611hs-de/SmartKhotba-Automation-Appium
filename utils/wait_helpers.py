"""
Wait Helpers — Explicit wait wrappers for mobile elements.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.webdriver.webdriver import WebDriver
from config.env_config import EXPLICIT_WAIT
from utils.logger import get_logger

logger = get_logger(__name__)


def wait_for_element(driver: WebDriver, locator: tuple, timeout: int = None):
    """Wait for element to be visible and return it.
    
    Args:
        driver: Appium WebDriver
        locator: Tuple of (By, value)
        timeout: Override default timeout
    
    Returns:
        WebElement when found
        
    Raises:
        TimeoutException if element not found within timeout
    """
    timeout = timeout or EXPLICIT_WAIT
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        return element
    except TimeoutException:
        logger.error(f"Element not found: {locator} after {timeout}s")
        raise


def wait_for_element_clickable(driver: WebDriver, locator: tuple, timeout: int = None):
    """Wait for element to be clickable and return it."""
    timeout = timeout or EXPLICIT_WAIT
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        return element
    except TimeoutException:
        logger.error(f"Element not clickable: {locator} after {timeout}s")
        raise


def wait_for_element_absent(driver: WebDriver, locator: tuple, timeout: int = None) -> bool:
    """Wait for element to disappear (useful for loaders/spinners)."""
    timeout = timeout or EXPLICIT_WAIT
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        return True
    except TimeoutException:
        logger.warning(f"Element still present: {locator} after {timeout}s")
        return False


def wait_for_text_present(driver: WebDriver, locator: tuple, text: str, timeout: int = None):
    """Wait for specific text to appear in element."""
    timeout = timeout or EXPLICIT_WAIT
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    except TimeoutException:
        logger.error(f"Text '{text}' not found in {locator} after {timeout}s")
        raise
