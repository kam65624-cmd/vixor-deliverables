# PHASE0_BASELINE.md — تثبيت حالة البداية (TASK 23 — إصلاح حزمة PR #11 + ربط R19)

**وقت التثبيت:** 2026-10-26T21:01–21:12 UTC (بيئة التنفيذ UTC صرفًا — انظر REPOSITORY_STATUS §6 لتسمية «2026-10-27»).
**قاعدة المرحلة:** لا كتابة قبل التثبيت؛ كل الأرقام أدناه مجلوبة حيًّا من GitHub API هذه الجلسة، لا من نصوص قديمة داخل الحزمة.

## 1) قناة الوصول (دون أي قيمة سرية)

| البند | القيمة |
|---|---|
| التوكن | صالح — ملفي 0600 من الحجم الدائم (`gh_api.py` يقرؤه داخليًا ولا يطبعه أبدًا) |
| الهوية | `kam65624-cmd` (GET /user → 200) |
| صلاحية الدفع | `push=true` + `maintain=true` على **كلا** المستودعين (vixor-deliverables العام + tg-content-bot الخاص) |
| الحدود | **لا دمج لأي PR، لا تغيير حالة PR، لا force-push، لا migrations، لا deploy، لا طباعة أسرار** — بوابة المالك باقية |

## 2) حالة PR #10 (الأصل الوحيد الذي تغيّر منذ TASK 22)

| الحقل | القيمة الحية | المصدر |
|---|---|---|
| state | **closed** | `evidence/raw/t23_pr10.json` |
| merged | **true** | نفسه |
| merged_at | **2026-10-26T20:52:59Z** | نفسه |
| merged_by | `kam65624-cmd` (المالك بنفسه) | نفسه |
| merge_commit_sha | **`01b8b9471f68f836994b060e3cf5027b579aea10`** | نفسه |
| head المدموج | `4b3eebe0e6033431ec6819cd9b0e303dec5a8a0c` (نسخة TASK 21 بعد إصلاح F1 — كما هو) | نفسه |

**الدلالة:** قرار الدمج (بند 2 في OWNER_ACTIONS) **أُنجز بواسطة المالك** — حزمة الأدلة `final-evidence-handoff/2026-10-26/` صارت جزءًا من `main` في vixor-deliverables. هذا **تصحيح حالة لا إغلاق مخاطر**: لا بند أمني/إنتاجي يُغلق بدمج حزمة توثيق (التفصيل: ملحقات TASK 23 في كل تقرير).

## 3) حالة PR #11 (نطاق عمل TASK 23)

| الحقل | القيمة الحية | المصدر |
|---|---|---|
| state / draft | **open / true (مسودة — تظل مسودة)** | `evidence/raw/t23_pr11.json` |
| head | `d1004b796ae27496e04d78db6c9c69dc6341a37a` @ `audit/final-audit-package-2026-10-26-task22` | نفسه |
| base | `bd3fbe3ad565d165b0a16d289481fed432497393` (main) | نفسه |
| changed_files | 68 (كلها إضافات تحت `final-audit-2026-10-27/`) | `evidence/raw/t23_pr11_files.json` |
| ملاحظة | main تحرك بعد إنشاء الفرع (دمج PR #10) — الفرع متأخر عن main بـcommit الدمج؛ لا تعارض محتمل (PR #10 أضاف `final-evidence-handoff/2026-10-26/` فقط) | REPOSITORY_STATUS ملحق TASK 23 |

## 4) أحدث main في كلا المستودعين

| المستودع | HEAD الآن | آخر حركة |
|---|---|---|
| kam65624-cmd/tg-content-bot | **`76830a721bb3761a6d25309acc3672b117116994`** (بلا تغيير منذ دمج PR #18) | 2026-10-26T05:11:36Z |
| kam65624-cmd/vixor-deliverables | **`01b8b9471f68f836994b060e3cf5027b579aea10`** (= merge commit لـPR #10) | 2026-10-26T20:52:58Z |

## 5) الملفات المرجعية المجلوبة من SHA الرئيسي (لا نسخ محلية قديمة)

مجلوبة عبر contents API على `76830a72` وحُفظت خامًا في `evidence/raw/`:

| الملف | bytes | sha256 | ملاحظة |
|---|---|---|---|
| `bot-worker/package.json` | 700 | `48c730481f40c79c…` | **لا سكربت regression** — R21-01 قائم على HEAD الحي |
| `.github/workflows/ci.yml` | 1,011 | `2a12a2e05a9bd27c…` | مطابق لسجل 16-H بايتيًا؛ خطوتان فقط (typecheck+test) بلا regression |
| `bot-worker/tests/alert01-regression.cjs` | 32,092 | blob `52e835c95390…` | موجود — المسار الفعلي `bot-worker/tests/` (المحاولة على `tests/` الجذر أعادت 404 وموثقة) |

check-runs على main `76830a72` (إعادة تأكيد طازجة): الثلاثة كلها success — `bot-worker (typecheck + smoke tests)` id 121409406883، `mini-app (typecheck)` id 121409407075، `Workers Builds: tg-content-bot` id 121409501944 (`evidence/raw/t23_phase0b_summary.json`).

## 6) تطابق نسخة العمل مع head البعيد (شرط العمل على «فرع PR #11 الحالي»)

- استنساخ طازج: `work/vixor-deliverables` @ `d1004b79` (الوالد `bd3fbe3a` مؤكد).
- تطابق بايتي ثلاثي المصادر لملفات المفتاح (API ↔ clone ↔ مرآة TASK 22 المحلية): `verify_manifest.py` `4d42a209…`، `MANIFEST.json` `f568357da0…`، `R19_CI_WIRING_PROPOSAL_v2_amended.patch` `00f1618e…` — **MATCH** للثلاثة.
- شجرة head كاملة: 89 blob (68 إضافة الحزمة + محتوى main الأساسي) — `evidence/raw/t23_pr11_head_tree.json`.

## 7) الأدوات والبيئة

git 2.47.3 · node v24.21.0 · npm 11.x · Python 3.12.15 · jq/curl/zip/unzip متوفرة · `gh` CLI غائب (غير ضروري — كل شيء عبر API/‏git مع القناة الملفية).

## 8) ما لا يزال محجوبًا عند نقطة البداية هذه (بذاعة)

SEC-03 (التدوير قرار مالك — التوكن نفسه ما زال يعمل)، ALERT-08 preflight (لا قناة DB إنتاج)، ALERT-07 §A (لا صلاحيات Cloudflare). لا شيء منها يُغلق بحزمة TASK 23.
