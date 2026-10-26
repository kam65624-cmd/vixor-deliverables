# مصفوفة الاختبارات وCI — النتيجة النهائية الموثقة

**قاعدة التمييز (سارية بكل الجلسات):** `FRESH` = شُغِّل في هذه الجلسة ب Exit codes حقيقية · `HISTORICAL` = نتيجة محفوظة من جلسة سابقة موثقة بلوج · `CI` = مشغل GitHub Actions بمعرّف run · لا يُرفع PASS من أي نوع على حساب الآخر.

---

## 1) المصفوفة الحاسمة: R19 / ALERT-01 (تحويل BLOCKED → PASS) — `FRESH 2026-10-26`

**البيئة:** worktree معزول `audit2/repos/tgb-r19`، فرع `fix/alert01-trackingpatch-r19`، الأساس `944e60c0` (main بعد دمج PR #17). node v24.21.0 / npm 11.19.0.
**الدليل:** `audit2/logs/r19_matrix_2026-10-26.log` (المراحل A→E كاملة بأكواد الخروج).

| المرحلة | الإجراء | النتيجة (exit code حقيقي) | الحكم |
|---|---|---|---|
| A1 | بناء `.smoke` من مصدر **قبل** الإصلاح (tsc -p tests/smoke.tsconfig.json) | exit 0 | FRESH PASS |
| A2 | `npm test` (smoke suite كاملة) قبل الإصلاح | **86/86**، exit 0 | FRESH PASS |
| A3 | `node tests/alert01-regression.cjs` قبل الإصلاح | **19/19**، exit 0 — **R19 غائب (0 ذكر)** | FRESH PASS |
| B1 | تطبيق باتش commit-3 (git apply --check ثم apply) | check=0، apply=0 | FRESH PASS |
| B2 | التحقق بالـ blobs الناتجة | `eb5da95b…` + `52e835c9…` = post-images **المتطابقة تامًّا** | VERIFIED |
| B3–B4 | إعادة بناء + smoke بعد الإصلاح | rebuild=0؛ **86/86** | FRESH PASS |
| B5 | regression بعد الإصلاح (يجب أن يعمل R19 ويجتاز) | **20/20 مع R19 أخضر**، exit 0 | **FRESH PASS** |
| C1–C3 | **الاختبار المعكوس:** مصدر قبل الإصلاح + اختبار R19 | **19/1 — فشل بالسبب المتوقع** («trackingPatch update result was never checked — save error silently discarded»)، exit 1 | GATE PROVEN |
| D | محاولة مرحلية (apply على ملف مرقّع مسبقًا) | فشل → **مصحح بصدق داخل اللوج** (سطر CORRECTION) | honesty note |
| E1–E5 | **الإعادة النظيفة النهائية:** checkout pre-images (15bee1df/48a89684) → apply نظيف → post-images مؤكدة → rebuild → smoke + tsc + regression | smoke **86/86**، **tsc exit 0**، regression **20/0 مع R19 أخضر**، exit 0 | **FINAL: FRESH PASS** |

**الاستنتاج:** إصلاح ALERT-01 الثلاثي (بعد الجولات 1+2+3) **مُتحقق منه سلوكيًا على شجرة حقيقية**، وR19 مثبت في الاتجاهين (يفشل قبل الإصلاح بالسبب المتوقع، ويجتاز بعده).

## 2) مشغلات CI على GitHub (معرفات runs حقيقية — متحقق API)

| النطاق | Run | الحدث | الخلاصة | التوقيت |
|---|---|---|---|---|
| PR #18 (f4d69f74) | 40272857668 | pull_request | **success** | 05:11:03Z |
| main بعد الدمج (76830a72) | 40272909018 | push | **success** | 05:11:38Z |
| main بعد PR #17 (944e60c0) | 40271520067 | push | success | 04:55:20Z |
| PR #17 (ccb6cbe — تاريخي 16-G/16-H) | 40245203792 | pull_request | success | 2026-10-25T23:32Z |
| main @ d745408 (baseline) | 39879264854 | push | success | 2026-10-23 |

## 3) مصفوفة الاختبارات الأخرى عبر المستودعات

| المستودع | ما شُغِّل | النتيجة | النوع | الدليل |
|---|---|---|---|---|
| tg-content-bot (bot-worker) | smoke suite | 86/86 (منذ Task 3 حتى المصفوفة الحالية — عدد ثابت عبر كل الجولات) | HISTORICAL + FRESH | لوجات متعددة |
| tg-content-bot (bot-worker) | regression ALERT-01 | تطور: 16/16 → 19/19 (بعد R1) → **20/20** (بعد commit 3) | HISTORICAL + FRESH | لوجات 16-*/18 |
| tg-content-bot | `tsc --noEmit` | نظيف في كل جولة | HISTORICAL + FRESH | المصفوفة E4 |
| vixor-trade | vitest | **199/199** (15 ملفًا — تغطية ingest = صفر، نتيجة مراجعة) | HISTORICAL | Task 3 |
| vixor-shield | vitest | **152/152** | HISTORICAL | Task 3 |
| vixor-hunt | vitest | **149/149** | HISTORICAL | Task 3 |
| vixor-packages | turbo typecheck | **4/4** | HISTORICAL | Task 3 |
| vixor-APP | CI كامل (typecheck/eslint/prettier/vitest/build) | أخضر على نفس commit | CI (بدل التشغيل المحلي) | Task 3 |
| الخيار A (SQL) | pglite_sequential_tests.mjs | **22/22** على PostgreSQL 18.6 حقيقي (wasm) | HISTORICAL + FRESH (16-I2/16-I3) | لوجات pglite |
| harness R20/R21/R22 | تزامن حقيقي بجلستي psql | **NOT EXECUTED** — لا PG server/docker في البيئة | **BLOCKED** | موثق بصدق |

## 4) حالة CI لكل مستودع (من baseline API — متسقة مع الأدلة التاريخية)

| المستودع | حالة CI | ملاحظة |
|---|---|---|
| tg-content-bot | أخضر (push + pull_request) | CI اختبارات bot-worker + mini-app |
| vixor-APP | أخضر + Block-Force-Push workflow | حماية main نشطة |
| vixor-hunt / vixor-shield / vixor-packages | أخضر على فروع PRs الدِرافت | نشطة |
| vixor-trade | batch-compute مجدول «success» دوري | **placeholder بلا عمل فعلي** (نتيجة Task 6 — لا يُحتسب كـ CI حقيقي) |
| vixor-deliverables | لا workflows | docs فقط |
| poplix-movie-app | deep-channel-health مجدول success | نشط |
| JAMRA | **لا CI** | فجوة — توصية: إضافة workflow أساسي |

## 5) ملاحظات نزاهة على القياس

- لوجات 16-H/16-I (regression/smoke/tsc) تُستشهد **كأدلة تاريخية فقط** بعد تدويرات البيئة — ولم تعد تُقدَّم كتشغيل جديد، حتى عادت البيئة بالاستنساخ الحي في TASK 18.
- تصحيح موثق داخل المصفوفة نفسها: المرحلة [D] كانت إعادة تطبيق على ملف مرقّع (خطأ إجرائي) — صُححت بإعادة [E] النظيفة من pre-images المؤكدة، ولي بإخفاء الخطأ.
- درس TASK 17-2 ساري: **كود خروج `git apply` وحده لا يكفي** (إيجابية كاذبة داخل شجرة scaffold) — الحكم دائمًا بـ post-blob.
- `tsc` في اللوجات التاريخية كان نظيفًا لكن بلا capture لكود الخروج داخل اللوج (تحفظ موثق 16-I3) — أُغلق هذا التحفظ بالمصفوفة الحالية (exit 0 صريح في E4).
