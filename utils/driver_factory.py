"""
Driver Factory — Single responsibility: create and configure Appium driver.
"""
import json
import os
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.env_config import (
    APPIUM_URL, ENVIRONMENT, PROJECT_ROOT,
    APP_PACKAGE, APP_ACTIVITY, IMPLICIT_WAIT
)
from utils.logger import get_logger

logger = get_logger(__name__)


def _resolve_app_path(caps: dict) -> dict:
    """Convert relative appium:app paths to absolute, validate existence."""
    app_path = caps.get("appium:app")
    if not app_path:
        return caps

    from pathlib import Path
    p = Path(app_path)
    if not p.is_absolute():
        p = PROJECT_ROOT / p

    if not p.exists():
        raise FileNotFoundError(
            f"APK not found at {p}. Place the APK in apps/ or set appium:app "
            f"to a valid path. The APK is gitignored — see README for how to obtain it."
        )

    caps["appium:app"] = str(p)
    return caps


def create_driver(env_override: str = None) -> webdriver.Remote:
    """Create Appium driver from capabilities config."""
    env = env_override or ENVIRONMENT
    caps_path = PROJECT_ROOT / "config" / "capabilities.json"

    with open(caps_path) as f:
        all_caps = json.load(f)

    if env not in all_caps:
        raise ValueError(f"Unknown environment '{env}'. Available: {list(all_caps.keys())}")

    caps = all_caps[env]

    # Override device identity from env vars (avoids hardcoding a single device)
    if os.getenv("DEVICE_UDID"):
        caps["appium:udid"] = os.getenv("DEVICE_UDID")
    if os.getenv("PLATFORM_VERSION"):
        caps["appium:platformVersion"] = os.getenv("PLATFORM_VERSION")

    if not caps.get("appium:appPackage") and APP_PACKAGE:
        caps["appium:appPackage"] = APP_PACKAGE
    if not caps.get("appium:appActivity") and APP_ACTIVITY:
        caps["appium:appActivity"] = APP_ACTIVITY

    caps = _resolve_app_path(caps)

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
