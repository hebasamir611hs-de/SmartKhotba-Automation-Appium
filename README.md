# SmartKhotba Mobile Automation

Appium-based test automation for the SmartKhotba Android app (`com.islam.khutba.qa`).

## Prerequisites

- **Python 3.11+** with `pip`
- **Appium 3.x** (`npm install -g appium`)
- **UiAutomator2 driver** (`appium driver install uiautomator2`)
- **Android SDK** with `adb` (via Android Studio or standalone SDK)
- **Real device** with USB debugging enabled, OR an Android emulator

## Setup

```bash
# 1. Clone and install dependencies
cd smartkhotba-mobile-automation
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env — set DEVICE_UDID, PLATFORM_VERSION, TEST_ENV
```

## Environment Selection

Set `TEST_ENV` in `.env` or as an environment variable:

| Value | Use case |
|-------|----------|
| `android_real_device` | Real phone via USB (default in `.env`) |
| `android_emulator` | Local emulator (requires APK in `apps/`) |
| `ci_headless` | CI pipeline with headless emulator |

`DEVICE_UDID` and `PLATFORM_VERSION` override `capabilities.json` defaults, so the config works for any device.

## APK

The APK is gitignored (`apps/*.apk`). For real device testing, install the APK manually:

```bash
adb install path/to/smartkhotba.apk
```

For emulator/CI, place the APK at `apps/smartkhotba.apk`. The framework will fail with a clear error if the APK is missing.

## Running Tests

```bash
# Start Appium server
appium

# Run smoke tests (4 critical-path tests)
pytest tests/test_smoke.py -m smoke

# Run structural acceptance tests (no device needed)
pytest tests/test_step1_acceptance.py

# Run full regression
pytest

# Run with Allure report
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Project Structure

```
config/          — capabilities.json, env_config.py
pages/           — Page Object Model (13 pages)
tests/           — pytest test suites
utils/           — driver factory, wait helpers, locator healing
core/            — metrics tracker
data/            — locator registry, test data
scripts/         — device setup, app data clearing
```

## Reset Strategy

- `noReset=true` by default — app state persists between tests (fast).
- For state-dependent tests, use the `clear_app_state` fixture to run `adb shell pm clear` before the test.
- Smoke tests do not depend on state and run reliably in any order.

## Allure Reports

```bash
allure serve reports/allure-results
```
