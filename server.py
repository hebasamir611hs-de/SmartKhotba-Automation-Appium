from fastmcp import FastMCP
import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import create_driver
from utils.mobile_actions import MobileActions
from core.api_testing import APITesting
from core.performance_testing import PerformanceTesting
from core.security_testing import SecurityTesting
from utils.logger import get_logger

# Load environment
load_dotenv()

# Initialize MCP
mcp = FastMCP("SmartKhotba Mobile AI")
logger = get_logger("MCP_Server")

class SmartKhotbaServer:
    """Enterprise-grade MCP Server for SmartKhotba Mobile Automation."""
    _init_lock = threading.Lock()

    def __init__(self):
        self.driver = None
        self.actions = None
        self.api = APITesting()
        self.perf = None
        self.sec = None

    def _ensure_driver(self):
        with self._init_lock:
            if not self.driver:
                logger.info("🚀 Initializing Appium Driver for SmartKhotba...")
                self.driver = create_driver()
                self.actions = MobileActions(self.driver)
                self.perf = PerformanceTesting(self.driver)
                self.sec = SecurityTesting(self.driver)
                logger.info("✅ Driver initialized successfully.")
            return self.driver

    def _is_alive(self) -> bool:
        if not self.driver:
            return False
        try:
            _ = self.driver.session_id
            self.driver.get_window_size()
            return True
        except Exception:
            return False

    def quit(self):
        with self._init_lock:
            if self.driver:
                try:
                    self.driver.quit()
                except Exception as e:
                    logger.warning(f"Driver quit error (ignored): {e}")
            self.driver = None
            self.actions = None
            self.perf = None
            self.sec = None

# Singleton instance
server_instance = SmartKhotbaServer()

@mcp.tool()
def click_element(selector: str, strategy: str = "id"):
    """
    Clicks a mobile element.
    - strategy: id, xpath, accessibility_id, class_name, android_uiautomator
    - selector: The locator string
    """
    server_instance._ensure_driver()
    server_instance.actions.click_element(selector, strategy)
    return f"Successfully clicked element [{strategy}={selector}]"

@mcp.tool()
def input_text(selector: str, text: str, strategy: str = "id"):
    """
    Inputs text into a mobile element.
    - selector: The locator string
    - text: The text to input
    - strategy: id, xpath, etc.
    """
    server_instance._ensure_driver()
    server_instance.actions.input_text(selector, text, strategy)
    return f"Successfully typed '{text}' into [{strategy}={selector}]"

@mcp.tool()
def capture_screen(filename: str = "mcp_capture.png"):
    """
    Captures a high-resolution screenshot from the active device.
    """
    server_instance._ensure_driver()
    path = server_instance.actions.capture_screen(filename)
    return f"Screenshot captured: {path}"

@mcp.tool()
def verify_api_endpoint(endpoint: str):
    """
    [Architectural Placeholder] Verifies backend API status.
    """
    return server_instance.api.verify_endpoint(endpoint)

@mcp.tool()
def get_performance_report():
    """
    [Architectural Placeholder] Retrieves mobile performance metrics (CPU/RAM).
    """
    server_instance._ensure_driver()
    return server_instance.perf.get_metrics()

@mcp.tool()
def run_security_audit():
    """
    [Architectural Placeholder] Runs a security scan on the current app state.
    """
    server_instance._ensure_driver()
    return server_instance.sec.scan_vulnerabilities()

@mcp.tool()
def get_toast_text():
    """Retrieves the current toast message text."""
    server_instance._ensure_driver()
    text = server_instance.actions.base_page.get_toast_message()
    return f"Toast message: {text}" if text else "No toast message found."

PROJECT_ROOT = Path(__file__).parent


@mcp.tool()
def run_smoke_tests() -> dict:
    """Run the smoke test suite and return pass/fail summary."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_smoke.py", "-v", "--tb=short", "-q"],
        capture_output=True,
        text=True,
        cwd=str(PROJECT_ROOT),
    )
    return {
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout[-3000:],
        "stderr": result.stderr[-1000:],
    }


@mcp.tool()
def run_tests(marker: str = "", test_file: str = "") -> dict:
    """Run tests with optional pytest marker or specific file."""
    cmd = [sys.executable, "-m", "pytest", "-v", "--tb=short"]
    if marker:
        cmd += ["-m", marker]
    if test_file:
        cmd.append(test_file)
    else:
        cmd.append("tests/")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(PROJECT_ROOT))
    return {
        "exit_code": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-1000:],
    }


@mcp.tool()
def get_drift_report() -> dict:
    """Get locator healing metrics — shows config drift and fragile locators."""
    metrics_path = PROJECT_ROOT / "data" / "healing_metrics.json"
    if not metrics_path.exists():
        return {"events": [], "summary": "No healing events recorded yet."}

    with open(metrics_path) as f:
        events = json.load(f)

    healed = [e for e in events if e.get("status") == "HEALED"]
    failed = [e for e in events if e.get("status") == "FAILED"]

    drift_by_page = {}
    for e in events:
        page = e.get("page", "Unknown")
        drift_by_page.setdefault(page, {"healed": 0, "failed": 0})
        drift_by_page[page][e["status"].lower()] += 1

    return {
        "total_events": len(events),
        "healed_count": len(healed),
        "failed_count": len(failed),
        "heal_rate": f"{len(healed) / len(events) * 100:.1f}%" if events else "N/A",
        "drift_by_page": drift_by_page,
        "recent_failures": failed[-5:],
    }


@mcp.tool()
def get_framework_status() -> dict:
    """Health check — verify APK exists, env configured, dependencies met."""
    apk_path = PROJECT_ROOT / "apps" / "smartkhotba.apk"
    env_path = PROJECT_ROOT / ".env"
    venv_path = PROJECT_ROOT / ".venv"
    return {
        "apk_present": apk_path.exists(),
        "apk_size_mb": f"{apk_path.stat().st_size / 1024 / 1024:.1f}" if apk_path.exists() else None,
        "env_configured": env_path.exists(),
        "venv_exists": venv_path.exists(),
        "project_root": str(PROJECT_ROOT),
    }


@mcp.tool()
def driver_status() -> dict:
    """Check Appium session liveness."""
    return {
        "initialized": server_instance.driver is not None,
        "alive": server_instance._is_alive(),
    }


@mcp.tool()
def reset_session() -> dict:
    """Quit current driver and reinitialize on next call."""
    server_instance.quit()
    return {"status": "session_terminated", "note": "Next tool call will spawn a fresh driver."}


@mcp.tool()
def ensure_driver_alive() -> dict:
    """Reconnect if session died."""
    if not server_instance._is_alive():
        server_instance.quit()
        server_instance._ensure_driver()
        return {"status": "reconnected"}
    return {"status": "healthy"}


if __name__ == "__main__":
    logger.info("Starting SmartKhotba Python MCP Server...")
    mcp.run()
