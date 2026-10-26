# ALERT-08 — سجل دليل مخطط الإنتاج القرائي (تاريخ التسجيل: 2026-10-26T23:4x–23:5x UTC (owner note dated 2026-10-27))

**الغرض:** تسجيل دليل المالك القرائي (تنفيذ الاستعلام المُعد سلفًا) بخصوص الأعمدة الأربعة على `public.meme_signals`، وتوثيق فحوص الاتساق التي أجراها المدقق **بدون** إعادة تنفيذ الاستعلام (لا قناة DB في بيئة التدقيق — وسبب حجب البند أصلًا).

---

## أ) الدليل كما ورد من المالك (حرفيًا، دون تعديل)

```
### ALERT-08 — Read-Only Schema Evidence Update
**Date:** 2026-10-27
**Status:** VERIFIED — Requested columns returned by read-only query; production project identity must be confirmed if not already documented.

**Evidence:** The supplied `information_schema.columns` query returned all four requested columns for `public.meme_signals`:
- `exit_reason`: `text`, nullable.
- `max_multiple`: `numeric`, nullable.
- `targets`: `jsonb`, nullable, default `'[]'::jsonb`.
- `updated_at`: `timestamp with time zone`, NOT NULL, default `now()`.

**Scope limitation:** This confirms the returned schema metadata for these four columns only. It does not independently establish the selected project's production identity, validate RLS or permissions, inspect row data, or prove application runtime behavior.

**Safety:** Read-only query only. No migrations, database writes, production code changes, merge, or deployment performed.

**Next:** Record the exact project identity through non-secret metadata if needed, then continue remaining audit checks. Keep the overall audit status `AUDIT INCOMPLETE` until all required checks are resolved. Preserve historical evidence and append this update without rewriting prior entries.
```

**ملاحظة التسجيل:** النص بلا أسرار؛ سُجل حرفيًا. النتيجة تقع في **الفرع الحميد** المُفسَّر سلفًا في ملف الاستعلام المُعد (`evidence/ALERT08_PREFLIGHT_READY_QUERY_2026-10-27.md`) — فرع «الأعمدة موجودة» وليس فرع `0 rows` الكارثي المفسَّر هناك.

## ب) تطابق الدليل مع الاستعلام المُعد سلفًا

الاستعلام المُعد في الحزمة يختار حرفيًا: `column_name, data_type, column_default, is_nullable` من `information_schema.columns` بشرط `table_schema='public' and table_name='meme_signals'` للأعمدة الأربعة نفسها. تقرير المالك يحمل **نفس الحقول الأربعة لكل عمود** (النوع + القابلية للفراغ + الافتراض لعمودَي `targets` و`updated_at`) — أي أن الدليل هو **تنفيذ للاستعلام المُعلن سلفًا** لا استعلام آخر.

## ج) فحوص الاتساق المستقلة (المدقق — بلا DB؛ سجل آلي: `t27_schema_consistency.json` خارجي)

| الفحص | النتيجة |
|---|---|
| تثبيت البايتات | الملفات الخمسة المفحوصة من شجرة main `2d8933ed…` طُوبقت بصمات git-blob (من المحتوى) مع الشجرة الحية — **تطابق كامل** |
| `updated_at` — مطابقة مباشرة ممكنة | تعريف repo SQL (`017_meme_signals.sql` سطر 45): `timestamptz NOT NULL DEFAULT now()` + trigger تحديث تلقائي (سطور 55-59) = **مطابق حرفيًا** لما أبلغ المالك من الإنتاج (نوعًا وفراغًا وافتراضًا) — فحص متقاطع حقيقي لا يحتاج قناة DB |
| `exit_reason` / `max_multiple` في SQL المستودع | **صفر** ذكر في **كل** ملفات SQL تحت `supabase/` في الشجرة الحية — يؤكد طازجًا ملاحظة المراجعة السطرية (§53): انحراف مستودع قائم |
| `targets` (العمود المجرّد) | غائب عن كل SQL المستودع (الموجود سابقًا `affiliate_links jsonb DEFAULT '[]'::jsonb` بنمط مشابه؛ و`targets_config` أيضًا غائب) |
| اتساق الأنواع مع الكود (`ath-monitor.ts`) | `targets` jsonb/`'[]'` افتراضيًا ↔ `parseTargets(s.targets)` مع fallback إلى `targets_config` عند الفراغ (سطور 336-337) — الافتراض `'[]'` هو بالضبط الشكل الذي يتوقعه الكود؛ `max_multiple` numeric ↔ `number \| string \| null` مع تطبيع قبل المقارنة (سطر 343)؛ `exit_reason` text ↔ كتابة قيم نصية قصيرة مثل `"tp"` (سطر 348)؛ أنواع الصف سطور 77-79 |
| ملاحظة مجاورة مسجلة بأمانة | أعمدة `extCols` المجاورة (`lang`, `persona`, `targets_config`, `pnl_style` — سطر 234) كلها غائبة عن SQL المستودع أيضًا — نفس نمط انحراف «المستودع يسبق الإنتاجَ تأخرًا» الموثق |

**خلاصة الاتساق:** لا يعارض أي فحص مستقل دليلَ المالك؛ وهناك مطابقة حرفية واحدة قابلة للتحقق بدون DB (`updated_at`). **هذا ليس إعادة تنفيذ للاستعلام** — الوجود الفعلي في الإنتاج يظل معتمدًا على دليل المالك القرائي ضمن نطاقه المعلن.

## د) حدود النطاق (كما نصّ المالك، ويؤكدها المدقق)

- الدليل يؤكد **بيانات وصف المخطط** لهذه الأعمدة الأربعة فقط.
- لا يثبت: **هوية مشروع الإنتاج** المُستعلم (بند تسجيل مفتوح — بيانات وصفية غير سرية)، ولا **RLS/الصلاحيات**، ولا محتوى الصفوف، ولا السلوك الحي للتطبيق.

## هـ) ما يغلق وما لا يغلق

1. **يُغلق (ضمن النطاق):** فرضية «أعمدة ناقصة في الإنتاج تُسقط حفظ حالة TP/SL بالكامل» — مُنبَّه عليها سلفًا كأخطر احتمال في ملف الاستعلام — **لا تتحقق**: الأعمدة الأربعة موجودة بأنواع متوافقة مع الكود.
2. **ALERT-08-ب (خيار A):** شرط الـpreflight المُعلن سلفًا تحقق بهذا الدليل؛ تبقى بوابات النشر قرار المالك (موافقة صريحة + ترتيب worker أولًا ثم migration) — لا migrations من المدقق إطلاقًا.
3. **لا يُغلق:** هوية المشروع (تسجيل)، RLS/الصلاحيات، ALERT-07 §A (النشر الفعلي وسبه الانقطاع الأصلي)، SEC-03، قرارات A/C وH1/H2.
4. **الحكم التراكمي يظل `AUDIT INCOMPLETE`.**
