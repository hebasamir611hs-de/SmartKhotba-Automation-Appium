"""
Screenshot Helper — Capture and organize failure screenshots.
"""
import os
from datetime import datetime
from pathlib import Path
from appium.webdriver.webdriver import WebDriver
from config.env_config import SCREENSHOTS_DIR
from utils.logger import get_logger

logger = get_logger(__name__)


def take_screenshot(driver: WebDriver, test_name: str, suffix: str = "failure") -> str:
    """Capture screenshot and save to reports/screenshots/.
    
    Args:
        driver: Appium WebDriver
        test_name: Name of the test (used in filename)
        suffix: Screenshot category (failure, step, debug)
    
    Returns:
        Path to saved screenshot
    """
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{suffix}_{timestamp}.png"
    filepath = SCREENSHOTS_DIR / filename
    
    try:
        driver.save_screenshot(str(filepath))
        logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        return ""
