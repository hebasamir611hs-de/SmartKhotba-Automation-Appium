# SmartKhotba Mobile Automation — QA Director Review

**Reviewed:** 2026-06-02 | **Reviewer:** Senior QA Director (mentor mode)
**Stack:** Python · Appium · UiAutomator2 · pytest · Page Object Model · Allure · FastMCP server
**Scope:** `smartkhotba-mobile-automation/` (75 tests, 15 page objects, self-healing layer)

> دلوقتي بصيت على المشروع الصح — ده Appium mobile framework حقيقي، ومستواه أعلى بكتير من الـ web framework. التقييم تحت بيركّز على اللي هيوقفك لما توصّلي الموبايل.

---

## ⚡ قبل ما توصّلي الموبايل — حقيقة مهمة

1. **مش محتاجة Android Studio عشان تشغّلي على موبايل حقيقي.** اللي محتاجاه: USB debugging مفعّل، `adb devices` يشوف الجهاز، Appium server شغّال، وتعملي `TEST_ENV=android_real_device`. Android Studio بس عشان الـ SDK/adb و Appium Inspector.
2. **الـ `android_real_device` caps فيها udid ثابت `RKCY600K8RD` و platformVersion `16`** — ده شغّال على موبايلك انتي بس. لو الجهاز اتغير → يقع.
3. **بلوك الـ real_device مفيهوش `appium:app`** (عكس الـ emulator) — يعني الـ APK لازم يكون **متسطّب على التليفون يدوي** قبل ما تشغّلي. متأكدة إنه متسطّب؟
4. **`login_page.py` و `home_page.py` لسه PLACEHOLDER** — اللوكيتورز متخمّنة ومتأكدتش من APK. أي تيست يعدّي عليهم هيقع بثقة كاذبة.

**خطوة الأمان قبل التوصيل:** ثبّتي smoke أخضر على الإيميوليتر الأول → اتأكدي الـ APK متسطّب على الموبايل → صلّحي اللوكيتورز عبر Appium Inspector.

---

## 0. 🔴 أحمر — اللي بيوقفك دلوقتي (Critical)

1. **الـ Smoke suite أحمر.** `lastfailed` + 11 screenshot فشل بتقول إن `test_app_launches`, `test_reaches_main_screen`, `test_khotba_section_accessible`, `test_concepts_section_accessible` كلهم وقعوا في آخر runs. ده **الأساس** — أي حاجة فوقه غير موثوقة. اعملي triage الأول قبل أي إضافة.
2. **Placeholder locators** في login/home (نقطة فوق). إما تتملّى من APK إما التيستات اللي بتعتمد عليها تتعلّم عليها skip.
3. **مسار الـ APK absolute ومتحطوط hardcoded:** `d:/MCP servers/.../smartkhotba.apk` في `capabilities.json` → يقع على أي جهاز/CI تاني. وكمان `apps/*.apk` متعمله gitignore → fresh clone مفيهوش APK أصلاً، يعني emulator/ci_headless مش هيشتغلوا خالص بعد clone.
4. **`core/` كله stubs فاضية.** `api_testing`/`performance_testing`/`security_testing` بترجّع `{}` و `risk_score: 0` ثابت. لو أي حاجة بتستوردهم وبتثق فيهم → نفس fake-green اللي اتكلمنا عليه. implement أو احذفي.
5. **`noReset=true` في كل البيئات.** الـ state بيتسرّب بين التيستات (favorites/reminders/settings بتفضل متخزّنة) → flakiness معتمد على الترتيب. ده على الأرجح سبب وقوع الـ smoke.

---

## 1. 🟡 أصفر — محتاج شغل (Needs Work)

- **مفيش README للمشروع الموبايل.** أي حد (أو انتي بعد شهر) مش هيعرف يشغّله. أهم ملف ناقص.
- **مفيش CI pipeline للموبايل.** Allure متظبّط بس مفيش حاجة بتشغّله أوتوماتيك. (الـ `.github` اللي موجود بتاع الـ MCP server مش بتاع التيستات).
- **أسلوبين للتيستات.** الأغلبية بتورّث `BaseTest` (بيعمل terminate/activate restart)، بس `test_login` و `test_step1_acceptance` بيستخدموا الـ `driver` fixture الخام (مفيش restart) → دورة حياة غير متسقة. وحّديهم.
- **Locators بالنص العربي في `main_page`** زي `//*[@text='الرئيسية']` — هشّة جدًا: أي تغيير في الكلام أو الـ localization يكسرها. فضّلي resource-id / content-desc.
- **Healing heuristic لـ By.ID** بيبني XPath `contains(@resource-id)` ممكن يطابق أكتر من عنصر ويرجّع الأول بصمت → نتيجة غلط محتملة.
- **Toast عبر `find_element` XPath** — الـ toasts عابرة، محتاجة polling سريع، الطريقة الحالية flaky.
- **`credentials.json` متعمله commit** (test_user/Test@123). خطر بسيط بس مكانش المفروض في الريبو — حطيها في env أو gitignore.
- **BaseTest بيعمل terminate/activate كل تيست** = بطيء؛ مفيش استراتيجية session reuse للـ smoke.

---

## 2. 🟢 ممكن تضيفيه عشان احترافية (High-Value Adds)

| الإضافة | الفايدة |
|---|---|
| **CI: GitHub Actions + `reactivecircus/android-emulator-runner`** | smoke يشتغل على كل PR + publish Allure تلقائي |
| **APK management (Git LFS أو download step) + مسار relative من env** | الريبو يشتغل على أي جهاز/CI |
| **pytest-rerunfailures** | retry للتيستات الـ flaky — حيوي في الموبايل |
| **Reset fixture يستخدم `scripts/clear_app_data.sh`** | يحل تسريب الـ state للتيستات المعتمدة على بيانات |
| **udid + platformVersion من `adb` أو env** | الـ real_device caps تشتغل لأي موبايل مش بتاعك انتي بس |
| **توصيل `metrics_tracker` / `healing_metrics.json` بداشبورد أو artifact** | تستفيدي من الـ self-healing data اللي بتتجمّع |
| **Device matrix عبر `TEST_ENV` في CI** | البنية موجودة — وصّليها بس |

---

## 3. ⚪ مش محتاجاه — نضّفيه (Cleanup)

- **400+ ملف `reports/allure-results/*.json`** متجمّعين على الديسك. (موجودين في .gitignore دلوقتي بس لسه على الديسك — امسحيهم).
- **11 screenshot فشل** في `reports/screenshots` — مؤقتين، شيليهم.
- **`core/` stubs الفاضية** — implement أو احذفي، مايصحّش يتشحنوا فاضيين.
- **`AUDIT_CONVERSATION_*.md` / `BUILD_LOG.md`** في الـ root — احتفظي بيهم كـ history بس مش في الجذر مثاليًا.

---

## 4. الأولويات بالترتيب (افعليها كده)

1. **اعملي triage للـ smoke الأحمر** — لحد ما الـ 4 تيستات الأساسية يبقوا أخضر ثابت. مفيش معنى لأي حاجة قبل دي.
2. املّي الـ placeholder locators (login/home) من Appium Inspector على APK حقيقي.
3. صلّحي مسار الـ APK (relative + env) واعملي خطة للـ APK في الريبو (LFS/artifact).
4. وحّدي `noReset` strategy — clear app data بين التيستات المعتمدة على state.
5. وحّدي أسلوب التيستات على `BaseTest`.
6. اكتبي README + ضيفي CI بإيميوليتر.
7. implement أو احذفي `core/` stubs.

---

**التحدي الأخير ليكي:** الـ `BaseTest` بيعمل `terminate/activate` كل تيست، بس `noReset=true` بيخلّي الداتا متراكمة. يعني التيست شايف شاشة "نضيفة" بس الـ state القديم لسه موجود. **إزاي تتأكدي إن `test_reaches_main_screen` بيقع بسبب bug حقيقي مش بسبب state متسرّب من تيست قبله؟** لو مش عارفة تجاوبي، ده أول سؤال تحلّيه قبل ما توصّلي الموبايل — عشان متطارديش أشباح.
