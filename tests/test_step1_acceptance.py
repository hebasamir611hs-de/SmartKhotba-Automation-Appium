"""
Step 1 Acceptance Gate — Architectural invariants that must hold.
Run with: pytest tests/test_step1_acceptance.py -v
No Appium server or device needed.
"""
import json
import re
import importlib
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

PAGE_MODULES = [
    "pages.splash_page", "pages.language_page",
    "pages.onboarding_page", "pages.otp_page", "pages.home_page",
    "pages.main_page", "pages.khotba_page", "pages.concepts_page",
    "pages.reminders_page", "pages.favorites_page", "pages.settings_page",
    "pages.video_player_page", "pages.location_page",
]


# ─── A: All pages declare PAGE_NAME ─────────────────────────────────

@pytest.mark.parametrize("module_path", PAGE_MODULES)
def test_page_declares_page_name(module_path):
    mod = importlib.import_module(module_path)
    page_classes = [
        obj for _, obj in vars(mod).items()
        if isinstance(obj, type) and hasattr(obj, "PAGE_NAME")
    ]
    assert page_classes, f"{module_path} has no class with PAGE_NAME"
    for cls in page_classes:
        assert cls.PAGE_NAME.endswith("_page"), \
            f"{cls.__name__}.PAGE_NAME = '{cls.PAGE_NAME}' must end with '_page'"


# ─── B: PAGE_NAME matches LOCATOR_REGISTRY keys ─────────────────────

def test_page_names_exist_in_registry():
    from data.locators import LOCATOR_REGISTRY
    registry_keys = set(LOCATOR_REGISTRY.keys())
    missing = []
    for module_path in PAGE_MODULES:
        mod = importlib.import_module(module_path)
        for _, obj in vars(mod).items():
            if isinstance(obj, type) and hasattr(obj, "PAGE_NAME"):
                if obj.PAGE_NAME not in registry_keys:
                    missing.append(f"{obj.__name__}.PAGE_NAME='{obj.PAGE_NAME}'")
    assert not missing, f"PAGE_NAMEs missing from LOCATOR_REGISTRY: {missing}"


# ─── C: No empty registry entries ───────────────────────────────────

def test_registry_no_empty_entries():
    from data.locators import LOCATOR_REGISTRY
    empty = [k for k, v in LOCATOR_REGISTRY.items() if not v]
    assert not empty, f"Empty registry entries: {empty}"


# ─── D: No noReset/fullReset contradiction ───────────────────────────

def test_capabilities_no_reset_contradiction():
    caps = json.loads((ROOT / "config" / "capabilities.json").read_text())
    for env, c in caps.items():
        if c.get("appium:noReset") is True:
            assert c.get("appium:fullReset") is not True, \
                f"{env}: noReset=true + fullReset=true is contradictory"


# ─── E: Package name consistent everywhere ──────────────────────────

EXPECTED_PACKAGE = "com.islam.khutba.qa"


def test_capabilities_use_correct_package():
    caps = json.loads((ROOT / "config" / "capabilities.json").read_text())
    for env, c in caps.items():
        assert c.get("appium:appPackage") == EXPECTED_PACKAGE, \
            f"{env} has wrong appPackage"


def test_locators_use_correct_package():
    from data.locators import LOCATOR_REGISTRY
    wrong = []
    for page, elements in LOCATOR_REGISTRY.items():
        for elem, entry in elements.items():
            primary = entry.get("primary", ())
            if len(primary) == 2 and ":id/" in str(primary[1]):
                if EXPECTED_PACKAGE not in str(primary[1]):
                    wrong.append(f"{page}.{elem}")
    assert not wrong, f"Wrong package in locators: {wrong}"


# ─── F: MetricsTracker is thread-safe ───────────────────────────────

def test_metrics_tracker_absolute_path():
    from core.metrics_tracker import _DEFAULT_METRICS
    assert _DEFAULT_METRICS.is_absolute()


def test_metrics_tracker_has_lock():
    import core.metrics_tracker as mt
    assert hasattr(mt, "_LOCK")
    assert isinstance(mt._LOCK, type(threading.Lock()))


def test_metrics_tracker_concurrent_writes():
    from core.metrics_tracker import MetricsTracker
    t = MetricsTracker()
    threads = [
        threading.Thread(target=t.log_failure_event, args=("_test", f"e{i}", ("id", "x")))
        for i in range(20)
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    data = json.loads((ROOT / "data" / "healing_metrics.json").read_text())
    test_events = [e for e in data if e.get("page") == "_test"]
    assert len(test_events) == 20, f"Expected 20 events, got {len(test_events)}"
    # Cleanup
    clean = [e for e in data if e.get("page") != "_test"]
    (ROOT / "data" / "healing_metrics.json").write_text(
        json.dumps(clean, indent=2), encoding="utf-8"
    )


# ─── G: Server exposes lifecycle tools + concurrency lock ────────────

def test_server_lifecycle_tools():
    import server
    for tool in ["driver_status", "reset_session", "ensure_driver_alive"]:
        assert hasattr(server, tool), f"Missing MCP tool: {tool}"


def test_server_has_init_lock():
    import server
    assert hasattr(server.SmartKhotbaServer, "_init_lock")


# ─── H: No bare except: in source ───────────────────────────────────

def test_no_bare_except():
    bare_re = re.compile(r"^\s*except\s*:", re.MULTILINE)
    violations = []
    for f in ROOT.rglob("*.py"):
        if ".venv" in str(f) or "__pycache__" in str(f):
            continue
        content = f.read_text(encoding="utf-8", errors="ignore")
        if bare_re.search(content):
            violations.append(str(f.relative_to(ROOT)))
    assert not violations, f"Bare 'except:' in: {violations}"


# ─── I: All core modules import cleanly ──────────────────────────────

CORE_MODULES = [
    "config.env_config", "utils.logger", "utils.wait_helpers",
    "utils.screenshot_helper", "utils.test_data", "utils.driver_factory",
    "utils.locator_healing", "utils.mobile_actions",
    "core.metrics_tracker", "data.locators",
    "pages.base_page", "tests.helpers",
]


@pytest.mark.parametrize("module_path", CORE_MODULES)
def test_module_imports(module_path):
    importlib.import_module(module_path)


# ─── J: Core infrastructure files exist ──────────────────────────────

def test_core_files_exist():
    required = [
        "config/capabilities.json",
        "config/env_config.py",
        "data/locators.py",
        "core/metrics_tracker.py",
        "server.py",
        "pytest.ini",
        "requirements.txt",
        ".gitignore",
    ]
    missing = [f for f in required if not (ROOT / f).exists()]
    assert not missing, f"Missing files: {missing}"