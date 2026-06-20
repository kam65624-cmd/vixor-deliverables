# POD — DevOps Engineer

> **Role**: DevOps Engineer for VIXOR Hybrid Platform
> **Reports to**: Lead Developer
> **Mission**: Manage deployment, CI/CD, monitoring, and infrastructure

---

## Responsibilities

### 1. Deployment
- Manage Vercel deployments (preview + production)
- Manage Supabase (database + auth + storage)
- Manage Upstash Redis (cache + rate limiting)
- Manage environment variables (secrets)

### 2. CI/CD
- Maintain GitHub Actions workflows
- Build + test on every PR
- Auto-deploy to staging on merge to main
- Manual deploy to production

### 3. Monitoring
- Sentry (error tracking)
- Vercel Analytics (performance)
- Supabase logs (database)
- Custom health endpoints
- Uptime monitoring

### 4. Infrastructure
- Domain management
- SSL certificates
- CDN configuration
- Backup strategy

---

## Phase-by-Phase Tasks

### Phase A — Infrastructure Setup (Week 1) ✅
- [x] Verify Vercel project configured
- [x] Verify Supabase project configured
- [x] Verify Upstash Redis configured
- [x] Verify env vars on Vercel

### Phase B — Ongoing (Weeks 2-7)
- [ ] Set up staging environment (separate Vercel preview + Supabase staging)
- [ ] Configure GitHub Actions:
  - On PR: lint + tsc + build + test
  - On merge to main: deploy to staging
  - On tag: deploy to production
- [ ] Set up Sentry (frontend + backend)
- [ ] Set up uptime monitoring (Better Stack or UptimeRobot)
- [ ] Configure Supabase automated backups (daily)
- [ ] Set up log aggregation (Vercel logs + Supabase logs)
- [ ] Create deployment runbook
- [ ] Test: staging deploy works, production deploy works

### Phase C — Monitoring Expansion (Weeks 8-11)
- [ ] Add Sentry performance monitoring
- [ ] Add custom metrics endpoint (Prometheus format)
- [ ] Set up alerting (Sentry + Vercel + uptime)
- [ ] Create status page (status.vixor.app)
- [ ] Set up log retention (30 days)
- [ ] Test: alerts trigger on errors, status page updates

### Phase D — Launch Prep (Weeks 12-14)
- [ ] Load testing infrastructure (k6)
- [ ] CDN configuration (Vercel Edge)
- [ ] Database connection pooling
- [ ] Redis cluster (if needed for scale)
- [ ] Backup verification (restore test)
- [ ] Disaster recovery plan
- [ ] SSL certificate renewal automation
- [ ] Test: load test passes 1000 concurrent users, backup restores correctly

---

## KPIs

| Metric | Target |
|--------|--------|
| Uptime | 99.5%+ |
| Deploy frequency | Daily (staging), weekly (prod) |
| Deploy success rate | 99%+ |
| Mean time to recovery (MTTR) | < 30 min |
| Build time (CI) | < 5 min |
| Staging deploy time | < 3 min |
| Production deploy time | < 5 min |
| Backup success rate | 100% |

---

## Daily Operations

### Morning Check (Every Day)
1. Check Vercel deployment status
2. Check Supabase health
3. Check Upstash Redis health
4. Check Sentry for new errors
5. Check uptime monitor
6. Review overnight deploys

### Before Production Deploy
1. All tests pass on staging
2. Database backup created
3. Env vars verified
4. Sentry release created
5. Owner notified
6. Rollback plan ready

### After Production Deploy
1. Verify health endpoint
2. Check Sentry for new errors
3. Monitor for 30 minutes
4. Update status page
5. Notify team

---

## Environment Variables Checklist

### Vercel (Production)
- [ ] SUPABASE_URL
- [ ] SUPABASE_SERVICE_ROLE_KEY
- [ ] VITE_SUPABASE_URL
- [ ] VITE_SUPABASE_PUBLISHABLE_KEY
- [ ] TELEGRAM_BOT_TOKEN
- [ ] VITE_TELEGRAM_BOT_USERNAME
- [ ] TELEGRAM_WEBHOOK_SECRET
- [ ] TWELVEDATA_API_KEY
- [ ] FINNHUB_API_KEY
- [ ] CRON_SECRET
- [ ] HEALTH_TOKEN
- [ ] CREDENTIAL_ENCRYPTION_KEY
- [ ] LLM_PROVIDER
- [ ] OPENAI_API_KEY (optional)
- [ ] ANTHROPIC_API_KEY (optional)
- [ ] GROQ_API_KEY (optional)
- [ ] UPSTASH_REDIS_REST_URL
- [ ] UPSTASH_REDIS_REST_TOKEN
- [ ] ARBITRAGE_BOT_MODE (mock)
- [ ] ARBITRAGE_DRY_RUN (true)
- [ ] ARBITRAGE_EXECUTION_ENABLED (false)
- [ ] ARBITRAGE_SOLANA_RPC_URL
- [ ] ARBITRAGE_AXIOM_API_KEY (optional)
- [ ] HELIUS_API_KEY (Phase B.4)
- [ ] BIRDEYE_API_KEY (Phase B.4)
- [ ] TWITTER_API_KEY (Phase B.4)
- [ ] LUNARCRUSH_API_KEY (Phase B.4)
- [ ] STRIPE_SECRET_KEY (Phase D)
- [ ] STRIPE_WEBHOOK_SECRET (Phase D)

---

## Quality Gates

1. All deploys are reproducible
2. All secrets in Vercel (not in code)
3. All environments have separate secrets
4. Backups tested monthly
5. Monitoring covers all critical paths
6. Runbook documented + accessible
7. No manual production changes (everything via CI/CD)
