"""
MobileActions - Core interaction layer for the MCP server.
Provides a clean API for mobile operations, abstracting driver complexity.
"""
from pages.base_page import BasePage
from utils.logger import get_logger
from appium.webdriver.common.appiumby import AppiumBy as By

logger = get_logger(__name__)

class MobileActions:
    def __init__(self, driver):
        self.driver = driver
        self.base_page = BasePage(driver)

    def click_element(self, selector: str, strategy: str = "id"):
        """Clicks an element using the specified strategy and selector."""
        locator = self._build_locator(strategy, selector)
        logger.info(f"Clicking element: {locator}")
        self.base_page.click(locator)

    def input_text(self, selector: str, text: str, strategy: str = "id"):
        """Inputs text into an element."""
        locator = self._build_locator(strategy, selector)
        logger.info(f"Typing '{text}' into {locator}")
        self.base_page.type_text(locator, text)

    def capture_screen(self, filename: str = "screenshot.png"):
        """Captures a screenshot of the current screen."""
        from config.env_config import REPORTS_DIR
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        path = str(REPORTS_DIR / filename)
        self.driver.save_screenshot(path)
        logger.info(f"Screenshot saved to {path}")
        return path

    def get_element_text(self, selector: str, strategy: str = "id"):
        """Gets text from an element."""
        locator = self._build_locator(strategy, selector)
        return self.base_page.get_text(locator)

    def _build_locator(self, strategy: str, selector: str):
        strategies = {
            "id": By.ID,
            "xpath": By.XPATH,
            "accessibility_id": By.ACCESSIBILITY_ID,
            "class_name": By.CLASS_NAME,
            "android_uiautomator": By.ANDROID_UIAUTOMATOR
        }
        if strategy not in strategies:
            raise ValueError(f"Unsupported strategy: {strategy}")
        return (strategies[strategy], selector)
