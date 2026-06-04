# Agent Execution Brief — SmartKhotba Mobile Automation

**For:** Claude Opus (Antigravity, host execution with adb + Appium access)
**Project:** `D:\MCP servers\Appium-MCP\smartkhotba-mobile-automation`
**App:** `com.islam.khutba.qa` (SmartKhotba Android) — Compose UI, Arabic-first
**Reference:** Read `PROJECT_REVIEW_QA.md` (same folder) BEFORE starting.
**Device:** Real Samsung phone, USB debugging ON, app installed.

---

## ⛔ NON-NEGOTIABLE RULES (read every time)

1. **No fake green.** Never make a test pass by: weakening an assertion, adding blanket `try/except`, `skip`/`xfail` to hide a real failure, returning hardcoded values, or trusting the empty `core/` stubs. A test passes only when the app genuinely does the right thing.
2. **One step at a time.** Finish a step, meet its Acceptance Criteria, report, THEN move on. Do not jump ahead.
3. **Verify locators against the live app** with Appium Inspector / `driver.page_source` — never guess and never keep a PLACEHOLDER.
4. **Root cause before fix.** For every failure, classify it: `(a) real app bug` / `(b) wrong locator` / `(c) state leak (noReset)` / `(d) timing/wait`. State the class, then fix accordingly.
5. **After each step report:** command run · raw result · root-cause read · what you changed. Keep it dense.
6. **Don't commit:** APKs, `reports/allure-results/`, `reports/screenshots/`, `.venv`, `.env`.
7. **Don't touch structural decisions** (CI design, BaseTest redesign) until Phase 3 — they're flagged, not free to rewrite.

---

## PHASE 0 — Environment & Connectivity (blocker)

**Tasks**
- `adb devices -l` → capture real serial (udid).
- `adb shell getprop ro.build.version.release` → real platformVersion.
- `adb shell pm list packages | findstr khutba` → confirm app installed.
- Refactor `config/capabilities.json` → `android_real_device`: read `udid` and `platformVersion` from **env vars** (`DEVICE_UDID`, `PLATFORM_VERSION`) with the current values as fallback. No hardcoded device identity.
- Confirm Appium server starts clean: `appium` (note version; must support UiAutomator2 driver — `appium driver list`).

**Acceptance:** `adb devices` shows the phone as `device`; app package listed; `capabilities.json` no longer hardcodes a single device; Appium server reachable at `127.0.0.1:4723`.

---

## PHASE 1 — RED → GREEN (Critical, blocks everything)

### 1.1 First light — single test
- Set `TEST_ENV=android_real_device`. Run ONLY: `pytest tests/test_smoke.py::TestSmoke::test_app_launches`.
- If fail: capture full stack + `driver.page_source` of what's actually on screen. Classify root cause. Fix. Re-run.
- **Acceptance:** `test_app_launches` green on the real device.

### 1.2 Fill PLACEHOLDER page objects
- `pages/login_page.py` and `pages/home_page.py` are guessed. Open the real app screens, use Appium Inspector, replace every locator with a verified one. Prefer `resource-id` or `content-desc` over text/XPath.
- Update the matching entries in `data/locators.py` (LOCATOR_REGISTRY) with verified primary + at least one real backup.
- **Acceptance:** Zero `PLACEHOLDER` comments remain in `pages/`; each locator confirmed present in the live UI.

### 1.3 Triage the full smoke suite
- Run all 4: `test_app_launches`, `test_reaches_main_screen`, `test_khotba_section_accessible`, `test_concepts_section_accessible`.
- For each failure, produce the root-cause classification table (a/b/c/d). Fix per class:
  - wrong locator → verify in Inspector, update page object + registry.
  - state leak → see 1.4.
  - timing → use explicit waits in `utils/wait_helpers`, never `sleep`.
- **Acceptance:** all 4 smoke tests green **twice in a row** (proves not flaky).

### 1.4 Decide the reset strategy (state-leak fix)
- Problem: `noReset=true` everywhere → favorites/reminders/settings persist between tests; `BaseTest` only does terminate/activate.
- Action: add a per-test (or per-suite) clean-state mechanism. Wire `scripts/clear_app_data.sh` (`adb shell pm clear com.islam.khutba.qa`) into a fixture for state-dependent suites. Keep `noReset` only where intentional and documented.
- **Diagnostic discipline:** to tell a real bug from a state leak — run the failing test in isolation (`pytest <node> -p no:randomly`) AFTER `adb shell pm clear`. If it passes clean but fails in suite → state leak, not a bug.
- **Acceptance:** state-dependent tests pass both in isolation and in full-suite order.

### 1.5 APK path / availability
- Replace the absolute `appium:app` path (`d:/MCP servers/...apk`) with a path relative to project root, resolved via `config/env_config.py`.
- Document in README how to obtain the APK (it's gitignored). Add a guard: if APK missing for emulator/ci env, fail with a clear message (not a cryptic Appium error).
- **Acceptance:** emulator/ci_headless env gives a clear, actionable error when APK absent; no machine-specific absolute paths in config.

---

## PHASE 2 — YELLOW (Needs Work)

### 2.1 Unify test lifecycle
- `test_login.py` and `test_step1_acceptance.py` use the raw `driver` fixture (no app restart); the rest use `BaseTest`. Standardize on `BaseTest` so every test has identical setup/teardown. Migrate the two outliers.
- **Acceptance:** all test classes inherit `BaseTest`; no test relies on the bare `driver` fixture unless explicitly justified in a comment.

### 2.2 Harden brittle locators
- `pages/main_page.py` uses Arabic text XPath (`//*[@text='الرئيسية']`). Replace with `resource-id`/`content-desc` where the app exposes them (check Inspector). Keep text XPath only as a registry backup, never primary.
- **Acceptance:** no Arabic-text XPath as a *primary* locator in page objects.

### 2.3 Fix the self-healing heuristic
- In `utils/locator_healing.py`, the `By.ID` fallback builds `//*[contains(@resource-id, ...)]` which can match multiple nodes and silently return the first. Make it assert uniqueness (find_elements, require len==1) before accepting a heal; otherwise log and fail.
- **Acceptance:** healer never returns an ambiguous match silently; ambiguous case is logged + raised.

### 2.4 Toast capture
- `get_toast_message` uses a single `find_element` — toasts are transient. Replace with a short polling loop (WebDriverWait, ~3s) so it actually catches them.
- **Acceptance:** a known toast-producing action is captured reliably across 3 runs.

### 2.5 Credentials hygiene
- `data/credentials.json` is committed. Move test creds to env (`.env`, gitignored) or clearly mark as throwaway dummy data. No real account secrets in repo.
- **Acceptance:** no real credentials tracked in git.

---

## PHASE 3 — GREEN (Professional Adds) — confirm with me before large changes

### 3.1 README
- Write a project README: prereqs (Appium, adb, Python, drivers), env setup, how to pick `TEST_ENV`, how to run smoke vs regression, how to view Allure.
- **Acceptance:** a new engineer can run smoke from README alone.

### 3.2 CI pipeline
- Add CI (GitHub Actions with `reactivecircus/android-emulator-runner`, or Azure). Run `@smoke` on PR; publish Allure. Use `ci_headless` env. **Propose the file, don't merge silently.**
- **Acceptance:** smoke runs in CI on an emulator and publishes a report.

### 3.3 Flaky control & metrics
- Add `pytest-rerunfailures` (limited retries, smoke only). Surface `data/healing_metrics.json` as a CI artifact or simple summary.
- **Acceptance:** retries configured; healing metrics visible post-run.

### 3.4 core/ stubs — implement or delete
- `core/api_testing.py`, `performance_testing.py`, `security_testing.py` return fake data. Either implement real logic or delete the modules and any imports. No empty shells shipped.
- **Acceptance:** no module returns hardcoded fake metrics.

---

## PHASE 4 — CLEANUP

- Remove tracked `reports/allure-results/*` and `reports/screenshots/*` from disk/git; confirm `.gitignore` covers them.
- Move `AUDIT_CONVERSATION_*.md` / `BUILD_LOG.md` to a `docs/` folder.
- **Acceptance:** clean working tree; `git status` shows no stray artifacts.

---

## FINAL DEFINITION OF DONE

- Smoke suite (4 tests) green twice consecutively on the real device.
- Zero PLACEHOLDER locators; zero fake-green patterns.
- Each Phase-1 fix has a documented root-cause classification.
- Structural changes (Phase 3) proposed, not force-merged.
- A short report per phase: what failed, why (root cause), what changed, evidence (passing run output).

**If you ever can't find a real cause, STOP and report it — do not invent a passing path.**
