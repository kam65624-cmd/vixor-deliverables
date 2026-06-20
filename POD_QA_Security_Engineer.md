# POD — QA / Security Engineer

> **Role**: QA and Security Engineer for VIXOR Hybrid Platform
> **Reports to**: Lead Developer
> **Mission**: Ensure code quality, security, and smooth user experience across all pages and widgets

---

## Responsibilities

### 1. Quality Assurance
- Write and maintain test suites (Vitest + Playwright)
- Perform manual testing for new features
- Verify bug fixes
- Test cross-browser compatibility
- Test mobile responsiveness

### 2. Security Testing
- OWASP Top 10 vulnerability scanning
- Dependency vulnerability scanning (npm audit)
- Secret scanning (git-secrets + truffleHog)
- Penetration testing (pre-launch)
- Web3-specific security (honeypot, rug pull, wallet)

### 3. User Flow Testing
- Test complete user journeys (signup → trade → portfolio)
- Test workspace switching (OS ↔ Terminal)
- Test all 3 UI styles (BullX + Axiom + OpenSea)
- Test all widgets and components
- Test error states + edge cases

### 4. Continuous Monitoring
- Monitor test coverage (80%+ target)
- Monitor bug reports
- Monitor Sentry errors
- Monitor user feedback

---

## Phase-by-Phase Tasks

### Phase B.1 — Arbitrage Testing (Week 2) ✅
- [x] Run arbitrage unit tests (strategies + risk + config)
- [x] Verify arbitrage API endpoint works
- [x] Verify arbitrage dashboard renders

### Phase B.2 — Wallet Hub Testing (Week 3)
- [ ] Test wallet connection (Phantom + MetaMask)
- [ ] Test session persistence (reload page)
- [ ] Test session expiry (after 7 days)
- [ ] Test non-custodial (no private keys stored)
- [ ] Test multi-chain switching (Solana + ETH + Base + BSC)
- [ ] Test error states (wrong network, rejected signature)
- [ ] Write Playwright e2e: connect wallet → trade → verify

### Phase B.3 — Web3 Terminal Testing (Weeks 3-5)
- [ ] Test Workspace Switcher (all pages, state persists)
- [ ] Test Discover page (filters work, cards render, click navigates)
- [ ] Test Token Page (chart loads, order book updates, order entry works)
- [ ] Test Communities page (all 5 tabs load, heatmap renders)
- [ ] Test Wallet page (holdings display, modals work)
- [ ] Test Activity page (feed loads, filters work)
- [ ] Test all 3 UI styles render correctly
- [ ] Test cross-browser (Chrome + Firefox + Safari)
- [ ] Test mobile responsive (375px + 768px + 1440px)
- [ ] Test dark mode (default)
- [ ] Write Playwright e2e for each page

### Phase B.4 — Memecoin Discovery Testing (Weeks 5-7)
- [ ] Test scoring algorithm (correct results)
- [ ] Test API rate limiting (no throttling)
- [ ] Test caching (30s for prices, 5min for social)
- [ ] Test real-time updates (30s polling)
- [ ] Test VIXOR AI Risk Badge (correct colors)
- [ ] Test NFT Badge (4 states)
- [ ] Test honeypot detection
- [ ] Test liquidity lock verification

### Phase C — VIXOR AI Testing (Weeks 8-11)
- [ ] Test Coach overlay (appears on trade preview)
- [ ] Test Analyst report (generates weekly, delivers)
- [ ] Test Governor (blocks risky trades)
- [ ] Test Hunter (alerts on smart money)
- [ ] Test feedback loop (accept/reject works)
- [ ] Test AI accuracy (win rate tracking)
- [ ] Test LLM fallback (provider failure → next provider)

### Phase C.2 — Knowledge Hub Testing (Weeks 10-11)
- [ ] Test Learning Hub (lessons load, quizzes work, certificates issue)
- [ ] Test Calendar Hub (events load, AI alerts trigger)
- [ ] Test News Hub (feed loads, classification correct)
- [ ] Test Decisions Hub (decisions display, feedback works)

### Phase D — Pre-Launch Testing (Weeks 12-14)
- [ ] Full regression test (all features)
- [ ] Load testing (1000 concurrent users with k6)
- [ ] Security penetration testing
- [ ] OWASP ZAP scan
- [ ] Dependency audit (npm audit)
- [ ] Secret scanning (git-secrets)
- [ ] Lighthouse audit (score > 90)
- [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] Beta user testing (100 users)
- [ ] Bug bash with team

---

## Test Suite Structure

### Unit Tests (Vitest)
```
src/
├── domains/
│   ├── arbitrage/
│   │   └── tests/
│   │       ├── config.test.ts ✅
│   │       ├── risk.test.ts ✅
│   │       └── strategies.test.ts ✅
│   ├── wallet/
│   │   └── tests/
│   │       ├── session.test.ts (B.2)
│   │       └── provider.test.ts (B.2)
│   ├── discovery/
│   │   └── tests/
│   │       ├── scoring.test.ts (B.4)
│   │       └── birdeye.client.test.ts (B.4)
│   └── copilot/
│       └── tests/
│           ├── coach.test.ts (C.1)
│           ├── analyst.test.ts (C.1)
│           ├── governor.test.ts (C.1)
│           └── hunter.test.ts (C.1)
└── shared/
    └── tests/
        ├── llm.test.ts
        ├── memory.test.ts
        └── crypto.test.ts
```

### E2E Tests (Playwright)
```
tests/e2e/
├── auth.spec.ts              # signup, login, logout
├── wallet.spec.ts            # connect, session, multi-chain (B.2)
├── workspace-switch.spec.ts  # OS ↔ Terminal switch (B.3)
├── discover.spec.ts          # filters, cards, navigation (B.3)
├── token-page.spec.ts        # chart, order book, trade (B.3)
├── communities.spec.ts       # tabs, heatmap, mentions (B.3)
├── wallet-page.spec.ts       # holdings, send, swap (B.3)
├── activity.spec.ts          # feed, filters, export (B.3)
├── arbitrage.spec.ts         # scan, results, dashboard (B.1)
├── ai-coach.spec.ts          # overlay, feedback (C.1)
├── learning.spec.ts          # lessons, quizzes (C.2)
└── full-flow.spec.ts         # signup → trade → portfolio (D)
```

---

## Security Testing Checklist

### OWASP Top 10
- [ ] A01: Broken Access Control — verify RLS on all tables
- [ ] A02: Cryptographic Failures — verify AES-256-GCM for credentials
- [ ] A03: Injection — verify parameterized queries (Supabase)
- [ ] A04: Insecure Design — review all API designs
- [ ] A05: Security Misconfiguration — verify headers, CORS, CSRF
- [ ] A06: Vulnerable Components — npm audit weekly
- [ ] A07: Auth Failures — verify session management
- [ ] A08: Data Integrity Failures — verify webhook signatures
- [ ] A09: Logging Failures — verify audit logs
- [ ] A10: SSRF — verify external API calls

### Web3 Specific
- [ ] Non-custodial wallet (no private keys stored)
- [ ] Signed JWT with short TTL (7 days)
- [ ] IP fingerprinting for sessions
- [ ] Honeypot detection (Honeypot.is API)
- [ ] Liquidity lock verification
- [ ] Dev wallet audit
- [ ] Smart money tracking (rug pull prevention)
- [ ] Phishing link blocking in descriptions

### Dependency Security
- [ ] `npm audit` — 0 high/critical vulnerabilities
- [ ] Dependabot enabled
- [ ] Weekly dependency review
- [ ] Pin major versions

### Secret Scanning
- [ ] git-secrets pre-commit hook
- [ ] truffleHog scan in CI
- [ ] No secrets in code
- [ ] No secrets in git history

---

## KPIs

| Metric | Target |
|--------|--------|
| Test coverage | 80%+ |
| Unit tests passing | 100% |
| E2E tests passing | 100% |
| Critical vulnerabilities | 0 |
| High vulnerabilities | 0 |
| Lighthouse score | > 90 |
| Accessibility score | > 90 |
| Bug escape rate | < 5% |
| Test execution time | < 10 min (full suite) |

---

## Daily QA Routine

### Morning (Every Day)
1. Run full test suite: `npx vitest run && npx playwright test`
2. Check Sentry for new errors
3. Review overnight CI/CD results
4. Test any new features manually

### Before Each Release
1. Full regression test
2. Security scan (npm audit + OWASP ZAP)
3. Lighthouse audit
4. Cross-browser test
5. Mobile test
6. Sign off on release

### Weekly (Friday)
1. Review test coverage
2. Update test cases for new features
3. Review bug reports
4. Plan testing for next week

---

## Quality Gates (Must Pass Before Merge)

1. All unit tests pass
2. All integration tests pass
3. All e2e tests pass (for affected flows)
4. No new console errors
5. No new TypeScript errors
6. No new ESLint errors
7. No new security vulnerabilities
8. Lighthouse score not degraded
9. Test coverage not decreased
10. Manual smoke test passed
