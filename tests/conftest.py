"""
conftest.py — Global pytest fixtures and hooks.
"""
import os
import subprocess
import pytest
from utils.driver_factory import create_driver
from utils.screenshot_helper import take_screenshot
from utils.logger import get_logger

logger = get_logger(__name__)

APP_PACKAGE = "com.islam.khutba.qa"


# ─── Hook: Store test result for screenshot-on-failure ────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available in fixtures via request.node.rep_call."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ─── Fixture: Per-test driver (isolated, each test gets a fresh session) ───
@pytest.fixture
def driver():
    """Function-scoped Appium driver for standalone tests not using BaseTest."""
    d = create_driver()
    yield d
    if d:
        d.quit()


# ─── Fixture: Screenshot on demand ───────────────────────────────
@pytest.fixture
def screenshot(driver, request):
    """Fixture to take a screenshot at any point during test."""
    def _capture(suffix="step"):
        return take_screenshot(driver, request.node.name, suffix)
    return _capture


# ─── Fixture: Clear app data for state-dependent tests ───────────
@pytest.fixture
def clear_app_state():
    """Clear app data via adb pm clear. Use for tests that need clean state."""
    android_home = os.environ.get("ANDROID_HOME", "")
    adb = os.path.join(android_home, "platform-tools", "adb.exe") if android_home else "adb"
    subprocess.run([adb, "shell", "pm", "clear", APP_PACKAGE],
                   capture_output=True, timeout=10)
    logger.info(f"App data cleared for {APP_PACKAGE}")


# ─── Session Setup Logging ────────────────────────────────────────
def pytest_configure(config):
    """Log test session start."""
    logger.info("═" * 60)
    logger.info("SmartKhotba Mobile Automation — Test Session Starting")
    logger.info("═" * 60)


def pytest_collection_modifyitems(items):
    """Auto-add reruns for smoke tests only."""
    for item in items:
        if "smoke" in [m.name for m in item.iter_markers()]:
            item.add_marker(pytest.mark.flaky(reruns=2, reruns_delay=5))


def pytest_unconfigure(config):
    """Log test session end + healing metrics summary."""
    import json
    from pathlib import Path
    metrics_path = Path(__file__).parent.parent / "data" / "healing_metrics.json"
    if metrics_path.exists():
        try:
            data = json.loads(metrics_path.read_text(encoding="utf-8"))
            healed = sum(1 for e in data if e.get("status") == "HEALED")
            failed = sum(1 for e in data if e.get("status") == "FAILED")
            logger.info(f"Healing metrics: {healed} healed, {failed} failed ({len(data)} total events)")
        except Exception:
            pass
    logger.info("═" * 60)
    logger.info("Test Session Complete")
    logger.info("═" * 60)
