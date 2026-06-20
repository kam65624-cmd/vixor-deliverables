# POD — Lead Developer / Tech Lead

> **Role**: Lead Developer for VIXOR Hybrid Platform
> **Reports to**: Project Owner
> **Manages**: Frontend, Backend, AI/ML, DevOps, QA engineers
> **Mission**: Ensure architectural integrity, code quality, and on-time delivery

---

## Responsibilities

### 1. Architecture
- Maintain Domain-Driven Design structure (`src/domains/*`)
- Enforce loose coupling between layers (UI → Domains → Shared → Infrastructure)
- Review all new domain additions
- Approve all dependency additions
- Maintain the `Result<T>` pattern for fallible operations

### 2. Code Quality
- Review every PR before merge
- Enforce 0 TypeScript errors, 0 ESLint errors
- Ensure 80%+ test coverage
- Reject any `any` types without justification
- Enforce JSDoc on all exported functions

### 3. Technical Decisions
- Choose libraries and frameworks
- Approve database schema changes
- Approve API design changes
- Resolve technical conflicts between team members

### 4. Risk Management
- Identify technical risks early
- Maintain risk register
- Plan mitigations
- Escalate blockers to owner

---

## Phase-by-Phase Tasks

### Phase B.2 — Wallet Hub (Week 3)
- [ ] Review Wallet Hub architecture before implementation
- [ ] Approve wallet provider choice (@solana/wallet-adapter + wagmi)
- [ ] Review JWT session design (non-custodial)
- [ ] Code review: WalletProvider, WalletConnect component
- [ ] Verify: no private keys stored, session TTL correct

### Phase B.3 — Web3 Terminal (Weeks 3-5)
- [ ] Approve 3-style Design System architecture
- [ ] Review WorkspaceSwitcher implementation
- [ ] Code review: each new page (Discover, Token, Communities, Wallet, Activity)
- [ ] Verify: workspace switch works seamlessly
- [ ] Verify: no layout breaks between styles

### Phase B.4 — Memecoin Discovery (Weeks 5-7)
- [ ] Approve scoring algorithm design
- [ ] Review API integration patterns (rate limiting, caching)
- [ ] Code review: Discovery engine, scoring logic
- [ ] Verify: real-time updates work without memory leaks

### Phase C — VIXOR AI (Weeks 8-11)
- [ ] Approve 4-agent architecture
- [ ] Review user_memories schema extension
- [ ] Code review: each AI agent (Coach, Analyst, Governor, Hunter)
- [ ] Verify: feedback loop works (accept/reject)

### Phase D — Polish + Launch (Weeks 12-14)
- [ ] Approve performance optimization plan
- [ ] Review Stripe integration (security)
- [ ] Final security review before launch
- [ ] Sign off on production deployment

---

## KPIs

| Metric | Target |
|--------|--------|
| PRs reviewed within 24h | 100% |
| Build success rate | 99%+ |
| Production incidents | 0 critical, < 2 minor/week |
| On-time phase delivery | Within 3 days of plan |
| Code coverage | 80%+ |

---

## Quality Gates (Must Pass Before Merge)

1. `npx tsc --noEmit` — 0 errors
2. `npm run lint` — 0 errors, 0 warnings
3. `npm run build` — success
4. `npx vitest run` — all pass
5. Code review approved by Lead
6. No new security vulnerabilities (npm audit)
7. Bundle size within budget (+50KB max per PR)
