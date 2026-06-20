# POD — Backend Developer

> **Role**: Backend Developer for VIXOR Hybrid Platform
> **Reports to**: Lead Developer
> **Mission**: Build API routes, server functions, database schema, and external integrations

---

## Responsibilities

### 1. API Development
- Build all API routes in `server/api/`
- Build all server functions in `src/domains/*/functions.ts`
- Input validation with Zod
- Auth gates on all endpoints
- Error handling with `createError`

### 2. Database
- Design and write Supabase migrations
- Implement RLS policies on all tables
- Optimize queries (indexes, pagination)
- Database backup + restore procedures

### 3. External Integrations
- Integrate all external APIs (Birdeye, Helius, Jupiter, Twitter, LunarCrush, Finnhub, etc.)
- Implement rate limiting + circuit breaker
- Implement caching (Upstash Redis)
- Implement fallback strategies

### 4. Security
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- Secrets management (env vars only)
- HMAC signature verification on webhooks

---

## Phase-by-Phase Tasks

### Phase B.1 — Arbitrage (Already Done ✅)
- [x] Port axiom-arbitrage to `src/domains/arbitrage/`
- [x] Create `server/api/arbitrage-scan.ts`
- [x] Create `supabase/migrations/20260621000000_add_arbitrage_domain.sql`

### Phase B.2 — Wallet Hub Backend (Week 3)
- [ ] Create `src/domains/wallet/` domain
- [ ] Implement `wallets` table migration (multi-chain)
- [ ] Implement `wallet_sessions` table migration (signed JWT)
- [ ] Build server function: `connectWallet({ address, chain, signature })`
- [ ] Build server function: `getWalletSession()`
- [ ] Build server function: `disconnectWallet()`
- [ ] Implement JWT signing + verification (HS256, 7-day TTL)
- [ ] Implement IP fingerprinting for sessions
- [ ] Test: connect → session created → session expires → reconnect

### Phase B.3 — Web3 Terminal Backend (Weeks 3-5)
- [ ] Build `server/api/discover.ts` (GET — return memecoin list with filters)
- [ ] Build `server/api/token/[symbol].ts` (GET — return token details + chart data)
- [ ] Build `server/api/communities/[symbol].ts` (GET — return community data)
- [ ] Build `server/api/wallet/balance.ts` (GET — return wallet balances)
- [ ] Build `server/api/wallet/send.ts` (POST — initiate send)
- [ ] Build `server/api/wallet/swap.ts` (POST — initiate swap via Jupiter)
- [ ] Build `server/api/activity.ts` (GET — return activity feed)
- [ ] Implement `web3_transactions` table migration
- [ ] Implement `nft_badges` table migration
- [ ] Test: all endpoints return correct data, auth gates work

### Phase B.4 — Memecoin Discovery Backend (Weeks 5-7)
- [ ] Create `src/domains/discovery/` domain
- [ ] Build Birdeye API client (`src/domains/discovery/exchanges/birdeye.client.ts`)
- [ ] Build Helius RPC client (`src/domains/discovery/exchanges/helius.client.ts`)
- [ ] Build Twitter API client (`src/domains/discovery/exchanges/twitter.client.ts`)
- [ ] Build LunarCrush API client (`src/domains/discovery/exchanges/lunarcrush.client.ts`)
- [ ] Build DexScreener client (already exists in vixor-APP? check)
- [ ] Implement 5-stage scoring algorithm
- [ ] Implement `memecoin_discoveries` table migration (cache)
- [ ] Implement `social_signals` table migration
- [ ] Build `server/api/discover/scan.ts` (POST — trigger scan)
- [ ] Implement caching layer (Upstash Redis, 30s TTL for prices, 5min for social)
- [ ] Test: all API clients work, scoring produces correct results

### Phase C — VIXOR AI Backend (Weeks 8-9)
- [ ] Extend `user_memories` table (add `workspace` field)
- [ ] Create `vixor_decisions` table migration
- [ ] Build Real-time Coach server function
- [ ] Build Behavioral Analyst cron job (Sunday 08:00)
- [ ] Build Risk Governor server function
- [ ] Build Smart Money Hunter cron job (hourly)
- [ ] Implement feedback loop (accept/reject decisions)
- [ ] Test: all agents produce correct output, cron jobs run

### Phase C.2 — Knowledge Hub Backend (Weeks 10-11)
- [ ] Create `learning_paths` + `learning_progress` table migrations
- [ ] Create `calendar_events` table migration
- [ ] Build Finnhub API client (news + economic calendar)
- [ ] Build CryptoPanic API client
- [ ] Build CoinMarketCal API client
- [ ] Build RSS parser (CoinDesk, The Block, DL News)
- [ ] Implement LLM classification for news (macro/crypto/token)
- [ ] Test: all hubs return data, AI alerts trigger

### Phase D — Polish Backend (Weeks 12-14)
- [ ] Stripe integration (subscriptions + webhook HMAC)
- [ ] Jupiter referral account integration
- [ ] Health endpoint expansion
- [ ] Metrics endpoint expansion
- [ ] Sentry integration (server-side)
- [ ] Database query optimization
- [ ] Test: Stripe webhook verified, referral works

---

## KPIs

| Metric | Target |
|--------|--------|
| API latency (p95) | < 200ms |
| API error rate | < 0.1% |
| Database query time (p95) | < 50ms |
| External API cache hit rate | > 80% |
| Migration success rate | 100% |
| Test coverage (domains + shared) | 80%+ |

---

## Quality Gates

1. All API inputs validated with Zod
2. All API routes have auth gate
3. All database tables have RLS
4. All external API calls have rate limiting + circuit breaker
5. All webhooks have HMAC verification
6. No SQL injection vulnerabilities
7. No secrets in code
8. All migrations tested on staging first
9. All tests pass (Vitest)
