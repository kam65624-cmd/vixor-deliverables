-- ============================================================================
-- VIXOR — P2-1: القناة التجريبية المعزولة + إعدادات بوابة الاستقبال
-- التنفيذ: Supabase → SQL Editor (idempotent — يمكن إعادة تشغيله بأمان)
--
-- ⚠️ قبل التشغيل استبدل قيمتين فقط:
--   PLACEHOLDER_TG_CHAT_ID       → معرف قناة الاختبار (يبدأ بـ -100…)
--   PLACEHOLDER_APPROVAL_CHAT_ID → معرف شات الموافقة
--      (أو احذف البند 4 كليًا للإبقاء على الضبط التلقائي من owner_ids
--       في myChatMember.ts:63-64)
--
-- ملاحظة حرجة: app_settings.ingest_channel_id يجب أن يكون **uuid لصف في
-- جدول channels** — وليس معرف تيليجرام. البند 3 أدناه يربطه تلقائيًا.
-- (المرجع: bot-worker/src/http/ingest.ts:223-233)
-- ============================================================================

-- 1) نيش اختبار (يُنشأ فقط إن لم يوجد)
insert into public.niches (name, slug)
select 'VIXOR Test', 'vixor-test'
where not exists (select 1 from public.niches where slug = 'vixor-test');

-- 2) صف القناة التجريبية (نشط) — استبدل PLACEHOLDER_TG_CHAT_ID
insert into public.channels (niche_id, tg_chat_id, tg_username, title, is_active)
select n.id, 'PLACEHOLDER_TG_CHAT_ID', null, 'VIXOR Test Channel', true
from public.niches n where n.slug = 'vixor-test'
on conflict (tg_chat_id) do update
  set is_active = true, niche_id = excluded.niche_id, updated_at = now();

-- 3) ربط بوابة الاستقبال بصف القناة (uuid تلقائيًا — لا تدخل يدويًا هنا)
insert into public.app_settings (key, value)
select 'ingest_channel_id', to_jsonb(c.id::text)
from public.channels c
where c.tg_chat_id = 'PLACEHOLDER_TG_CHAT_ID'
on conflict (key) do update set value = excluded.value, updated_at = now();

-- 4) شات الموافقة — استبدل PLACEHOLDER_APPROVAL_CHAT_ID أو احذف هذا البند
insert into public.app_settings (key, value)
values ('approval_chat_id', '"PLACEHOLDER_APPROVAL_CHAT_ID"'::jsonb)
on conflict (key) do update set value = excluded.value, updated_at = now();

-- ============================================================================
-- تحقق فوري بعد التشغيل (شغّل هذه الاستعلامات وتأكد من النتائج):
-- ============================================================================

-- أ) القيمتان مثبتتان:
select s.key, s.value from public.app_settings s
where s.key in ('ingest_channel_id', 'approval_chat_id');

-- ب) القناة المرتبطة موجودة ونشطة (يجب أن يرجع صفًا واحدًا is_active = true):
select c.id, c.tg_chat_id, c.title, c.is_active
from public.channels c
where c.id::text = (select value#>>'{}' from public.app_settings where key = 'ingest_channel_id');
