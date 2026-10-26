# LINE_BY_LINE_REVIEW.md — مراجعة سطرًا بسطر (TASK 21، 2026-10-27)

**نطاق ما تاح فعليًا:** ‏(أ) PR #10 كاملًا (9 ملفات مثبتة بايتيًا)؛ ‏(ب) diff الإنتاجي الكامل `d745408…→76830a72` (6 ملفات +928/−26 — patches من compare API)؛ ‏(ج) شجرة main الحية (tarball رسمي) للتحقق الكودي المباشر.
**غير المتاح:** أي diffs ‏للمستودعات الأخرى لا يوجد فيها تغيير من الوكيل أصلًا (صفر diffs = لا شيء لمراجعته).

---

## أ) PR #10 — فرع `audit/final-evidence-handoff-2026-10-26` @ `4b3eebe0`

**التاريخ:** 3 commits ‏(b0e18219 → afa37b81 → **4b3eebe0 إصلاح F1**) · 9 ملفات، كلها docs/manifest + verifier واحد · **لا كود إنتاجي في الـPR إطلاقًا** ⇒ أثر سلوكي: صفر على أي خدمة.

| الملف | الحكم | ملاحظات المراجعة |
|---|---|---|
| SESSION_FINAL_REPORT.md (23,213 B) | سليم | الرواية الزمنية A–L ‏مطابقة للسجلات المحفوظة؛ التصنيفات FRESH/HISTORICAL ‏منضبطة؛ ادعاء ALERT-01 ‏أصبح الآن **متحققًا حيًا** (REPOSITORY_STATUS §2) |
| REPOSITORY_INVENTORY.md (6,474 B) | سليم — دقيق | مطابقة حية كاملة للـ9 مستودعات (الاستثناء الوحيد: pushed_at ‏لـdeliverables تحرك بدفع F1 المرخص) |
| FILE_CHANGE_REGISTER.md (8,025 B) | سليم | +928/−26 مطابق للـcompare API ‏حرفيًا؛ لا حذف تاريخي |
| TEST_AND_CI_MATRIX.md (6,757 B) | سليم | المصفوفة مطابقة للـCI ‏الحية (runs الخمسة كلها success على SHAs ‏الصحيحة) |
| SECURITY_AND_RISK_REGISTER.md (6,484 B) | سليم | SEC-03 ‏ما يزال مفتوحًا — صحيح (التوكن لم يُدوَّر) |
| CROSS_PROJECT_INTEGRATION_AUDIT.md (5,730 B) | سليم | PATH-C ‏خلاصات مطابقة لمصفوفة r1 المحفوظة |
| UPLOAD_AND_HANDOFF.md (6,247 B بعد F1) | سليم بعد F1 | النسخة النهائية المقصودة (تضيف رابط PR ‏+ SHA + التحقق الحي) — الفرق عن النسخة المنحرفة: صف واحد فقط |
| MANIFEST.json (بعد F1) | سليم بعد F1 | 9/9 MATCH ‏محسوبة من blobs ‏الرأس؛ كتلة f1_correction توثق السبب الجذري والقيود |
| verify_manifest.py (مضاف F1) | سليم | 952 B — مُحقّق ذاتي (تشغيله على الشجرة = exit 0)؛ مسح أسرار: نظيف |

**Findings على الـPR:** ‏F1 (مُصلَح — HIGH، كان يجعل التحقق الذاتي يفشل) · F2 ‏(INFO — صياغة «60 نتيجة/+13×P3» وضّحناها) · لا CRITICAL ‏لا HIGH متبقية.

## ب) diff الإنتاجي tg-content-bot: `d745408… → 76830a72` (إصلاح ALERT-01 الثلاثي، 5 commits شاملة المدمجات)

### ب.1 `bot-worker/src/pipeline/ath-monitor.ts` (+101/−17) — تمت مراجعته سطرًا
| الأسطر | التغيير | الحكم |
|---|---|---|
| L32 | استيراد `MAX_NOTIFY_ATTEMPTS` | سليم |
| L352-361 | `trackRes = await ...update(trackingPatch)` + **فحص `trackRes.error`** + سجل خطأ صاخب (signal id + message فقط — لا أسرار) + تعليق صادق أن `exit_reason` تقارري فقط | **سليم** — جوهر commit-3؛ supabase-js ‏لا يرمي ({error} semantics موثقة db/client.ts) |
| L364-371 | حلقة رؤية المستنفد: `hit_at && !hit_notified_at && attempts>=5` ⇒ سجل error ‏«pending manual review» كل مسح | سليم — يحقق «إنهاك بصوت مسموع» |
| L380-445 | إعادة كتابة حلقة التسليم: حلقة لكل هدف؛ الحارس `tgthit:<signal>:<kind>` **يُكتب بعد نجاح الإرسال فقط**؛ مسار مصالحة (حارس موجود + حالة ناقصة ⇒ تسوية بلا إرسال)؛ محاولات/تهدئة تُحدّث دائمًا | سليم — يطابق تصميم V2 ‏(S0-S6) وR1-R18 |
| حفظ حالة التسليم بعد الحلقة | أعيدت كتابة targets ‏كاملة (كما هو سابقًا) | **ملاحظة معروفة موثقة** = ALERT-08-ب ‏(lost-update) — حلها خيار A، وليست تراجعًا عن هذا الإصلاح |

### ب.2 `bot-worker/src/utils/targets.ts` (+35/−4) — تمت مراجعته سطرًا
- `TargetDef` +3 حقول تسليم (`hit_notified_at`/`hit_notify_attempts`/`hit_last_attempt_at`) بصور آمنة.
- ثوابت: `MAX_NOTIFY_ATTEMPTS = 5`، `NOTIFY_RETRY_COOLDOWN_MS = 5د` — مطابقة للتصميم وللثوابت في r3 SQL.
- `parseTargets`: يحمل الحقول الجديدة بقيم آمنة للشكل الغلط. **(ملاحظة معروفة: قائمة حقول صريحة تُسقط المجهول — خطر الانتقال للخيار A، موثق ومطلوب معه ترتيب نشر worker↔migration.)**
- `evaluateTargets` — **التغيير الدلالي الجوهري**: القديم `if (t.hit_at) continue` (كتم دائم) ⇒ الجديد: تسليم مكتمل يتخطى؛ ضرب غير مُسلّم يُعاد إنتاجه كل مسح مع احترام السقف والتهدئة (at-least-once). **مطابق حرفيًا للتصميم الملزم.**

### ب.3 الاختبارات (+706 regression جديد، +54 fake-supabase، +29/−5 smoke، +3 tsconfig) — تمت مراجعتها
- regression ‏يغطي R1-R19 ‏بما فيها المسارات التي طلبها المالك (R16 فحص نتيجة الحفظ، R17 وجهة ناقصة، R18 ‏TP+SL بنفس الإشارة، R19 ‏trackingPatch) — وقد **شُغّلت طازجة على هذا الشجرة: 20/20 exit 0**.
- fake-supabase: حقن أخطاء HTTP ‏حقيقية الشكل (500 + {message,code} ‏مُعادة لا مُرمية) — محاكاة أمينة لسلوك supabase-js.
- smoke: ‏+29/−5 — التوافق مع الحقول الجديدة؛ 86/86 طازج.

### ب.4 تأثير على الميزات القائمة
- مسار النشر العادي/الـcron/الـmini-app: لا مساس (الفرق محصور بـbot-worker ‏مسار ath-monitor + اختباراته). CI ‏أخضر على كل الـSHAs ‏المتأثرة. tsc ‏نظيف.

## ج) التحقق المستودعي الطازج المرتبط

- **ALERT-08 مستودعيًا ⇒ `VERIFIED` (طازج):** 27 ملف SQL ‏في الشجرة الحية، **صفر** يذكر `max_multiple`/`exit_reason`، ولا ALTER/CREATE ‏يضيف `targets` — اكتشاف 16-I ‏مؤكد على الشجرة المدموجة. (مستوى الإنتاج: UNKNOWN حتى preflight — BLOCKED.)
- **R19 ‏والـCI ‏(P1 المالك):** `package.json` لا يملك سكربت regression؛ `ci.yml` (sha256 ‏2a12a2e0…، بايتيًا `branches: [main]`) يشغّل typecheck+smoke فقط ⇒ **R19 غير بوّابي في الـCI**. الرقعة المقترحة: `R19_CI_WIRING_PROPOSAL.patch` (مراجعة فقط). البديل المنفذ: **سجل تشغيل طازج قابل للتحقق** على main ‏المدموج 20/20+86/86+tsc ‏0 ‏(`test-evidence-r19_fresh_main_2026-10-27.log`).
- **commit F1 الخاص بي** (4b3eebe0): 3 ملفات، الـdiff ‏= استعادة صف واحد + كتلة توثيق + مُحقّق ذاتي — مُراجع عبر API ‏بعد الدفع (9/9 MATCH).

## د) الشدات المرتبة

| الشدة | Finding | الحالة |
|---|---|---|
| HIGH | F1: تضارب MANIFEST/الملف (نسختان للتوثيق) | **مُصلَح** بـ4b3eebe0 |
| MEDIUM | R19 غير بوّابي في CI (قد ينكسر صمتًا مستقبلًا) | مقترح جاهز — قرار المالك |
| MEDIUM | ALERT-02/05/06 مؤكدة كوديًا وغير مُصلحة (سابقة، معروفة) | جولة إصلاح قادمة — قرار المالك |
| INFO | F2: صياغة عدّ النتائج | وُضّحت |
| INFO | parseTargets يُسقط المجهول | معروف — يُدار بترتيب النشر مع خيار A |

## هـ) ملحق TASK 22 — إعادة المراجعة المستقلة (2026-10-26 18:0x UTC)

**إعادة بناء وإثبات PR #10 @ `4b3eebe0` (من blobs الرأس مباشرة، 37+ استجابة خام في `evidence/raw/`):**

| البند | النتيجة | الدليل |
|---|---|---|
| رأس الـPR والسلسلة | open draft @ `4b3eebe0`؛ `b0e18219 → afa37b81 → 4b3eebe0`؛ والد الرأس = `afa37b81` | `raw/pr10_meta_t22.json` + `raw/pr10_head_commit_t22.json` |
| الملفات التسعة | كلها additions-only؛ `verify_manifest.py` (952 B) مضاف | `raw/pr10_files_t22.json` |
| MANIFEST↔الملفات | **8/8 entries MATCH** من blobs الرأس (9 = الملفات على الفرع؛ MANIFEST.json نفسه غير مسجَّل ذاتيًا) | `t22_digest.json` → manifest_check_t22 |
| كتلة `f1_correction` | موجودة في `remote_upload.f1_correction` | `t22_f1_verify_results.json` |
| UPLOAD_AND_HANDOFF.md (6,247 B) | يحمل أدلة حية فعلية (روابط PR/SHAs/طوابع تحقق API) لا مجرد وصف | `raw/UPLOAD_AND_HANDOFF_HEAD_FULL.md` |
| سلوك المُحقّق | إيجابي exit 0؛ حذف ملف/تزوير بايت/تزوير manifest ⇒ exit 1 لكل منها | `t22_f1_verify_results.json` |

**diff الإنتاجي وCI (إعادة تأكيد طازجة):**
- `ci.yml` بالبايت: `od -c` يثبت `branches: [main]` (المرة **الرابعة** لظاهرة العرض التي تبتلع `[m`) — sha256 `2a12a2e0…` مطابق؛ **لا خطوة regression** فيه ⇒ R21-01 قائم طازجًا.
- `package.json` scripts: لا `regression` ⇒ الرقعة المقترحة ما زالت ضرورية؛ واكتشاف N-1 (اعتماد `.smoke`) أُلحق برقعة v2.
- check-runs على main `76830a72`: 3 نجاحات منها **Workers Builds: tg-content-bot** (id 121409501944) — قيادة بحثية لـALERT-07 §A (خط بناء CF متصل؛ إثبات النشر يظل BLOCKED).
- `0eed7821` غائب (HTTP 422) — إعادة تأكيد طازجة.

**F2 (PATH-C) — ارتقاء إلى VERIFIED بايتيًا:**
- النسخ الثلاث `lib/core/` (hunt/shield/trade) موجودة بنيويًا (شجرة كاملة لكل مستودع) — `t22_f2_deep.json`.
- مصفوفة الهوية: `plans.ts` hunt=`3373648f…` shield=`da96c995…` trade=`661afcc6…` ⇒ **DIVERGED**؛ `i18n/ar.ts` الثلاث مختلفة؛ `i18n/en.ts` الثلاث مختلفة؛ `i18n/index.ts` متطابق `30d638cf…` — `t22_f2_identity.json`.
- `@vixor/contracts`: غائب (جذر packages = 4 حزم فقط؛ بحث شجرة كامل = صفر مسارات contract) — `t22_f1_verify_results.json`.

**جدول الشدات المحدّث:** يُضاف MEDIUM واحد — **N-1**: سكربت regression المقترح غير مستقل التشغيل (يتطلب أثر بناء `.smoke`)؛ العلاج جاهز برقعة v2 (قرار مالك). لا findings جديدة أخرى على PR #10 أو diff الإنتاجي في هذه الجولة.
