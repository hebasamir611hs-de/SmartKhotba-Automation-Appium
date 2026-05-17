# SmartKhotba Mobile Automation — Build Log

> **Date:** May 11, 2026
> **Project:** SmartKhotba Android Automation Framework
> **Methodology:** 4-Role Review (Senior → Manager → PM → Stakeholder)
> **Reference:** Appium_MCP_Strategy_SmartKhotba.md

---

## Approach Agreement

### Multi-Role Review Process

| Role | المسؤولية |
|---|---|
| **Role 1: QA Automation Senior & MCP Expert** | يبني ويعمل implementation |
| **Role 2: QA Automation Manager & MCP Expert** | يراجع شغل الـ Senior — ملاحظات، تحسينات، حاجات ناقصة |
| **Role 3: Project Manager** | يبص على الصورة الكبيرة — هل ده مناسب وكامل؟ |
| **Role 4: Stakeholder** | يشوف الـ deliverable من برة — هل ده اللي كان متوقعه؟ |

### Execution Plan

| Step | المحتوى | محتاج inputs؟ | Status |
|---|---|---|---|
| 1 | Project structure + folder architecture | ❌ | ✅ Done + Reviewed |
| 2 | Config system (capabilities template) | ❌ | ✅ Done + Reviewed |
| 3 | Base classes (BasePage, BaseTest) | ❌ | ✅ Done + Reviewed |
| 4 | MCP server setup + connection | ❌ | ✅ Done + Reviewed |
| 5 | SmartKhotba Page Objects | ✅ APK provided | ✅ Done + Reviewed |
| 6 | Actual test cases | ✅ Full coverage | ✅ Done + Reviewed |
| 7 | Azure DevOps linking | ✅ محتاج test environment | ⬜ Blocked |

---

## Clarification: Two Things Being Built

| | **Appium Python Framework** | **Appium MCP Server** |
|---|---|---|
| **What** | Python code running tests | AI agent controlling Appium via MCP |
| **When** | Automatically in CI/CD every release | Interactively when you ask Claude |
| **Output** | Test results (pass/fail) | Live actions / generated code |
| **Reliability** | Deterministic, repeatable | Intent-based, may vary |
| **Role** | Regression suite (Phase 1 — foundation) | Test accelerator (Phase 3 — enhancement) |

> **MCP server = accelerator, not runner.** Without the Python framework, MCP generates code into a vacuum.

---

## Step 1: Project Structure + Folder Architecture

### Status: ✅ Built → ✅ Manager Reviewed → ✅ Fixes Applied

---

### Role 1: Senior — Deliverables

#### Project Structure

```
smartkhotba-mobile-automation/
│
├── config/
│   ├── capabilities.json          # Android desired capabilities (3 environments)
│   ├── env_config.py              # Environment settings (URLs, timeouts, paths)
│   └── .env.example               # Template for developers
│
├── pages/                          # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # BasePage — shared actions (click, type, wait, swipe)
│   ├── login_page.py              # [placeholder — needs APK]
│   └── home_page.py               # [placeholder — needs APK]
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # pytest fixtures (driver setup/teardown, screenshots)
│   ├── base_test.py               # BaseTest class
│   ├── test_login.py              # [placeholder — needs scenarios]
│   └── test_smoke.py              # [placeholder — needs scenarios]
│
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py          # Appium driver initialization
│   ├── logger.py                  # Custom colorized logging
│   ├── screenshot_helper.py       # Screenshot on failure
│   ├── wait_helpers.py            # Explicit wait wrappers
│   └── test_data.py               # Shared test data loader (JSON/CSV from data/)
│
├── data/                           # Test data files (JSON/CSV)
│   └── credentials.json           # Login test data by user type
│
├── scripts/                        # Utility scripts
│   ├── setup_device.sh            # Device/emulator setup
│   ├── install_apk.sh             # APK installation
│   └── clear_app_data.sh          # Clear app data before runs
│
├── reports/                        # Allure / HTML reports output
│   └── .gitkeep
│
├── apps/                           # APK storage
│   └── .gitkeep
│
├── mcp/
│   ├── mcp_server_config.json     # Appium MCP server setup
│   └── playwright_mcp_config.json # Playwright MCP server setup
│
├── pytest.ini                      # pytest configuration
├── requirements.txt                # Python dependencies
├── .gitignore
└── BUILD_LOG.md
```

---

### Role 2: Manager — Review Notes (Step 1)

| # | الملاحظة | الحالة | القرار |
|---|---|---|---|
| 1 | مفيش `data/` folder | ✅ Applied | Added `data/` + `credentials.json` |
| 2 | مفيش `scripts/` folder | ✅ Applied | Added 3 utility scripts |
| 3 | `.gitignore` بيتجاهل كل APKs | ⏳ Deferred | No APK yet — solve when input arrives |

---

## Step 2: Config System

### Status: ✅ Built → ✅ Manager Reviewed

---

### Role 1: Senior — Deliverables

#### Files Created

| File | Purpose |
|---|---|
| `config/capabilities.json` | 3 environment profiles: `android_emulator`, `android_real_device`, `ci_headless` |
| `config/env_config.py` | Centralized settings — Appium URL, timeouts, paths, Azure DevOps |
| `.env.example` | Template with all env vars documented |

#### Design Decisions

| Decision | Rationale |
|---|---|
| 3 capability profiles | Covers dev (emulator), QA (device), CI (headless) without code changes |
| `env_config.py` over YAML | Python native, no parser dependency, auto-loads `.env` via dotenv |
| APP_PACKAGE/APP_ACTIVITY in .env | Decoupled from capabilities — same caps file works across apps |

### Role 2: Manager — Review Notes (Step 2)

No issues found. Config system is clean and environment-agnostic.

---

## Step 3: Base Classes

### Status: ✅ Built → ✅ Manager Reviewed → ✅ Bugs Fixed

---

### Role 1: Senior — Deliverables

| File | Content |
|---|---|
| `pages/base_page.py` | BasePage — click, type, wait, swipe, scroll, toast, keyboard handling |
| `tests/base_test.py` | BaseTest — driver lifecycle, screenshot-on-failure, pass/fail logging |
| `tests/conftest.py` | Global fixtures, hooks, standalone driver fixture |
| `utils/driver_factory.py` | Appium driver creation from capabilities.json |
| `utils/logger.py` | Colorized logger with configurable level |
| `utils/wait_helpers.py` | Explicit wait wrappers (visible, clickable, absent, text) |
| `utils/screenshot_helper.py` | Screenshot capture with timestamped filenames |
| `utils/test_data.py` | JSON test data loader from `data/` directory |
| `pages/login_page.py` | LoginPage placeholder (needs APK for locators) |
| `pages/home_page.py` | HomePage placeholder (needs APK for locators) |
| `tests/test_smoke.py` | Smoke test placeholder |
| `tests/test_login.py` | Login test placeholder with 4 scenarios |

### Role 2: Manager — Review Notes (Step 3)

**3 bugs found and fixed:**

| # | Bug | Severity | Fix |
|---|---|---|---|
| 1 | `driver_factory.py` — dead variable `attr_name` assigned but never used | Low | Removed dead code path, simplified capability setting |
| 2 | `driver_factory.py` — empty `appPackage`/`appActivity` in capabilities.json never overridden from env vars | High | Added env var override logic: if caps empty + env var set → merge |
| 3 | `base_test.py` — `request.node.rep_call` would `AttributeError` if setup itself fails | Medium | Added `hasattr()` guard with 3-state logging (pass/fail/unknown) |

**1 improvement applied:**

| # | Improvement | Details |
|---|---|---|
| 1 | `driver_factory.py` — no logging | Added `logger.info` for driver creation, added `implicit_wait` from config |

---

## Step 4: MCP Server Setup

### Status: ✅ Built → ✅ Manager Reviewed

---

### Role 1: Senior — Deliverables

| File | Purpose |
|---|---|
| `mcp/mcp_server_config.json` | Appium MCP config for AI-assisted test generation |
| `mcp/playwright_mcp_config.json` | Playwright MCP for web companion tests |

#### Design Decisions

| Decision | Rationale |
|---|---|
| MCP configs isolated in `mcp/` | Don't pollute core framework |
| Usage notes embedded in JSON | Self-documenting — new team members understand purpose immediately |
| Shared `test_data.py` reference | Same data layer powers both mobile and web test suites |

### Role 2: Manager — Review Notes (Step 4)

No issues found. MCP configs are properly scoped as Phase 3 accelerator, not Phase 1 dependency.

---

## Step 5: SmartKhotba Page Objects

### Status: ✅ Built → ✅ Manager Reviewed

---

### APK Analysis

| Field | Value |
|---|---|
| **Package** | `com.islam.khutba.qa` |
| **Version** | 1.1.0 (code: 4) |
| **Launcher** | `com.dev.smartkhotba.prsentation.splash.SplashActivity` |
| **Framework** | Kotlin Native (not Flutter/RN) |
| **Encryption** | SQLCipher (encrypted local DB) |

### Activities Discovered

| Activity | Screen |
|---|---|
| `SplashActivity` | Splash / Launch |
| `LanguageActivity` | Language selection |
| `LocationActivity` | Location permission |
| `InfoPagesActivity` | Onboarding pages |
| `VerifyOtpNumber` | OTP verification |
| `MainActivity` | Main screen (hosts all fragments) |
| `VideoPlayerActivity` | Live stream / video player |

### Page Objects Created (13 screens)

| Page Object | Screen | Key Actions |
|---|---|---|
| `splash_page.py` | Splash | wait for auto-transition |
| `language_page.py` | Language selection | select Arabic/English |
| `location_page.py` | Location | allow/skip/search location, system permission handler |
| `onboarding_page.py` | Info pages | swipe, skip, complete onboarding |
| `otp_page.py` | OTP verification | enter phone, enter OTP, resend, skip |
| `main_page.py` | Main (hub) | bottom nav (5 tabs), drawer menu |
| `khotba_page.py` | Khotba (sermon) | list, detail, play audio, live stream, search, favorite, share |
| `concepts_page.py` | Religious concepts | list, detail, share, favorite |
| `reminders_page.py` | My reminders | add, edit, toggle, delete (full CRUD) |
| `favorites_page.py` | Favorites | view, remove, filter by type |
| `settings_page.py` | Settings | language, font, notifications, share app, about, location |
| `video_player_page.py` | Video player | play/pause, fullscreen, error/retry |
| `base_page.py` | (base) | shared actions: click, type, swipe, scroll, toast, keyboard |

### Role 2: Manager — Review Notes (Step 5)

No structural issues. All page objects follow POM pattern consistently. Locators are placeholder IDs that need Appium Inspector validation — this is expected and correct for pre-device phase.

---

## Step 6: Test Cases

### Status: ✅ Built → ✅ Manager Reviewed → ✅ Bug Fixed

---

### Test Coverage Summary

| Test File | Screen | Tests | Markers |
|---|---|---|---|
| `test_smoke.py` | Cross-screen | 4 | smoke, critical |
| `test_onboarding_flow.py` | E2E onboarding | 3 | smoke, critical |
| `test_splash.py` | Splash | 2 | smoke |
| `test_language.py` | Language | 3 | regression |
| `test_location.py` | Location | 3 | regression |
| `test_otp.py` | OTP | 5 | regression |
| `test_khotba.py` | Khotba | 7 | regression, critical |
| `test_concepts.py` | Concepts | 5 | regression |
| `test_reminders.py` | Reminders | 6 | regression |
| `test_favorites.py` | Favorites | 5 | regression |
| `test_settings.py` | Settings | 11 | regression |
| `test_navigation.py` | Navigation | 3 | smoke, critical |
| `test_video_player.py` | Video | 4 | regression |
| **Total** | | **61** | |

### Shared Test Infrastructure

| File | Purpose |
|---|---|
| `tests/helpers.py` | `navigate_to_main()` — shared helper to skip onboarding for all feature tests |
| `tests/conftest.py` | pytest hooks, standalone driver fixture, session logging |
| `tests/base_test.py` | BaseTest class with driver lifecycle + screenshot-on-failure |

### Role 2: Manager — Review Notes (Step 6)

**1 bug found and fixed:**

| # | Bug | Severity | Fix |
|---|---|---|---|
| 1 | `test_khotba.py` uses `By` without importing it (line referencing `share_sheet` locator) | Medium | Added `from selenium.webdriver.common.by import By` |

**Design notes:**
- `test_login.py` deprecated — app uses OTP, not username/password. Redirects to `test_otp.py`.
- `home_page.py` superseded by `main_page.py` but can't delete (permission). Left in place, not imported.
- All feature tests use `navigate_to_main()` helper — DRY, avoids 6-step onboarding duplication.

---

## Blocked Items (Remaining)

| # | Input | Status | Impact |
|---|---|---|---|
| 1 | SmartKhotba APK | ✅ Provided | APK analyzed, capabilities configured |
| 2 | Regression scenarios | ✅ Covered | 61 tests across all screens |
| 3 | Playwright framework structure | ⬜ Pending | Blocks: shared data layer validation |
| 4 | Test environment (emulator/real device) | ⬜ Pending | Blocks: Azure DevOps linking (Step 7) |
| 5 | Appium Inspector session | ⬜ Pending | Needed to validate/fix placeholder locators |

---

## Framework Quality Notes

### What was removed from original plan
- `pytest-rerunfailures` — removed from requirements.txt. Earn stability first.
- `login_page.py` / `test_login.py` — deprecated (app uses OTP, not credentials).

### What was added beyond original plan
- `data/` directory + `credentials.json` (Manager note)
- `scripts/` directory + 3 utility scripts (Manager note)
- `.env.example` for developer onboarding
- `hasattr` guard in BaseTest for setup failures
- Env var → capabilities.json override logic
- `tests/helpers.py` — shared navigation helper
- 13 page objects covering all app screens
- 61 test methods across 13 test files
