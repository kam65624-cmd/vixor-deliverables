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
