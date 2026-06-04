"""
BaseTest — Common test lifecycle: driver setup, teardown, screenshot on failure.
All test classes inherit from this.
"""
import pytest
from utils.driver_factory import create_driver
from utils.screenshot_helper import take_screenshot
from utils.logger import get_logger
from config.env_config import APP_PACKAGE

logger = get_logger(__name__)

APP_PACKAGE_DEFAULT = "com.islam.khutba.qa"


class BaseTest:
    """Base class for all test classes. Provides driver lifecycle management."""

    driver = None

    @pytest.fixture(autouse=True)
    def setup_teardown(self, request):
        """Setup driver before test, teardown after."""
        logger.info(f"▶ Starting: {request.node.name}")
        self.driver = create_driver()

        package = APP_PACKAGE or APP_PACKAGE_DEFAULT
        try:
            self.driver.terminate_app(package)
            self.driver.activate_app(package)
            logger.info("App restarted from splash via terminate/activate")
        except Exception as e:
            logger.warning(f"App restart failed (non-fatal): {e}")

        yield
        
        # Screenshot on failure (hasattr guard — rep_call may not exist if setup itself fails)
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            take_screenshot(self.driver, request.node.name, suffix="failure")
            logger.error(f"✖ FAILED: {request.node.name}")
        elif hasattr(request.node, "rep_call"):
            logger.info(f"✔ PASSED: {request.node.name}")
        else:
            logger.warning(f"⚠ UNKNOWN: {request.node.name} — no result captured")
        
        # Teardown
        if self.driver:
            self.driver.quit()
            logger.debug("Driver quit")
