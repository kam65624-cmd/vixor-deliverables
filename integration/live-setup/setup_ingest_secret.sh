#!/usr/bin/env bash
# VIXOR — P2-0: توليد وتثبيت INGEST_HMAC_SECRET دون عرضه أو حفظه في أي مكان.
# الاستخدام: انسخ هذا الملف بجوار مجلد bot-worker في استنساخ tg-content-bot ثم:
#   bash setup_ingest_secret.sh
# المتطلب: wrangler مثبت ومسجل دخول بنفس حساب Cloudflare صاحب الـ Worker (tg-content-bot).
set -euo pipefail

# انتقل إلى مجلد bot-worker حيث wrangler.toml (اسم الـ Worker: tg-content-bot)
if [ -f "bot-worker/wrangler.toml" ]; then
  cd bot-worker
elif [ ! -f "wrangler.toml" ]; then
  echo "خطأ: شغّل السكربت من جذر استنساخ tg-content-bot أو من داخل bot-worker." >&2
  exit 1
fi

command -v wrangler >/dev/null 2>&1 || {
  echo "wrangler غير مثبت:  npm i -g wrangler && wrangler login" >&2
  exit 1
}
command -v openssl >/dev/null 2>&1 || { echo "openssl مطلوب." >&2; exit 1; }

echo "→ توليد سر عشوائي 256-بت وتمريره مباشرة إلى wrangler (لن يُطبع أبدًا)..."
openssl rand -hex 32 | wrangler secret put INGEST_HMAC_SECRET

echo ""
echo "✓ تم تثبيت INGEST_HMAC_SECRET على الـ Worker 'tg-content-bot'."
echo "  تحقق: أي POST /ingest/signal بلا توقيع يجب أن يرجع 403 (وليس 503)."
