"""
Driver Factory — Single responsibility: create and configure Appium driver.
"""
import json
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.env_config import (
    APPIUM_URL, ENVIRONMENT, PROJECT_ROOT,
    APP_PACKAGE, APP_ACTIVITY, IMPLICIT_WAIT
)
from utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(env_override: str = None) -> webdriver.Remote:
    """Create Appium driver from capabilities config.

    Args:
        env_override: Override ENVIRONMENT setting (e.g., 'ci_headless')

    Returns:
        Configured Appium WebDriver instance
    """
    env = env_override or ENVIRONMENT
    caps_path = PROJECT_ROOT / "config" / "capabilities.json"

    with open(caps_path) as f:
        all_caps = json.load(f)

    if env not in all_caps:
        raise ValueError(f"Unknown environment '{env}'. Available: {list(all_caps.keys())}")

    caps = all_caps[env]

    # Override empty appPackage/appActivity from env vars
    if not caps.get("appium:appPackage") and APP_PACKAGE:
        caps["appium:appPackage"] = APP_PACKAGE
    if not caps.get("appium:appActivity") and APP_ACTIVITY:
        caps["appium:appActivity"] = APP_ACTIVITY

    options = UiAutomator2Options()

    for key, value in caps.items():
        if key == "platformName":
            options.platform_name = value
        else:
            options.set_capability(key, value)

    logger.info(f"Creating driver — env: {env}, server: {APPIUM_URL}")

    driver = webdriver.Remote(
        command_executor=APPIUM_URL,
        options=options
    )

    driver.implicitly_wait(IMPLICIT_WAIT)

    return driver
