"""
Environment Configuration
Centralized settings for all environments (local, CI, device).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
APPS_DIR = PROJECT_ROOT / "apps"
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
DATA_DIR = PROJECT_ROOT / "data"

# Appium Server
APPIUM_HOST = os.getenv("APPIUM_HOST", "http://127.0.0.1")
APPIUM_PORT = int(os.getenv("APPIUM_PORT", "4723"))
APPIUM_URL = f"{APPIUM_HOST}:{APPIUM_PORT}"

# Timeouts (seconds)
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
COMMAND_TIMEOUT = int(os.getenv("COMMAND_TIMEOUT", "300"))

# Environment
ENVIRONMENT = os.getenv("TEST_ENV", "android_emulator")  # android_emulator | android_real_device | ci_headless
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# App Settings
APP_PACKAGE = os.getenv("APP_PACKAGE", "")
APP_ACTIVITY = os.getenv("APP_ACTIVITY", "")

# Azure DevOps (for test result linking)
AZURE_ORG_URL = os.getenv("AZURE_ORG_URL", "")
AZURE_PROJECT = os.getenv("AZURE_PROJECT", "")
AZURE_PAT = os.getenv("AZURE_PAT", "")

# Screenshots
SCREENSHOT_ON_FAILURE = True
SCREENSHOT_ON_PASS = False
