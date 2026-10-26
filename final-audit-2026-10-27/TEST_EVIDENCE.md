# TEST_EVIDENCE.md — أدلة الاختبارات (TASK 21، 2026-10-27)

**قاعدة:** `FRESH` = شُغِّل هذه الجلسة بكود خروج حقيقي · `CI` = GitHub ‏Actions بمعرّف run على SHA ‏محدد · `HISTORICAL` = محفوظ ببصمة · لا PASS ‏من نوع على حساب آخر.

## 1) ما شُغِّل فعليًا هذه الجلسة (FRESH)

| # | الاختبار | الهدف | النتيجة | exit | اللوج |
|---|---|---|---|---|---|
| T1 | **R20–R22 مصفوفة التزامن** (جلستا TCP ‏حقيقيتان على PostgreSQL ‏**17.10 حقيقي** — ثنائيات فعلية، معزول 127.0.0.1:54329، datadir مؤقت) | خيار A ‏(claim/resolve RPC) | **6/6 PASS** — R20: حجز واحد حتمي (B انتظر **3509ms** على قفل الصف ثم رأى الـlease ⇒ null) · R21a: قطع اتصال ⇒ abort بلا lease ⇒ إعادة حجز فورية · R21b: الـlease يمنع 31ث ثم تُستعاد · R22: hold المصالحة + unknown_at ثم delivered نهائي | 0 | `test-evidence-r22_run1_2026-10-27.log` |
| T2 | **إعادة T1 للثبات** | نفسه | **6/6 PASS مجددًا** (R20 ‏blocked_ms=3509) | 0 | `test-evidence-r22_run2_2026-10-27.log` |
| T3 | **alert01-regression.cjs على main المدموج `76830a72`** (استنساخ tarball رسمي بالتوكن + npm ci + بناء .smoke) | ALERT-01/R19 | **20/20** — R19 أخضر بالسلوك الظاهر: «trackingPatch save returns error → detected + logged loudly + delivery unaffected» | 0 | `test-evidence-r19_fresh_main_2026-10-27.log` |
| T4 | `npm test` ‏(tsc ‏-p ‏smoke.tsconfig.json && smoke-test.cjs) على نفس الشجرة | الحزمة الكاملة | **86/86** | 0 | نفس اللوج |
| T5 | `npm run typecheck` ‏(tsc ‏--noEmit) على نفس الشجرة | الأنواع | نظيف | 0 | نفس اللوج |
| T6 | `verify_manifest.py` ‏(منطقيًا — نفس الحسابات) على رأس PR #10 الجديد | F1 | MANIFEST↔الملفات **9/9 MATCH** من blobs ‏الرأس | — | داخل `task1_f1_fix_push.py` + محادثة |

**بيئة T1/T2:** `embedded-postgres@17.10.0-beta.17` (حزم `@embedded-postgres/linux-x64` — initdb/postgres/pg_ctl ‏ثنائيات حقيقية) · قاعدة `vixor_test_disposable` · fixture ‏+ r3 ‏SQL ‏مطبقان حرفيًا كالـharness الأصلي · تكيف موثق: عميل `pg` ‏TCP بدل psql (غير متوفر بالحزمة) وقطع سوكيت فجائي بدل `timeout 2 psql` — نفس الدلالة (abort ‏عند قطع الاتصال) ومُتحقق من النتيجة. **صفر صلة بأي قاعدة إنتاج.**

## 2) CI ‏الحية المتحققة (API ‏بالتوكن، 2026-10-27)

| Run | الحدث | head SHA | النتيجة | مطابقة الادعاء |
|---|---|---|---|---|
| 40272909018 | push | `76830a721bb3` (main بعد PR #18) | success | ✓ |
| 40272857668 | pull_request | `f4d69f748d0d` (PR #18) | success | ✓ |
| 40271520067 | push | `944e60c0c794` (main بعد PR #17) | success | ✓ |
| 40245203792 | pull_request | `ccb6cbefd58d` (PR #17 تاريخي) | success | ✓ |
| 39879264854 | push | `d74540876cdc` (baseline) | success | ✓ |

- **لا CI ‏على رأس PR #10 الجديد `4b3eebe0`:** vixor-deliverables **لا workflows** ⇒ `NOT_APPLICABLE` (ليست فجوة؛ نجاح «الاختبارات المحلية» لا يُدّعى هناك أصلًا — الحزمة docs).
- **فجوة P1 المالك مؤكدة:** R19 ‏غير مستدعى في ci.yml/package.json (LINE_BY_LINE §ج) — مقترح الربط جاهز، والتطبيق بوابة مالك.
- **تحذير CI-NEW-01 ‏مثبت مجددًا:** نص ci.yml ‏البايتي `branches: [main]` (sha256 ‏2a12a2e0…) — ما يُعرض في المخرجات يبتلع `[m`.

## 3) ما لم يُشغَّل / محجوب (بذاعة — لا صمت)

| البند | الحالة | السبب الدقيق | ما يلزم |
|---|---|---|---|
| ALERT-08 ‏preflight ‏على قاعدة الإنتاج | `BLOCKED` | القناة الوحيدة بالبيئة `DATABASE_URL=file:…/db/custom.db` (SQLite ‏ساندبوكس غير موجود أصلًا)؛ توكن GitHub ‏لا يمنح DB؛ `upload/` فارغ | المالك ينفذ الاستعلام الجاهز ويلصق النتيجة (بيانات وصفية فقط) — أو يُسقط ملف اتصال قراءة-فقط في `upload/` |
| ALERT-07 ‏§A ‏(Cloudflare deployments/cron) | `BLOCKED` | توكن CF ‏السابق غير صالح؛ لا مسار آخر لإثبات المنشور فعلًا | أدلة من لوحة CF ‏بصلاحيات المالك |
| R20-R22 ‏على PostgreSQL **إنتاجي-مطابق** (v14+ بمكوّنات Supabase) | `PASS_WITH_LIMITATIONS` | نُفذ على PG ‏17.10 ‏معزول بثنائيات رسمية — بيئة Supabase ‏المدارة قد تختلف إضافات/صلاحيات (SECURITY DEFINER/grants ‏مغطاة بالاختبار المنطقي) | إن رغب المالك: تشغيل نفس الـSQL ‏على قاعدة Supabase ‏اختبارية قبل أي ترحيل |
| اختبارات تكامل منتِج→مستهلك جديدة | `NOT_RUN` | **صفر منتجين موجودين** (PATH-C) — كتابة اختبارات على مسارات وهمية محظور نصًا | تُنشأ عند أول تفعيل منتج (M1→M4→M3) |
| إعادة R19 ‏pre-fix ‏(بوابة معكوسة) هذه الجلسة | `NOT_RUN` | main ‏المدموج يحوي الإصلاح؛ البوابة المعكوسة أُنجزت موثقة في مصفوفة TASK 18 ‏(لوج ‏453eb0c5… بصمته في MANIFEST) | لا شيء — غطاها التاريخ + التشغيل الحالي |

## 4) أدلة تاريخية ببصمات (نموذجية)

- لوج مصفوفة R19 ‏الأصلي: `audit2/logs/r19_matrix_2026-10-26.log` (7,443 B، sha256 ‏453eb0c5… = MANIFEST) — محفوظ بالحجم الدائم.
- patch commit-3: sha256 ‏54dc37b5… (محفوظ بسجلات 16-H/MANIFEST) — content الآن **على main فعليًا** بـblobs ‏مطابقة.

## 5) ملحق TASK 22 — أدلة طازجة (إعادة تشغيل مستقلة، 2026-10-26 18:0x UTC)

| # | الاختبار | البيئة | النتيجة | exit | اللوج (نسخة داخل evidence/) |
|---|---|---|---|---|---|
| T7 | **R20–R22 جولة ثالثة** (`node r22_real_pg.js run3_task22`) — نفس المنهجية حرفيًا | PG ‏17.10 ثنائيات، معزول 127.0.0.1:54329، datadir جديد | **6/6 PASS** — R20 blocked_ms=**3509** (ثالث ظهور متطابق ⇒ حتمية الانتظار على قفل الصف) | 0 | `test-evidence-r22_run3_task22_2026-10-27.log` |
| T8a | `node tests/alert01-regression.cjs` من شجرة طازجة **قبل** بناء `.smoke` | tarball رسمي @ `76830a72` | **FAILED — MODULE_NOT_FOUND** `../.smoke/src/db/client.js` | 1 | `test-evidence-r19_task22_fresh_2026-10-27.log` (محفوظ بصدق) |
| T8b | نفس الأمر **بعد** `npm test` (يبني `.smoke` داخل tsc -p tests/smoke.tsconfig.json) | نفس الشجرة | **20/20** — R19 خضراء | 0 | نفس اللوج (تصحيح الترتيب موثق داخله) |
| T8c | `npm test` | نفس الشجرة | **86/86** | 0 | نفس اللوج |
| T8d | `npm run typecheck` | نفس الشجرة | نظيف | 0 | نفس اللوج |
| T9 | **اختبارات سلوك المُحقّق** على رأس PR #10 `4b3eebe0`: تشغيل نظيف / حذف ملف / تزوير بايت / تزوير sha256 بالمانيفست | دليل مُعاد بناؤه من blobs الرأس | exit **0 / 1 / 1 / 1** — يقرأ المحتوى الفعلي (hashlib+open) لا قيم الـmanifest | — | `t22_f1_verify_results.json` |

**اكتشاف N-1 (من T8a):** `alert01-regression.cjs` يستهلك أثر بناء `.smoke/` — أي سكربت `regression` مستقل (`node tests/alert01-regression.cjs`) يفشل من شجرة نظيفة. أثره على رقعة R19 المقترحة: **الترتيب الحالي للرقعة آمن** (خطوة regression تأتي بعد Smoke tests في ci.yml المقترح) لكن يُوصى بجعل السكربت مكتفًا — الرقعة v2: `R19_CI_WIRING_PROPOSAL_v2_amended.patch` (اقتراح فقط، بلا تطبيق).
**تصنيف T7:** `PASS_WITH_LIMITATIONS` كما هو (PG محلي معزول ≠ طبقة Supabase المدارة — القيد R21-03 قائم). **تصنيف T8:** `VERIFIED (fresh)` على SHA المدموج `76830a72` بالبيئة المعلنة (node v24.21.0، npm 11.19.0، tarball رسمي بالتوكن).
