# REPRODUCIBILITY.md — خطوات إعادة إنتاج كل نتيجة (TASK 21، 2026-10-27)

**متطلب عام:** توكن GitHub ‏بصلاحية repo ‏على `kam65624-cmd` (يُقرأ من ملف 0600 خارج المستودعات — لا يُطبع أبدًا). سكربت المساعد: `scripts/gh_api.py` ‏يقرأ التوكن من `/tmp/my-project/scripts/.cred/git-cred.txt` (بنية git-credential-store: ‏password= ‏في سطر).

## 1) التحقق البايتي لحزمة PR #10 (F1)

```bash
# 9/9 MATCH — إما بالمحقق الذاتي المرفوع نفسه (بعد استنساخ/تنزيل المجلد):
python3 final-evidence-handoff/2026-10-26/verify_manifest.py     # exit 0
# أو عبر API مباشرة (كما فعلنا):
python3 - <<'PY'
import sys, hashlib, json
sys.path.insert(0, "scripts"); from gh_api import api, get_blob_sha256
R="kam65624-cmd/vixor-deliverables"; P="final-evidence-handoff/2026-10-26/"
st,t=api(f"/repos/{R}/git/trees/4b3eebe0e6033431ec6819cd9b0e303dec5a8a0c?recursive=1")
b={e["path"]:e["sha"] for e in t["tree"] if e["type"]=="blob"}
m=json.loads(get_blob_sha256(R,b[P+"MANIFEST.json"]))["package_files"]
print(all((lambda x: len(x)==m[n]["bytes"] and hashlib.sha256(x).hexdigest()==m[n]["sha256"])(get_blob_sha256(R,b[P+n])) for n in m))
PY
```

## 2) R20–R22 ‏(تزامن حقيقي — PostgreSQL ‏17.10 ‏ثنائيات)

```bash
cd r22pg && npm install pg@8 embedded-postgres@17.10.0-beta.17 --no-audit --no-fund
node r22_real_pg.js run1   # 6/6، exit 0  (اللوج: test-evidence-r22_run1_2026-10-27.log)
node r22_real_pg.js run2   # 6/6، exit 0  (الثبات)
```
- المعزولة: datadir ‏مؤقت `r22pg/data-r22` (يُنشأ من جديد كل تشغيل)، 127.0.0.1:54329 فقط، صفر صلة بالإنتاج.
- المواصفات حرفيًا من `download/alert01-atomic/psql_concurrency_harness.sh`؛ التكيفات موثقة برأس `r22_real_pg.js`.

## 3) R19 ‏+ ‏smoke ‏+ typecheck ‏على main المدموج

```bash
python3 - <<'PY'   # تنزيل الشجرة الرسمية بالتوكن (tarball) — SHA مثبت بالـAPI قبلها
# (الكود المستخدم محفوظ في سجل الجلسة؛ المخرج: audit3/tg-content-bot @ 76830a72)
PY
cd audit3/tg-content-bot/bot-worker
npm ci --no-audit --no-fund
npx tsc -p tests/smoke.tsconfig.json
node tests/alert01-regression.cjs     # 20/20 — R19 ‏أخضر
npm test                              # 86/86
npm run typecheck                     # exit 0
```
اللوج المرجعي: `test-evidence-r19_fresh_main_2026-10-27.log`.

## 4) تحققات الـAPI ‏الحية (مستودعات/PRs/CI/blobs)

```bash
python3 scripts/task6_repo_audit.py          # يكتب pr10-review/repo_audit_live_2026-10-27.json
# نقاط محددة:
#  - blobs main: GET /repos/kam65624-cmd/tg-content-bot/contents/<path>?ref=main → sha == eb5da95b…/52e835c9…
#  - PR #17/#18: merged=true + merge_commit 944e60c0/76830a72
#  - CI: GET /actions/runs → runs 40272909018/40272857668/40271520067 success
#  - ci.yml بايتيًا: branches: [main] (sha256 2a12a2e0…) — لا تثق بالعرض المطبوع
```

## 5) فحص أسرار الحزمة (نفس النتيجة: نظيف)

أنماط `ghp_/gho_/github_pat_/AKIA/JWT/three-part/postgres://user:pass@/BEGIN PRIVATE KEY/…` على ملفات PR #10 ‏التسعة + جواب الـPR — `pr10-review/secret_scan.json` (سالب كامل).

## 6) ملاحظات إعادة إنتاج

- كل الأوامر أعلاه قراءة-فقط على GitHub ‏(GET) عدا خطوة §1 الاختيارية عبر verify_manifest ‏(محلي) — وخطتا §2/§3 ‏تنفذان كودًا محليًا معزولًا.
- أي إعادة توليد للـMANIFEST ‏يجب أن تكون **آخر خطوة** بعد تجميد الملفات (درس F1/R21-02).

## 7) ملحق TASK 22 — أوامر الجولة الطازجة (كلها نُفذت فعليًا 2026-10-26 18:0x UTC)

```bash
# (أ) الجلب الحي المعتمد — PR #10 + المستودعات التسعة + CI + blobs (توكن ملفي، GET فقط):
python3 scripts/t22_fresh_fetch.py          # → download/task22-verification/raw/*.json + t22_digest.json

# (ب) إثبات F1 وسلوك المُحقّق (إيجابي + 3 اختبارات سلبية):
python3 scripts/t22_f1_verify.py            # → t22_f1_verify_results.json (exit 0/1/1/1)

# (ج) R20–R22 جولة ثالثة + R19 طازج على main المدموج (معزول بالكامل):
bash scripts/t22_fresh_reruns.sh
#   ملاحظة ترتيب حاسمة: شغّل 'npm test' قبل alert01-regression.cjs من شجرة نظيفة
#   (regression يستهلك أثر بناء .smoke — اكتشاف N-1 موثق داخل اللوج نفسه بصدق)

# (د) F2: نسخ core الثلاث ومصفوفة الهوية بblob SHAs:
python3 scripts/t22_f2_core_check.py && python3 scripts/t22_f2_deep.py && python3 scripts/t22_f2_identity.py

# (هـ) تحقق الحزمة نفسها (MANIFEST.json داخل هذا المجلد):
python3 verify_manifest.py                   # exit 0 = كل الملفات المسجلة MATCH
```

- كل الطوابع أعلاه UTC؛ مصدر تسمية «2026-10-27» = ساعة منصة الجلسة (التفصيل: REPOSITORY_STATUS §6).
- لا خطوة من هذه الجولة كتبت على أي مستودع (GET فقط) باستثناء خطوات معزولة محلية (PG مؤقت + tarball إلى مجلد عمل مؤقت).

# ملحق TASK 23 — إعادة إنتاج تحقق الحزمة v3 وZIP (2026-10-26T21:2x UTC)

## (أ) تحقق الحزمة نفسها (بعد كل تعديلات TASK 23)

```bash
# داخل جذر الحزمة (المجلد الذي يحوي هذا الملف):
python3 verify_manifest.py
# exit 0 = PASS — تغطية كاملة مثبتة (كل ملف على القرص مسجل/مستثنى صراحة/المانيفست نفسه)
# exit 1 = أي فشل (مفقود/إضافي/معدل/غير آمن/أنواع خاطئة/تكرار) — v3 يفحص الجرد الكامل لا المسجل فقط
```

## (ب) اختبارات المُحقق المستقلة (10 سيناريوهات سلبية/إيجابية)

```bash
python3 verify_manifest_tests.py
# ينشئ نسخًا حقيقية من الحزمة في /tmp، يعدّل كل نسخة بايتيًا بطريقة محددة،
# يشغّل المُحقق الحقيقي ويتحقق من exit code المتوقع — exit 0 للسويتش = 10/10
# اللوج الكامل بالنسخ: evidence/t23_verifier_tests_output.log
```

## (ج) تحقق ZIP النهائي (نسختان: محليّة + على فرع PR #11)

```bash
# 1) بصمة النسخة المرفوعة على فرع PR #11 قارنها بالقيم الموثقة خارجيًا
#    (وصف PR #11 + t23_zip_record.json بجوار الـZIP على جذر الفرع) —
#    بصمة ZIP لا يمكن أن تُسجل داخل الحزمة نفسها (استحالة ذاتية: الـZIP يُبنى بعد التجميد)
unzip VIXOR_FINAL_AUDIT_PACKAGE_2026-10-26_task23.zip -d /tmp/t23_check
python3 /tmp/t23_check/final-audit-2026-10-27/verify_manifest.py /tmp/t23_check/final-audit-2026-10-27
# exit 0 = النسخة المستخرجة سليمة (أُثبت مسبقًا بهذا المسار بالضبط)
# 2) بديل دائم بلا ZIP: أرشيف GitHub المصدر للـcommit النهائي لفرع PR #11
#    https://github.com/kam65624-cmd/vixor-deliverables/archive/<full-head-sha>.tar.gz
#    (أرشيف مصدر GitHub — ليس نفس ZIP المخصص ولا يُدّعى كذلك؛ تحقق MANIFEST يعمل داخله أيضًا)
```

## (د) إعادة إنتاج اختبارات R19 على الفرع الإنتاجي (PR #19 — مسودة)

```bash
git clone https://github.com/kam65624-cmd/tg-content-bot.git
cd tg-content-bot && git checkout 8d45f22eba3c598e451139fdeed6c1a29c938d0c
cd bot-worker
npm ci && npm run regression && npm run typecheck && npm test
# الترتيب أعلاه متعمد: regression قبل أي build يثبت استقلالية v2 (يبني .smoke بنفسه)
# النتائج المرجعية: 20/20 + نظيف + 86/86 (exit 0 للجميع) — evidence/test-evidence-r19_task23_clean_checkout.log
# CI الفعلي: run 40404172527 على head 8d45f22 (خطوة ALERT-01 regression completed/success)
```

- كل الطوابع UTC. لا خطوة من TASK 23 كتبت على main أو دمجت أي PR أو شغلت migrations.
- ملاحظة بنيوية: سجلات التحقق النهائي (على الحزمة المجمدة نفسها) وُلّدت بعد التجميد فلا يمكن أن تكون داخل الحزمة بتعريفها — تُحفظ بجوار الحزمة على فرع الـPR (لوجات t23_verify_*.log) بينما اختبارات السلوك العشرة (التي تشمل نسخة سليمة→PASS) داخل الحزمة كأدلة مكافئة.


## ملحق TASK 25 — إعادة بناء وتحقق T24-01 خطوة بخطوة (2026-10-26T22:3x–23:0x UTC)

**المدخلات:** أصول الحزمة كما في الأقسام أعلاه، مع: (أ) سجل التنقيح `evidence/T24_01_REDACTION_LOG.json`، (ب) سكربتات مُثبتة: `t25_redact.py` (تنقيح) و`t25_build_package.py` (بناء/تحقق) و`t25_push_pr11.py` (رفع fast-forward) في أدلة السكربتات الخارجية المرافقة للتقرير.

**خطوات إعادة البناء بالترتيب (manifest-last):**
1. تنقيح: تحقق أن بايتات الملفات الثمانية مطابقة لما سُجل في MANIFEST v3 → حفظ الأصل محليًا (حجر صحي، لا يُنشر) → إزالة القيم (سلاسل فارغة) عند المواضع المضبوطة → فحوص لاحقة (صفر قيم متبقية، صلاحية JSON، فارق البايتات = طول القيمة).
2. بناء: نسخ الأدلة الجديدة إلى `evidence/` → توليد MANIFEST v4 (بعد كل التعديلات) → تشغيل المدقق exit 0 → تشغيل مصفوفة الاختبارات 10/10 (يُكتب لوجها داخل الحزمة) → إعادة توليد MANIFEST (r2-final) → ZIP → استخراج نظيف → المدقق داخل المستخرَج exit 0 → الاختبارات داخل المستخرَج 10/10.
3. فحص الأسرار المستقل على bytes الـZIP النهائي: أنماط v3 + نمط جديد لأي قيمة غير فارغة لحقل `temp_clone_token` — النتيجة CLEAN بعد نفس الإفرادات الأربعة الموثقة (placeholder توثيقي حرفي).
4. رفع fast-forward إلى فرع PR #11 (blobs → tree على أساس شجرة الفرع الحالية → commit واحد → تحديث ref دون قوة) → تحديث وصف PR بقيم ZIP الجديدة.
5. **قاعدة ثابتة:** لا تُكتب بصمة ZIP داخل الحزمة أبدًا (استحالة self-reference) — تُسجل في وصف PR وفي سجل خارجي بجوار الـZIP.

**فروقات الإصدار السابق:** 8 ملفات منقحة (بصمات قبل/بعد في سجل التنقيح) + MANIFEST.json (v3→v4) + 5 ملفات جديدة (سجل تنقيح، فحص توكن، ملخص عدّ، لوج اختبارات، تقرير جذر) + ملاحق توثيقية مؤرخة في 5 ملفات قائمة — **كل ما عدا ذلك مطابق بايتيًا** (سجل مقارنة آلي في الأدلة الخارجية).


## ملحق TASK 26 — إعادة إنتاج تحقق دليل ALERT-01 خطوة بخطوة (2026-10-26T23:3x–23:5x UTC (owner note dated 2026-10-27))

**الهدف:** إعادة إنتاج قناتي التحقق المستقلتين لادعاء المالك (`ALERT-01 regression: 20 passed, 0 failed` على R1–R19) وبناء الحزمة v5.

**قناة أ — دليل CI على main المدموج:**
1. `GET /repos/kam65624-cmd/tg-content-bot/actions/runs?per_page=10` → حدد run 40416117388 (head `2d8933ed…`, push, success).
2. `GET /repos/…/actions/runs/40416117388/jobs` → job «bot-worker (typecheck + smoke tests)».
3. نزّل لوج الـjob (نقطة النهاية تعيد توجيهًا 302 إلى URL موقع — **احذف ترويسة Authorization عند التحويل**) وابحث عن السطر الحرفي `=== ALERT-01 regression: 20 passed, 0 failed ===` ومجموعة `Run npm run regression`.

**قناة ب — إعادة تشغيل محلية مثبتة البايتات (git محجوب في بيئة التدقيق):**
1. نزّل tarball الالتزام: `GET /repos/…/tarball/2d8933ed7cd92d23144099642497f32794340715` واستخرجه في دليل نظيف.
2. ثبت البايتات: احسب git-blob sha1 من المحتوى (`sha1("blob <len>\0" + bytes)`) لأربعة ملفات مفتاحية وقارنها بأشجار API الحية — يجب التطابق (`package.json` = `7a2c289d…`، `alert01-regression.cjs` = `52e835c9…`، `ci.yml` = `e18c7cb4…`، `smoke-test.cjs` = `f409aa5f…`).
3. في `bot-worker/`: `npm ci` → `npm run regression` **قبل أي بناء** (`.smoke` غائب — إثبات الاكتفاء الذاتي v2) → `npm run typecheck` → `npm test` (smoke 86/0) → `npm run regression` بعد البناء. المتوقع: كل الأكواد 0، والانحدار 20/0 في المرهين.
4. عزل النطاق: `GET /repos/…/compare/76830a72…2d8933ed…` → ملفان فقط (`ci.yml` +2/−0، `package.json` +2/−1).

**بناء الحزمة v5 (نفس قواعد TASK 25):** مزامنة النسخ المحلية مع main الحي (ملفات PR #12 من blobs الحية) → ملاحق TASK 26 + 3 ملفات جديدة → MANIFEST v5 (r1 → اختبارات 10/10 داخل الحزمة → r2-final) → مدقق exit 0 → ZIP → استخراج نظيف → مدقق + اختبارات داخل المستخرَج → فحص أسرار مستقل (CLEAN بعد الإفرادات الموثقة) → سجل مقارنة آلي task25→task26 → رفع بـblobs→tree→commit→ref على فرع جديد فوق main (fast-forward بنيويًا؛ لا قوة) → فتح PR مسودة (لا دمج).

**سكربتات مثبتة:** `t26_phase0.py` / `t26_phase0b.py` / `t26_phase0c.py` / `t26_clean_checkout.py` / `t26_rerun.sh` / `t26_sync_main.py` / `t26_docs_append.py` / `t26_build_package.py` / `t26_push_pr11.py` في أدلة السكربتات المرافقة للتقرير الخارجي.
