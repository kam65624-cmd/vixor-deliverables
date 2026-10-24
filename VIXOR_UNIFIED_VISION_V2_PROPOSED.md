# VIXOR Ecosystem — Unified Vision V2 (Multi-Product SaaS)

**Status:** Proposed for review — NOT yet the production source of truth  
**Owner:** Ecosystem Tech Lead  
**Supersedes:** Nothing until explicitly approved  
**Operating constraints:** zero-cost-first, no live trading, no custody, private Telegram publishing only during initial rollout, human approval for sensitive financial content.

## 1. Executive vision

VIXOR is one coordinated ecosystem of independently useful products, not a set of disconnected bots and not one monolithic repository.

Each specialized product must:
- Have a clear user problem, distinct product identity, and independently usable experience.
- Have its own brand/character and audience strategy where useful.
- Produce useful, accurate Arabic and English content appropriate to its purpose.
- Participate in shared discovery, risk, content, distribution, and measurement workflows through versioned contracts.
- Refer interested users to the central control product when they need cross-product signal management and distribution.

The products should grow individually while reinforcing the central control plane. No product may claim integration or capability that has not been verified in code and tests.

## 2. Product roles

- **tg-content-bot — Control Center:** central administration, content calendar, character/brand profiles, channel/group registry, approval workflow, routing rules, scheduled publishing, analytics, click tracking, and operational alerts.
- **vixor-hunt — Discovery:** discover candidate assets and market events from approved free sources; preserve source, timestamp, chain, canonical address, and data quality.
- **vixor-shield — Risk Gate:** assess the exact canonical asset and event; issue explicit allow/review/reject decisions with reasons, freshness, expiry, policy version, and source completeness. Fail closed.
- **vixor-trade — Established-asset signals:** generate and track signals for supported established assets using real, timestamped market data; distinguish analysis from execution.
- **vixor-APP — Intelligence experience/orchestration:** provide supported analysis and coordinate specialized engines without duplicating their domain logic. Mock/simulated data must never be presented as real.
- **vixor-packages — Shared contracts:** own versioned schemas, validation, event types, and compatibility tests shared by producers and consumers.
- **vixorweb3 — Web3 experience:** retain only capabilities backed by real sources or clearly labeled demo data; establish its specific independent product value before launch.
- **vixor-deliverables — Governance:** maintain approved vision, decision log, architecture map, evidence-based audit, task registry, and acceptance criteria.

These roles are intended ownership boundaries. They do not prove that any current implementation is complete.

## 3. Canonical coin-event journey

Approved free data source → discovery producer → normalized event → canonical asset identity → mandatory Shield assessment → Core/control-plane validation → content/character selection → policy and human approval where required → private allowlisted Telegram destination → delivery/outbox reconciliation → outcome tracking.

Every event must include or resolve:
- stable event ID and idempotency key;
- chain/network identifier and canonical asset address or provider-native stable identifier;
- source and observation timestamp;
- market-data timestamps, quote currency, and provenance;
- schema version;
- risk assessment ID, decision, policy version, checked time, expiry, and exact asset identity assessed;
- content/approval status and destination policy;
- trace/correlation ID.

Ticker/symbol alone is never sufficient asset identity. A missing, stale, contradictory, expired, or mismatched assessment must not be treated as approval.

## 4. Control Center and publishing policy

The control plane must centrally manage:
- brand/character identity, voice, language, and content templates;
- channel/group registry, ownership, visibility classification, and allowlist;
- routing by event type, product, language, brand, and destination;
- human approval for sensitive financial content;
- deduplication, retries, unknown delivery outcomes, and audit records;
- analytics that distinguish reach/clicks from verified conversions and confirmed commissions.

Initial release policy:
- publish only to explicitly allowlisted private Telegram channels;
- do not publish publicly by default;
- do not enable live trading, custody, or money movement;
- fail closed if Shield, identity validation, destination validation, or freshness checks fail;
- no automatic paid plan/API upgrade; no paid dependency for the core path without explicit owner approval;
- never claim guaranteed profits or fabricate market data, risk checks, conversions, or results.

## 5. Independent SaaS product standard

A repository is not considered a SaaS product merely because it has a bot, UI, or README. Each product must document and demonstrate:
1. target user and distinct value proposition;
2. independent usable product journey;
3. product identity and responsible content strategy;
4. onboarding, configuration, permissions, and safe defaults appropriate to its scope;
5. observable health, errors, and usage;
6. cost/free-tier limits and documented dependency policy;
7. tests and operational runbook;
8. a clear, non-deceptive path to the central Control Center.

Billing, paid plans, account provisioning, or production launch are separate scope and require explicit approval. Do not add paid services by assumption.

## 6. Multi-agent engineering operating model

Roles:
- **Tech Lead/Integrator:** owns architecture, decisions, cross-repository sequencing, shared contracts, and integration gates.
- **Repository owners:** one accountable implementation agent per repository/domain, with explicit file ownership.
- **Security agent:** independently reviews auth, authorization, RLS, secret handling, data integrity, and financial safety.
- **QA/Release agent:** independently verifies tests and acceptance evidence; may reject a change.
- **Product/Growth agent:** owns product requirements, brand/character/content specs, and honest funnel measurement.

Rules:
- Every task has one accountable owner, repository, file scope, dependencies, acceptance criteria, and rollback notes.
- Agents must not edit the same files concurrently. Shared-file changes require coordination and one designated owner.
- Use isolated branches and pull requests; never push directly to protected production branches.
- Shared-contract changes are implemented first or behind an agreed compatibility plan.
- No agent may approve its own work.
- No merge, deployment, production migration, destructive operation, paid upgrade, or live-trading enablement without the required owner approval.
- Report actual evidence; never claim tests or runtime behavior were verified if they were not executed.

## 7. Required quality gates

For every PR:
- build, typecheck, lint, unit/integration tests as applicable;
- auth and authorization tests;
- invalid, missing, stale, duplicate, replayed, and mismatched-asset event tests;
- failure tests for source, database, Shield, and Telegram outages;
- review of changed files and dependency/contract compatibility;
- independent review and documented rollback plan.

Cross-repository acceptance must prove the same event traverses the actual producer, Shield, control plane, approval, private test destination, and delivery ledger without bypass or duplicate delivery.

Zero defects cannot be promised mathematically. The goal is measurable prevention, detection, and safe containment before production.

## 8. Rollout stages

1. **Reality audit:** inventory actual code, workflows, branches, open PRs, migrations, tests, deployment configuration, and evidence. No production changes.
2. **Vision approval:** review this proposed V2 against V1 and record an explicit owner decision. Until approval, V1 remains the approved source of truth.
3. **Contract foundation:** settle canonical event/risk/delivery schemas and compatibility tests.
4. **Critical safety fixes:** close confirmed authorization, secret, idempotency, stale-data, and fail-open issues.
5. **Vertical slice:** demonstrate one real or safely simulated test event end-to-end, with simulation clearly marked and private test destination only.
6. **Product readiness:** prove each product's distinct useful experience and content/growth role.
7. **Independent release review:** verify CI, staging behavior, recovery, rollback, cost constraints, and operational monitoring.
8. **Controlled rollout:** owner approval required; expand only after the preceding gate passes.

## 9. Evidence status labels

- **VERIFIED:** demonstrated by current code plus executed tests or runtime evidence appropriate to the claim.
- **PARTIAL:** some implementation exists but required paths or tests are missing.
- **BLOCKED:** depends on unavailable credentials, access, external service, or owner decision.
- **NOT IMPLEMENTED:** no implementation evidence found.
- **UNKNOWN:** current production state cannot be inferred from repository code.

Documentation and mock data are not runtime proof. An open/draft PR is not part of the default branch.

## 10. Approval and change control

This document is a proposed V2. It does not silently override `VIXOR_UNIFIED_VISION.md` V1.0. The owner must review and approve the change in product scope—especially independent SaaS experiences, character/brand growth, and cross-promotion—before it becomes the canonical vision.

Until approval, continue non-destructive audit and planning. Do not change production behavior based solely on this proposal.
