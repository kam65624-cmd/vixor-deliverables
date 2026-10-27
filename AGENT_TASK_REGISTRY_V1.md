# VIXOR Multi-Agent Task Registry — Phase 0/1

**Status:** Initial task registry; ownership is by domain, not a claim that external coding agents are currently running.  
**Control branch:** `vision/v2-multi-agent-saas`  
**Policy:** No direct-to-main changes, production deployment, production migration, paid upgrade, or live trading.

## 1. Task order and dependencies

| Order | Repo | Task | Branch | Dependency | Acceptance focus |
|---|---|---|---|---|---|
| 0 | vixor-deliverables | Vision approval + evidence inventory | `vision/v2-multi-agent-saas` | Owner reviews V2 proposal | V1/V2 decisions logged; evidence-backed repo matrix |
| 1 | vixor-packages | Shared contract foundation | `agent/shared-contract-foundation` | Agree required fields with Tech Lead | Versioned schemas + compatibility tests |
| 2 | vixor-shield | Risk gate | `agent/shield-risk-gate` | Contract identity fields | Exact asset binding, freshness, expiry, fail-closed, replay tests |
| 3 | vixor-hunt | Discovery producer | `agent/hunt-event-integration` | Contract + Shield API shape | Real event provenance, canonical identity, idempotency |
| 3 | vixor-trade | Established-asset producer | `agent/trade-signal-contract` | Contract + Shield API shape | Real timestamps, freshness, idempotency; no live execution |
| 4 | vixor-APP | Orchestration and data integrity | `agent/app-orchestration-hardening` | Contract; parallel audit allowed | Auth, simulated-data separation, no duplicate domain logic |
| 5 | tg-content-bot | Control-plane publishing safety | `agent/control-center-publishing-safety` | Contract + Shield decision format | Single mandatory send gate, private allowlist, approval, durable delivery |
| 6 | vixorweb3 | Product readiness | `agent/web3-product-readiness` | Product definition; integration uses shared contract | Mock/live separation, CI quality, independent product value |
| 7 | all | Independent review and E2E acceptance | Per-repo PRs | Prior tasks and CI | Same event traverses source → Shield → Control Center → private test channel without bypass or duplicate |

## 2. Initial issue tracker

- Deliverables governance: https://github.com/kam65624-cmd/vixor-deliverables/issues/8
- Shared contracts: https://github.com/kam65624-cmd/vixor-packages/issues/3
- Hunt: https://github.com/kam65624-cmd/vixor-hunt/issues/2
- Shield: https://github.com/kam65624-cmd/vixor-shield/issues/3
- Trade: https://github.com/kam65624-cmd/vixor-trade/issues/1
- APP: https://github.com/kam65624-cmd/vixor-APP/issues/24
- Telegram Control Center: https://github.com/kam65624-cmd/tg-content-bot/issues/16
- Web3: https://github.com/kam65624-cmd/vixorweb3/issues/1

## 3. Provisional file ownership

Exact paths must be confirmed from the current default branch before implementation. These are domain boundaries, not permission to edit unreviewed files.

- Shared contract schemas/tests: `vixor-packages` owner.
- Discovery source/normalization/producer path: `vixor-hunt` owner.
- Risk policy and assessment API: `vixor-shield` owner.
- Established-asset signal generation/ingestion: `vixor-trade` owner.
- APP orchestration, server auth, and data-source boundaries: `vixor-APP` owner.
- Telegram routing, approvals, channel allowlist, outbox and delivery reconciliation: `tg-content-bot` owner.
- Web3 demo/live data distinction and product scope: `vixorweb3` owner.
- Vision, decision log, audit matrix, and release gates: `vixor-deliverables` owner.

No two agents may concurrently edit the same file. Cross-repository contract changes must be coordinated before dependent implementation lands.

## 4. Required evidence in each issue/PR

1. Baseline commit SHA and exact file paths inspected.
2. Current behavior and a minimal reproduction or code evidence.
3. Changed files and why each change is necessary.
4. Tests actually executed, with exact results.
5. Negative tests: missing/stale data, wrong asset identity, unauthorized caller, duplicate/replay, provider outage.
6. CI result, compatibility risks, and rollback plan.
7. Independent review status.

## 5. Hard release gates

- No merge solely because the CI badge is green.
- No production publishing until the complete coin-event journey is proven in a private test destination.
- No public financial signal publishing during the initial rollout.
- No live trading, custody, or money movement.
- No paid API/service or automatic upgrade without explicit owner approval.
- No production migration or deployment without explicit owner approval.
- Keep V1 as canonical until the owner explicitly approves V2.


## 6. Current execution status (2026-10-27)

The evidence-backed owner status and prioritized repair queue are maintained in [OWNER_VISIBLE_EXECUTION_STATUS_2026-10-27.md](./OWNER_VISIBLE_EXECUTION_STATUS_2026-10-27.md) on the audit branch. It distinguishes:
- implementation present on a PR branch,
- CI/test pass,
- merged into default branch,
- deployed,
- and end-to-end verified.

Current verified evidence: tg-content-bot PR #20 CI run 40440971027 passed on commit 3e79428f7774caa40648060920b7af52b6a96af7. PR #20 remains draft/open. Hunt PR #1 and Shield PR #2 also remain draft/open. These are not considered production-delivered. Full migration-chain repeatability, effective RLS/grants, cross-repository contract parity, and deployed Hunt → Shield → control-center → private test destination E2E remain open gates.

The status file is documentation for owner visibility and does not authorize a merge, deployment, production migration, publishing, or live trading.
