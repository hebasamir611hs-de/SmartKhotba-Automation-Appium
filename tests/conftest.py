"""
conftest.py — Global pytest fixtures and hooks.
"""
import pytest
from utils.driver_factory import create_driver
from utils.screenshot_helper import take_screenshot
from utils.logger import get_logger

logger = get_logger(__name__)


# ─── Hook: Store test result for screenshot-on-failure ────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test result available in fixtures via request.node.rep_call."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ─── Fixture: Shared driver via server singleton (consistent with MCP lifecycle) ───
@pytest.fixture(scope="session")
def driver():
    """Session-scoped Appium driver — mirrors MCP server singleton behavior."""
    from server import server_instance
    server_instance._ensure_driver()
    yield server_instance.driver
    server_instance.quit()


# ─── Fixture: Screenshot on demand ───────────────────────────────
@pytest.fixture
def screenshot(driver, request):
    """Fixture to take a screenshot at any point during test."""
    def _capture(suffix="step"):
        return take_screenshot(driver, request.node.name, suffix)
    return _capture


# ─── Session Setup Logging ────────────────────────────────────────
def pytest_configure(config):
    """Log test session start."""
    logger.info("═" * 60)
    logger.info("SmartKhotba Mobile Automation — Test Session Starting")
    logger.info("═" * 60)


def pytest_unconfigure(config):
    """Log test session end."""
    logger.info("═" * 60)
    logger.info("Test Session Complete")
    logger.info("═" * 60)
