# VIXOR — عدة الإعداد الحي (P2-0 + بوابة P2-1): السر والإعدادات ثم تدوير المفاتيح

> **التاريخ:** 2026-10-21 | **المرجع:** خطة المرحلة 2 (`PHASE2_TASKS_PLAN_AR.md`)
> **قاعدة السر:** لا يُولَّد أو يُمرَّر أو يُطبع أي سر في هذه المحادثة — كل ما يلي يُنفَّذ على جهازك أو في لوحات التحكم مباشرة.
> **كل الأسماء أدناه متحقق منها من الكود المدموج** (`tg#14`, `tg#13`) — ليست افتراضات.

---

## 0) الحقائق المتحقق منها من الكود (اقرأها قبل التنفيذ)

| البند | القيمة الفعلية | المصدر في الكود |
|---|---|---|
| اسم الـ Worker | `tg-content-bot` | `bot-worker/wrangler.toml` |
| اسم سر الـ ingest | `INGEST_HMAC_SECRET` | `src/http/ingest.ts:135` — غير مضبوط → **503** fail-closed |
| صيغة التوقيع | HMAC-SHA256 على `"{ts}:{body}"` في `x-vixor-signature` + `x-vixor-timestamp` (±5 دقائق) | `src/http/ingest.ts:155` |
| `ingest_channel_id` | **uuid لصف في جدول `channels`** — وليس معرف تيليجرام `-100…` | `src/http/ingest.ts:223–228` (`getChannelById`) |
| شرط القناة | صف `channels` موجود و`is_active = true` وإلا **503** | `src/http/ingest.ts:229–233` |
| `approval_chat_id` | معرف شات تيليجرام كنص JSON — يُضبط تلقائيًا من `owner_ids[0]` إن غاب | `src/telegram/handlers/myChatMember.ts:63–64` |
| شكل `app_settings` | `(key text pk, value jsonb)` — القيمة نص JSON | `migrations/001_schema.sql:27` |
| سكربت الإرسال (Hunt) | `emit-test-opportunity.mjs --target <url> --secret <s> [--dry-run]` | `vixor-hunt/scripts/` |

> **الخطأ الأكثر شيوعًا (تجنّبه):** وضع معرف التيليجرام في `ingest_channel_id`. الصحيح: uuid صف القناة — ملف `setup_app_settings.sql` أدناه يعمل هذا تلقائيًا.

---

## 1) المتطلبات المسبقة (5 دقائق)

1. **قناة تيليجرام اختبار معزولة** منشأة (خاصة)، والبوت **مشرفًا فيها** بصلاحية النشر.
2. **شات موافقة** (يمكن شاتك الخاص مع البوت — يُضبط تلقائيًا — أو مجموعة اختبار والبوت مشرفًا فيها).
3. `wrangler` مثبت ومسجَّل دخول: `npm i -g wrangler && wrangler login` (نفس حساب Cloudflare صاحب الـ Worker).
4. وصول SQL Editor في Supabase.
5. استنساخ حديث لـ `tg-content-bot` بعد دمج `tg#14` — **أو** التنفيذ من أي نسخة لأن الخطوات أدناه كلها CLI/SQL لا تعتمد على نسخة محلية سوى موقع الملفات.

---

## 2) الخطوة 1 — توليد وتثبيت `INGEST_HMAC_SECRET` (بدون عرضه أبدًا)

**الطريقة أ (الموصى بها):** شغّل السكربت المرفق `setup_ingest_secret.sh`:

```bash
cd tg-content-bot/bot-worker
bash /path/to/setup_ingest_secret.sh   # انسخ السكربت بجوار مجلد bot-worker وشغّله
```

ما يفعله: يولّد `openssl rand -hex 32` (256-بت) ويُمرِّره **مباشرة عبر pipe** إلى `wrangler secret put INGEST_HMAC_SECRET` — لا يُطبع ولا يُحفظ في أي ملف.

**الطريقة ب (بلا تيرمينال):** Cloudflare Dashboard → Workers & Pages → `tg-content-bot` → Settings → Variables & Secrets → Add → type **Secret** → الاسم `INGEST_HMAC_SECRET` والقيمة من **مولّد كلمات مرور** في مدير كلمات مرورك (64 حرفًا hex).

> ⛔ **لن أضع قيمة جاهزة هنا عمدًا** — أي سر يمرّ بمحادثة يصبح مُحرَقًا مثل PAT الذي سنلغيه اليوم. هذا بالضبط درس P2-0.

**تحقق فوري:** بعد التثبيت، الطلب التالي يجب أن يرجع **403** (وليس 503) — 403 يعني السر مضبوط والبوابة الحية ترفض غير الموقّع:

```bash
curl -s -o /dev/null -w "%{http_code}\n" -X POST \
  "https://tg-content-bot.<YOUR_CF_SUBDOMAIN>.workers.dev/ingest/signal" \
  -H "content-type: application/json" -d '{}'
# المتوقع: 403 (توقيع مفقود) — لو 503 فالسر لم يُثبَّت بعد
```

---

## 3) الخطوة 2 — القناة التجريبية والإعدادات (SQL واحد idempotent)

افتح **Supabase → SQL Editor** وشغّل ملف `setup_app_settings.sql` المرفق بعد استبدال قيمتين:

- `PLACEHOLDER_TG_CHAT_ID` → معرف قناة الاختبار (يبدأ بـ `-100…`) — تحصل عليه بإرسال رسالة في القناة ثم `getUpdates` أو عبر `@userinfobot` بإعادة توجيه الرسالة.
- `PLACEHOLDER_APPROVAL_CHAT_ID` → معرف شات الموافقة (**احذف البند 4 من الملف** لو تريد الإبقاء على الضبط التلقائي من `owner_ids`).

الملف ينفذ بالترتيب: نيش اختبار (إن غاب) → صف قناة `is_active=true` → ربط `ingest_channel_id` بـ **uuid** الصف تلقائيًا → `approval_chat_id`.

**تحقق فوري:**

```sql
select s.key, s.value
from app_settings s where s.key in ('ingest_channel_id','approval_chat_id');
-- ثم: يجب أن يرجع الصف التالي قناة نشطة:
select c.id, c.is_active from channels c
where c.id::text = (select value#>>'{}' from app_settings where key='ingest_channel_id');
```

---

## 4) الخطوة 3 — التدرج الحي حتى إثبات T1 (بعد دمج `tg#14` والنشر)

نفّذ بالترتيب وتوقف عند أول نتيجة غير متوقعة:

| # | الأمر | المتوقع | يثبت |
|---|---|---|---|
| 1 | `curl` بلا توقيع (أعلاه) | **403** | البوابة حية وfail-closed |
| 2 | `node scripts/emit-test-opportunity.mjs --dry-run` | عرض `idempotency_key` و`event_id` | الحمولة حتمية |
| 3 | `node scripts/emit-test-opportunity.mjs --target <worker-url>/ingest/signal --secret <السر من مدير كلماتك>` | **202** | الاستقبال والتقييم والتخزين |
| 4 | افتح شات الموافقة | draft بلوحة أزرار | القناة = `ingest_channel_id` فقط (§4) |
| 5 | اضغط موافقة | **رسالة واحدة** في قناة الاختبار | دورة النشر كاملة (T1) |
| 6 | كرر الأمر 3 حرفيًا | **409** بلا رسالة ثانية | idempotency حي (T2) |

> السر في الخطوة 3 يُمرَّر كوسيط سطر أوامر على جهازك فقط — لا في أي محادثة. بعدها نظّف سجل التيرمينال `history -c` لو تشارك الجهاز.

---

## 5) الخطوة 4 — تدوير بقية المفاتيح P2-0 (بنودك وحدك، 30–45 دقيقة)

نفّذها بهذا الترتيب، وقبل كل تدوير: لا شيء في الجلسة الحالية يحتاج PAT بعد الآن.

| # | السر (الاسم الفعلي في الكود) | مسار التدوير | تحديث الـ Worker بعد التدوير |
|---|---|---|---|
| 1 | **PAT GitHub** | `github.com/settings/tokens` → حذف التوكن الحالي | لا شيء — إن احتجت توكنًا جديدًا أنشئه بنطاق `repo` ومدة ≤30 يومًا |
| 2 | `TELEGRAM_BOT_TOKEN` | `@BotFather` → `/mybots` → البوت → API Token → **Revoke current token** | `cd bot-worker && wrangler secret put TELEGRAM_BOT_TOKEN` ثم أعد `setWebhook` بالتوكن الجديد |
| 3 | `TELEGRAM_WEBHOOK_SECRET` | ولّد جديدًا محليًا: `openssl rand -hex 32` (لا ترسله لأحد) | `wrangler secret put TELEGRAM_WEBHOOK_SECRET` + مرّر نفس القيمة في `secret_token` عند `setWebhook` |
| 4 | `SUPABASE_SERVICE_KEY` | Supabase → Project Settings → API → **Rotate** service_role | `wrangler secret put SUPABASE_SERVICE_KEY` + حدّث أي متغير بنفس القيمة في vixor-APP |
| 5 | anon key (للـ APP) | نفس الصفحة → Rotate anon | حدّث متغيرات البيئة في vixor-APP |
| 6 | `ANTHROPIC_API_KEY` (إن كان مستخدمًا ومكشوفًا) | console.anthropic.com → API Keys → Create/Revoke | `wrangler secret put ANTHROPIC_API_KEY` |
| 7 | مفاتيح Cloudflare API (إن وُجدت للنشر الآلي) | dash.cloudflare.com → My Profile → API Tokens → **Roll** | حدّث أسرار GitHub Actions إن كانت مستخدمة |

**تحقق ما بعد التدوير (كلها يجب أن تنجح):**
- إرسال `/start` للبوت → يرد (توكن تيليجرام الجديد شغال).
- رسالة في القناة المصدر → تصل وتُسجَّل في `telegram_updates` (الويبهوك + `TELEGRAM_WEBHOOK_SECRET` الجديد شغالان).
- تشغيل الخطوات 3–6 من القسم 4 → نفس النتائج (Supabase الجديد شغال عبر الـ Worker).

---

## 6) حالة الإقفال

| البند | المسؤول | الحالة قبل | الحالة بعد التنفيذ |
|---|---|---|---|
| توليد `INGEST_HMAC_SECRET` | أنت (سكربت/داشبورد) | ⏳ | ✓ البوابة ترجع 403 |
| `app_settings.ingest_channel_id` + `approval_chat_id` | أنت (SQL مرفق) | ⏳ | ✓ استعلام التحقق يرجع قناة نشطة |
| تدوير المفاتيح السبعة | أنت | ⏳ | ✓ تحقق ما بعد التدوير ناجح |
| مراجعة ودمج PRs المرحلة 1 | أنت | ⏳ | ✓ main يحمل M1–M4 |
| إعادة النشر + تشغيل T1 الحي | نحن معًا | ⏳ | ✓ 202 → موافقة → رسالة واحدة → 409 |

أول ما تنهي البنود الأربعة الأولى أعلاه، ننتقل معًا إلى إعادة النشر وتشغيل T1 الحي، وبعدها تُعلن المرحلة 1 مغلقة رسميًا ونبدأ P2-2 (تدقيق صلاحيات DB) ثم P2-5 (دورة الإيراد).
