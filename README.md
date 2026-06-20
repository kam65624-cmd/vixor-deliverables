# VIXOR Phase A + B.1 — تطبيق فوري

## محتويات المجلد

| الملف | الوصف |
|------|-------|
| `apply-phase-a-b1.sh` | Script شامل يطبق Phase A + B.1 على vixor-APP |
| `vixor-phase-a-b1.patch` | Git patch file (29 ملف، 2284 سطر) — بديل للـ script |

---

## كيفية التطبيق (طريقتان)

### الطريقة 1: استخدم الـ Script (موصى به)

```bash
# 1. انسخ الـ script لمجلد vixor-APP
cp apply-phase-a-b1.sh /path/to/your/vixor-APP/

# 2. ادخل لمجلد vixor-APP
cd /path/to/your/vixor-APP

# 3. شغّل الـ script
bash apply-phase-a-b1.sh

# 4. راجع التغييرات
git diff
git status

# 5. ثبت dependencies الجديدة
npm install

# 6. اختبر الـ build
npm run build

# 7. اختبر الـ lint
npm run lint

# 8. اختبر arbitrage tests
npx vitest run src/domains/arbitrage/tests/

# 9. commit
git add -A
git commit -m "Phase A+B.1: arbitrage integration from axiom-arbitrage"
git push
```

### الطريقة 2: استخدم الـ Patch file

```bash
# 1. انسخ الـ patch لمجلد vixor-APP
cp vixor-phase-a-b1.patch /path/to/your/vixor-APP/

# 2. ادخل لمجلد vixor-APP
cd /path/to/your/vixor-APP

# 3. طبّق الـ patch
git apply vixor-phase-a-b1.patch

# 4. ثبت dependencies
npm install

# 5. اختبر
npm run build && npm run lint

# 6. commit
git add -A
git commit -m "Phase A+B.1: arbitrage integration from axiom-arbitrage"
git push
```

---

## ما تم تنفيذه

### ✅ Phase A — التحقق من التنظيف (6 بنود)

| البند | الحالة | التفاصيل |
|------|--------|----------|
| A.1 .gitignore | ✅ سليم | يحتوي على node_modules, dist, .env*, .vercel, إلخ |
| A.2 ESLint config | ✅ سليم | `eslint.config.js` مع TypeScript + React + Prettier |
| A.3 Git baseline | ✅ clean working tree | لا توجد untracked files حرجة |
| A.4 API routes | ✅ لا حاجة لـ `dynamic = 'force-dynamic'` | TanStack Start يستخدم server functions (dynamic by default) |
| A.5 Webhook signatures | ✅ HMAC verification موجود | `x-telegram-bot-api-secret-token` في telegram-webhook + stars-webhook |
| A.6 fix-vercel-bundle.mjs | ✅ production-safe | Error handler لا ي expose stack traces في production |

### ✅ Phase B.1 — دمج axiom-arbitrage (22 ملف)

**الملفات المنقولة:**

```
src/domains/arbitrage/
├── index.ts                    ← Public API + createArbitrageEngine factory
├── config.ts                   ← ArbitrageConfig + ARBITRAGE_ env prefix
├── engine.ts                   ← ArbitrageEngine (orchestrator)
├── executor.ts                 ← TradeExecutor (dry-run + live)
├── risk.ts                     ← RiskManager + CircuitBreaker
├── types.ts                    ← Shared domain types
├── logger.ts                   ← Logging utility
├── math.ts                     ← Profit/loss calculations
├── price-feed.ts               ← Price feed (mock + live)
├── token-registry.ts           ← Token registry (SOL, USDC, BONK, WIF, JUP)
├── strategies/
│   ├── base.ts                 ← BaseStrategy abstract class
│   ├── cross-dex.ts            ← Cross-DEX arbitrage
│   ├── triangular.ts           ← Triangular cycles (A→B→C→A)
│   ├── cex-dex.ts              ← CEX-DEX spreads
│   └── index.ts                ← createStrategies factory
├── exchanges/
│   ├── types.ts                ← ExchangeClient interface
│   ├── jupiter.client.ts       ← Jupiter v6 Quote API
│   ├── axiom.client.ts         ← Axiom terminal API
│   ├── index.ts                ← createExchangeClients factory
│   └── mock/
│       ├── dex-clients.ts      ← Mock DEX clients
│       └── quote-simulator.ts  ← Quote simulator
└── tests/
    ├── config.test.ts          ← Config tests
    ├── risk.test.ts            ← RiskManager + CircuitBreaker tests
    └── strategies.test.ts      ← Strategy tests
```

**الملفات الجديدة (غير المنقولة):**

| الملف | الوصف |
|------|-------|
| `src/routes/_authenticated/arbitrage.tsx` | Arbitrage dashboard route |
| `server/api/arbitrage-scan.ts` | API endpoint للـ scan |
| `supabase/migrations/20260621000000_add_arbitrage_domain.sql` | 3 جداول جديدة + RLS |

**التعديلات على ملفات موجودة:**

| الملف | التغيير |
|------|---------|
| `package.json` | إضافة `@solana/web3.js@^1.98.4` + `bs58@^6.0.0` |
| `.env.example` | إضافة 17 متغير بـ prefix `ARBITRAGE_` |

---

## التعديلات على الكود الأصلي (axiom-arbitrage)

1. **Imports**: إزالة `.js` extensions + تحويل `'../src/...'` لمسارات نسبية صحيحة
2. **Types**: `AppConfig` → `ArbitrageConfig`، `loadConfig` → `loadArbitrageConfig`
3. **Env vars**: إضافة `ARBITRAGE_` prefix لكل المتغيرات (تجنب التعارض)
4. **Tests**: حذف `engine.test.ts` (يعتمد على Express — غير مطبق في vixor-APP)
5. **API**: تخطي نقل Express REST API (vixor-APP يستخدم TanStack Start server functions)

---

## بعد التطبيق — الخطوات التالية

### 1. تطبيق Supabase migration

```bash
# الطريقة الأولى: supabase CLI
npx supabase db push

# الطريقة الثانية: Supabase SQL Editor
# انسخ محتوى supabase/migrations/20260621000000_add_arbitrage_domain.sql
# والصقه في Supabase Dashboard → SQL Editor → Run
```

### 2. تعيين env vars على Vercel

```bash
# المتغيرات الأساسية (آمنة — no real funds)
vercel env add ARBITRAGE_BOT_MODE        # set to "mock"
vercel env add ARBITRAGE_DRY_RUN          # set to "true"
vercel env add ARBITRAGE_EXECUTION_ENABLED # set to "false"

# المتغيرات الاختيارية (لـ live mode لاحقاً)
vercel env add ARBITRAGE_SOLANA_RPC_URL   # Helius RPC URL
vercel env add ARBITRAGE_AXIOM_API_KEY    # from Axiom
vercel env add ARBITRAGE_WALLET_PRIVATE_KEY # ⚠️ فقط لـ live mode

# redeploy
vercel --prod
```

### 3. اختبار arbitrage محلياً

```bash
# شغّل التطبيق محلياً
npm run dev

# افتح arbitrage dashboard
# http://localhost:3000/arbitrage

# أو استخدم API مباشرة
curl -X POST http://localhost:3000/api/arbitrage/scan \
  -H "Authorization: Bearer $HEALTH_TOKEN"
```

### 4. تشغيل arbitrage tests

```bash
npx vitest run src/domains/arbitrage/tests/
# المتوقع: 3 test files تنجح
```

---

## ⚠️ تحذيرات أمنية حرجة

1. **`ARBITRAGE_DRY_RUN=true` افتراضياً** — لا يتم نقل أموال حقيقية
2. **`ARBITRAGE_EXECUTION_ENABLED=false` افتراضياً** — لا صفقات live
3. **لا تفعّل live execution** إلا بعد:
   - ✅ tests ناجحة
   - ✅ مراجعة code review
   - ✅ اختبار على testnet بـ small amounts (&lt; 0.1 SOL)
4. **لا commit `ARBITRAGE_WALLET_PRIVATE_KEY`** لـ git أبداً
5. **استخدم Helius RPC** (مش free RPC) لـ reliability

---

## ما التالي (Phase B.2-B.4 + C+D)

بعد تطبيق Phase A + B.1 بنجاح:

| Phase | المحتوى | المدة |
|-------|---------|-------|
| B.2 | Wallet Hub (multi-chain) | أسبوع |
| B.3 | Web3 Terminal (3 styles) | 4 أسابيع |
| B.4 | Memecoin Discovery | 3 أسابيع |
| C | VIXOR AI 4 agents + Knowledge Hub | 4 أسابيع |
| D | Polish + Premium + Launch | 3 أسابيع |

**الإجمالي:** 14 أسبوع (بدلاً من 16 — توفير 2 أسبوع بفضل axiom-arbitrage)

---

## الدعم

لو واجهت أي مشكلة أثناء التطبيق:

1. راجع `git diff` للتأكد من التغييرات
2. شغّل `npm run build` وتحقق من الأخطاء
3. تأكد إن `npm install` شغّل بنجاح (لـ @solana/web3.js + bs58)
4. لو في خطأ في imports، شغّل:
   ```bash
   npx eslint --fix src/domains/arbitrage/
   ```

**ملاحظة عن vixorweb3**: الملف `vixorweb3-main.zip` لم يصل للسيرفر. لو سمحت ترفعه تاني وأراجعه.
