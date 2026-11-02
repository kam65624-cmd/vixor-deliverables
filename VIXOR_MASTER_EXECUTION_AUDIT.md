# VIXOR — MASTER VISION, AUDIT & EXECUTION REGISTER

**Document ID:** VIXOR-MASTER-OPS-001  
**Version:** 1.0  
**Snapshot date:** 2026-11-02  
**Status:** ACTIVE — canonical working register; not a production-readiness certificate  
**Owner:** Mahmoud Omar  
**Execution model:** Agent 1 is the sole delegated implementation agent; the technical lead may perform independent, isolated engineering/review work when repository access and testability permit.

> This document consolidates the approved product vision, architecture, stage plan, known defects, evidence, decisions, and execution queue. It supersedes fragmented status snapshots for current task coordination, but it does not erase historical records or silently override owner-approved decisions. Every update must be append-only in the change log and must preserve source evidence.

---

## 1. Executive direction

VIXOR is one unified crypto intelligence product: a large, modular machine internally and a simple, coherent experience externally.

The objective is not to keep producing audits. The objective is to deliver a working product through a controlled sequence:
1. establish trustworthy shared contracts and security boundaries;
2. prove producer-to-consumer integration;
3. make the unified product experience visibly coherent and useful;
4. establish character identities and reusable assets;
5. complete memory, activity, wallet intelligence, notifications, operations, and payment flows;
6. prove the end-to-end journey and obtain owner approval.

**Current execution priority:** finish Stage 2 without losing momentum on product visibility. Prepare the Stage 4 product backlog and evidence in parallel, but do not bypass the approved stage gates or make production-effective changes without approval.

### Progress principles
- Prefer one tested, owner-visible outcome over multiple speculative branches.
- Fix confirmed defects; do not create new abstractions without a demonstrated need.
- Do not repeat tests already passed unless the code/base changed or the prior evidence is stale.
- A report, branch, green unit test, or Draft PR is not the same as integration or production delivery.
- Every task must have an owner, acceptance criteria, exact base/head SHA, tests, and a next action.
- Keep one canonical issue register here; other logs remain evidence/history, not competing task lists.

---

## 2. Approved product vision and boundaries

### 2.1 Product model
- One product: VIXOR.
- Approved experience model: **Hybrid Experience (Model C)** — Unified Shell plus specialized workspaces and context-adaptive personas.
- Repositories remain separate deployable codebases; they are not separate products with unrelated audiences.
- Telegram remains the control, approval, alert, and publishing channel for the relevant workflows. It is not a reason to split the VIXOR product into separate character mini-apps.
- The web application is a first-class unified SaaS experience; the older Telegram-first-only plan is superseded by the later owner-approved Hybrid Experience decision.

### 2.2 Product scope
**In scope for the approved crypto product:**
- crypto assets, meme coins, on-chain intelligence;
- token discovery, opportunity research, risk assessment;
- public wallet/whale intelligence and portfolio analysis;
- signal lifecycle, simulation, analytics, activity, performance;
- content preparation, approval, private-channel distribution, and click/event reporting;
- free and permitted data sources, with explicit freshness/provenance.

**Out of scope for v1 unless the owner explicitly changes scope:**
- forex, gold, stocks, commodities;
- live trade execution and movement of user funds;
- custody of user funds;
- paid API dependency, automatic paid upgrades, or unapproved subscriptions;
- public auto-publishing before the private-channel workflow is proven;
- claims of guaranteed returns or unverified performance.

### 2.3 Workspaces
The approved target shell contains:
1. Home — MOXI
2. Discover
3. Intelligence
4. Opportunities
5. Trading Intelligence — decisions and simulation, not live execution
6. Portfolio — public-wallet analysis
7. Activity
8. Performance

Existing routes may be reused, consolidated, redirected, or retired only after route ownership, user journey, and dependency checks. Do not delete working pages just because they are not in the target navigation.

### 2.4 Personas
Approved personas: **MOXI, MR.VIGO, DR.DEX, ECHO**. A fifth persona is not approved; do not invent one.
Each persona ultimately needs a consistent identity system and reusable asset library. Character production is Stage 5, not a substitute for fixing the current product.

### 2.5 Product quality bar
- No placeholder data presented as live.
- Every live metric has source, timestamp, and freshness state.
- Demo/simulation data is explicitly labeled.
- Loading, empty, stale, unavailable, and error states are designed—not hidden.
- Primary workflows work end-to-end, not merely render.
- Responsive behavior and accessibility are part of acceptance.
- Navigation reflects the approved product model, not a collection of disconnected feature routes.

---

## 3. System architecture and repository ownership

| Repository | Responsibility | Ownership boundary |
|---|---|---|
| vixor-APP | Unified VIXOR application, shell, workspaces, account-facing product experience | Orchestrates and presents; must not duplicate engine logic |
| vixor-packages | Canonical shared contracts and reusable packages | Single intended source for shared contracts |
| vixor-hunt | Discovery and opportunity production | Owns discovery logic and source evidence |
| vixor-shield | Risk evaluation and fail-closed risk decisions | Owns risk policy and assessment |
| vixor-trade | Trade lifecycle intelligence and simulation | No live execution or user funds in v1 |
| tg-content-bot | Telegram control, channel configuration, content workflow, approval, publishing, delivery and reporting | Delivery/control plane; not owner of VIXOR engine logic |
| vixor-deliverables | Architecture, master register, decisions, evidence indexes, handoffs | Documentation is not proof that code works |

### 3.1 Target event flow
Free/permitted source → HUNT → canonical event/contract → SHIELD → VIXOR Core / APP orchestration → content/decision workflow → owner approval where required → private Telegram destination → persisted delivery/activity/click evidence → reporting.

Each transition must validate identity, schema version, freshness, authorization, idempotency, and provenance as appropriate.

### 3.2 Shared contract decisions
- Intended canonical source: vixor-packages.
- Target package version 0.2.0 only after validation and owner approval.
- Maintain an explicit adapter between legacy v0.1 snake_case and canonical v1 camelCase.
- Do not silently change wire formats.
- HUNT should consume canonical validators rather than retain an independent vendored source.
- SHIELD should delegate asset identity validation to the canonical implementation.
- TG-BOT's remaining vendored contract must be measured against canonical behavior and removed/adopted only through a reviewed change.
- APP and TRADE adoption must be proven from their actual source and CI, not inferred from repository existence.
- No package publish or production dependency switch without explicit owner approval.

---

## 4. Stage roadmap — original nine stages

| Stage | Target outcome | Current status | Exit evidence |
|---|---|---|---|
| 0. System Map | Repository/system inventory and ownership boundaries | Reported complete in prior handoffs | Current repository map and evidence links retained |
| 1. Crypto-only Scope | Enforce approved product scope | Approved; APP PR #30 merged into main | Scope tests and merged commit evidence |
| 2. Core Contracts & Security Gates | Canonical contracts, security, provenance, and cross-repo compatibility foundation | **ACTIVE — not closed** | All original Stage 2 gates dispositioned; confirmed defects fixed/tested; blockers explicit; contract adoption evidence |
| 3. HUNT/SHIELD/APP Integration | Safe, reproducible producer → risk → APP/control-center integration | Pending Stage 2 | Isolated end-to-end test with no public/real delivery |
| 4. Unified Product Experience | Deliver one coherent VIXOR shell and visible workspace experience | Pending formal stage start; discovery may be prepared in parallel | Reviewed user journeys, route map, visible UI acceptance, tests and owner preview |
| 5. Characters & Assets | Consistent approved personas and reusable 2D/3D asset libraries | Pending | Character sheets, approved identity locks, reusable assets |
| 6. Memory, Activity, Wallets & Notifications | Durable user context, event/activity history, public wallet intelligence and notifications | Pending | Data ownership, permissions, retention, freshness, tests |
| 7. Security, Data, Operations & Payments | Operational hardening, payment correctness, data governance and recovery | Pending as a full stage; security/payment work already overlaps Stage 2 | Security review, operational runbooks, payment tests, recovery and owner approval |
| 8. End-to-End Tests & Owner Approval | Full journey proof and release decision | Pending | Reproducible E2E evidence and explicit owner sign-off |

**Stage order remains authoritative.** Stage 4 preparation can run as non-production discovery and backlog grooming, but Stage 3/4 implementation must not be represented as complete or used to bypass Stage 2 acceptance.

---

## 5. Verified repository baseline — 2026-11-02 snapshot

The following default-branch heads were read from GitHub during this snapshot. They are repository baselines, not proof of deployment:

| Repository | Default branch | Verified SHA | Latest visible commit date |
|---|---|---|---|
| vixor-deliverables | main | af62a0051b961cdc932d6009bd73c476744a6591 | 2026-10-27 |
| vixor-APP | main | e746c4087823bb205cafc7988c54ae4c13ea3427 | 2026-10-31 |
| vixor-packages | main | d58e7268f366923c82819756466719a1bdd39315 | 2026-10-20 |
| vixor-hunt | main | ceeb2474d3b20cf556e45abd0e9798739a0d887f | 2026-10-06 |
| vixor-shield | main | f21b56223758f5c6f82d611ad9a04a798ca1a3db | 2026-10-28 |
| vixor-trade | main | 6fab976c65bedf5b351cb65307b9d38dfdd2df96 | 2026-10-08 |
| tg-content-bot | main | 63c0c5475debcc8e9815e67296fd71556a17e903 | 2026-11-02 |

### 5.1 Important freshness warning
- The current APP main head e746c40 is newer than several prior APP audit snapshots.
- The current TG-BOT main head 63c0c54 is newer than the October 31/November 1 handoffs. Any task touching TG-BOT must inspect this head and current PR bases first.
- vixor-packages, HUNT and TRADE have older visible main commits; do not assume their local or PR branches are represented on main.
- GitHub access to these repositories is available through the connected GitHub integration in this session. Do not use exposed PAT files or credentials from repositories.

---

## 6. Existing work that must be preserved

### 6.1 APP payment remediation
- Local branch: task44r/payments-remediation
- Reported head: 6e65480
- Base: e746c40
- Reported scope: Telegram Stars payer-to-order identity binding, fail-closed identity validation, payment tests included in Vitest, isolated SQL harness.
- Reported evidence: 1060/1060 Vitest, typecheck clean, lint 0 errors (15 pre-existing warnings), Prettier clean, build passed with 3 GB Node heap, PGlite 74/74.
- Status: implemented/tested locally per Agent 1 report; not pushed, not merged, not production verified.
- **Preservation rule:** do not modify or rewrite this branch. Build any follow-up in a separate branch and explicitly compare changes.

### 6.2 APP Gate 5 RLS/GRANT review
- Local branch: task44r/gate5-rls-grant-review
- Reported head: 7d65524
- Base: e746c40
- Reported evidence: PostgreSQL 16.15 isolated cluster, security matrix, concurrency lock test, 7/7 regression tests, negative control.
- Status: local branch and evidence per Agent 1 report; not pushed, not merged, not production verified.
- **Preservation rule:** do not modify or overwrite this branch.

### 6.3 TG-BOT FIX-01 contract mismatch
- Branch: task44r/fix-01-risk-assessment-mismatch
- Reported head: a2beaf533277e400179f113f5b5ace7387eef684
- Reported base: f9f631a3cc4de0571434356d6af3c2c677cf8bb3
- Reported evidence: compatibility 8/8, E2E 8/8, chain 16/16, smoke 106/106, type checks clean, battery 41/41.
- Status: local branch/evidence per Agent 1 report; push blocked in prior session; not merged or production verified.
- Do not transplant into current main until the branch base and current TG-BOT PR stack are reconciled.

### 6.4 Contract adoption evidence
- TASK44R Gate 3 adoption/drift matrix SHA256 reported: d29fbfc22d0af3bc81a8c2bc6ce4b3e4657ad399b4696db7a14dc3370e950578.
- Reported findings: HUNT consumes @vixor/contracts through transitional file dependency; SHIELD delegates identity validation; TG-BOT has a structurally vendored copy with behavior parity reported after FIX-01; APP had zero @vixor dependencies at the time; TRADE access was blocked at that time.
- These are historical/branch-level findings. Refresh against the verified current heads before closing any adoption gate.

### 6.5 Other protected work
- APP PR #26 must remain untouched pending an owner decision; its current head/base must be rechecked before any interaction.
- Existing TG-BOT PR stack must be inspected before changing overlapping paths.
- Dirty local worktrees, archives, patches, and evidence must be preserved.
- Never rebuild a working feature just to make the branch history look cleaner.

---

## 7. Current open pull-request and collision map

### 7.1 vixor-APP
At snapshot time, open PR #26:
- Title: Prevent premium activation without verified payment.
- Head: c5f3c5ef1458fffb8b8cc7d6113be785dec1b50e.
- Base: main.
- This is not the same as the unpushed local payments-remediation branch at 6e65480.
- Prior handoff reported overlapping files with the payment remediation branch and a stale base. Do not rebase, close, supersede, or modify PR #26 without an owner decision and a fresh diff review.

### 7.2 tg-content-bot
At snapshot time main is 63c0c54 and the following open PRs were visible. Several are stacked; their base branches are not main. Do not merge or flatten them blindly.

| PR | Topic | Head | Base | Handling |
|---|---|---|---|---|
| #65 | Preserve durable Outbox rows on grant revoke | ae39aad | main | Review current main compatibility |
| #54 | Crypto-only content scope CI gate | 6bb5b98 | stage1/crypto-only-content-scope | Stacked; reconcile with #53 |
| #53 | Stage 1 crypto-only scope | ddadb37 | scheduler reliability branch | Stacked |
| #52 | Scheduler reliability integration | f9f631a | content workflow branch | Check stack and current main |
| #51 | Agent 1 content workflow vertical slice | ce95ae2 | content-ops contract branch | Stacked |
| #50 | Asset-library browser recovery test | 1b69181 | asset-library finalize branch | Stacked |
| #49 | Content delivery scheduler/APIs | 8dd5cd2 | content-ops contract branch | Stacked |
| #48 | Reliability R-16 and tests | fa5e8b1 | main | Review independently |
| #46/#44/#42/#41 | Asset-library recovery/retry chain | multiple | stacked branches | Preserve chain; verify in order |
| #45 | Campaign ownership lookup | f39105a | content-ops contract branch | Stacked |
| #40 | Content-ops migration assertion | ef48765 | channel-niche UX branch | Stacked |
| #36 | Channel niche isolation | 3095de8 | main | Review visible product impact |
| #34 | Channel niche UX | 0464418 | content-ops branch | Stacked |
| #31 | Content Operations Center / Channel Studio | ef8885a | main | Major visible product work; inspect before changes |
| #27/#26 | Wrangler lock refresh | multiple | main/stacked | Infrastructure; avoid unrelated edits |
| #24 | Reject mismatched embedded Shield assessments | 4b20c77 | main | Contract/security fix |
| #23 | Consolidated register with payment RLS findings | 4fbb917 | main | Documentation branch |
| #21 | Correct audit handoff | a2d01cd | main | Documentation branch |
| #2 | UX foundation | 446af6a | main | Historical open PR; inspect overlap |

**Important:** this is a discovery snapshot, not a full PR review. For any touched PR, fetch its full metadata, changed filenames, diff, CI checks, and latest base/head first.

---

## 8. Consolidated issue register

Statuses use: **Confirmed**, **Possible Risk**, **Not Verified**, **Blocked**, **Remediated on branch**, **Integrated**, **Production Verified**. Never infer a stronger state than the evidence supports.

### 8.1 Stage 2 — contracts, identity, and security

| ID | Severity | Finding / impact | Current disposition | Next action |
|---|---|---|---|---|
| T44-08 / FIX-01 | High | TG-BOT accepted a risk assessment whose embedded opportunity_id could differ from payload opportunity_id | Reported remediated/tested on local branch a2beaf5; unpushed | Reconcile branch against current TG-BOT main and PR stack; retain tests |
| T44-13 | Medium | Push/access and PR-base uncertainty blocked normal delivery | Prior push failure reported; current GitHub connector access is available for repository review | Recheck branch availability and authorized path; do not use stored PAT |
| T44-14 | High | Contract adoption/drift differed across HUNT, SHIELD, APP, TRADE, TG-BOT | Historical local matrix; not current production proof | Refresh all repos and verify canonical package adoption |
| T44-15 | High | APP Stars payment identity binding missing; payer could fulfill another user's order | Reported fixed/tested on local branch 6e65480 | Preserve branch; validate G5-05 dependency and reconcile PR #26 |
| G5-01 | Critical | points_balances RLS policy without explicit TO scope allowed authenticated users to directly alter balances | Reported exploit reproduced on isolated PG16; remediation proposed on branch 7d65524 | Review migration and CI evidence; do not apply live |
| G5-02 | High | execute_signal_transition SECURITY DEFINER executable by PUBLIC and lacked fixed search_path | Reported exploit reproduced on isolated PG16; remediation proposed on branch 7d65524 | Review exact SQL, grants, negative/positive tests |
| G5-03 | High | Production definition/provenance of credit_points and points_reason missing from tracked migrations | Confirmed repository provenance gap; production definition unknown | Locate authoritative production DDL; do not invent a stub as production schema |
| G5-05 | Critical | profiles.telegram_id is writable through a client-controlled server function and an owner UPDATE policy; self-relink/squatting can undermine payer identity binding | **Confirmed by current APP main source review:** AppShell reads initDataUnsafe and sends telegramId; syncTelegramProfile accepts caller-supplied telegramId under auth-only middleware and writes it through supabaseAdmin. Migration 20260803000000 grants own-row UPDATE policy. linkTelegramAccount separately verifies signed initData. No runtime exploit test was run in this review. | Remove telegram_id from the auto-sync input/write path; enforce server-verified initData for linking; prevent authenticated direct column updates; add tests for forged ID, cross-account collision, valid link, relink and payment payer mismatch |
| G5-08 | High | Migration chain cannot bootstrap cleanly; forward references, incompatible FK types, volatility and enum/text drift | Confirmed repository migration-chain defect; production schema provenance unresolved | Reconcile actual production schema and migration history; no blind historical rewrite |
| G5-09 | Medium | P0004 ASSERT_FAILURE is not caught by WHEN OTHERS | Reported confirmed by PostgreSQL experiment | Decide intended error semantics and add targeted regression |
| G5-10 | High | Actual package distribution/canonical adoption not proven across all consumers | Possible/Not Verified per prior evidence | Prove installable package distribution and consumer compatibility |
| G5-11 | High | Freshness declarations/runtime and legacy v0.1/v1 adapters may drift | Prior declaration-only and adapter fixes reported | Refresh compatibility tests on current heads |
| G5-12 | High | APP/TRADE access and schema provenance were previously incomplete | Not Verified/current state may have changed | Inspect current accessible repositories and record any remaining access boundary |

### 8.1.1 Current-source proof for G5-05 (APP main e746c40)

- File: src/components/vixor/app-shell/index.tsx. The auto-sync effect reads Telegram WebApp initDataUnsafe.user and passes tgUser.id to syncTelegramProfile.
- File: src/domains/user/functions.ts. syncTelegramProfile uses requireSupabaseAuth, accepts telegramId as a client-supplied number, and writes String(data.telegramId) to profiles using supabaseAdmin. It does not verify Telegram initData.
- Same file: linkTelegramAccount does verify signed initData through verifyTelegramInitData before writing telegram_id. This is the correct trust boundary to preserve.
- Migration: supabase/migrations/20260803000000_add_missing_core_tables.sql creates an owner-scoped UPDATE policy on profiles. Row ownership does not restrict which columns the owner may update.
- Finding: a signed-in user can submit an arbitrary Telegram ID to the sync server function; this is a source-confirmed trust-boundary defect. Direct PostgREST writeability must also be tested against effective grants/RLS in isolated PostgreSQL/Supabase-compatible tests.
- Safe remediation direction: make syncTelegramProfile update only non-identity display metadata, derive Telegram identity only from server-verified initData, and deny direct authenticated writes to telegram_id (using a DB-enforced control compatible with actual Supabase roles). Do not assume a client-side UI restriction is sufficient.
- Evidence reviewed: current APP main e746c4087823bb205cafc7988c54ae4c13ea3427; files above. This source review did not execute the app or database and is not production verification.

### 8.2 Control center and Telegram reliability
The following are carried forward from the owner-visible execution status and earlier integration audit. Their current status must be refreshed against TG-BOT main 63c0c54 and current PRs.

| ID | Severity | Finding / impact | Current status | Next action |
|---|---|---|---|---|
| BOT-01 | High | Media album retry/recovery behavior | CI/PR evidence historical | Inspect current main and PR stack; verify buffer reopen, retry and dedup |
| BOT-02 | High | Telegram update processing lease and stale worker fencing | Distributed behavior not proven historically | Test concurrent claims, lease expiry, fencing and redrive/webhook race |
| BOT-03 | High | Draft/classification idempotency | Isolated migration/test evidence historical | Verify full current migration chain and concurrent insert/upsert |
| BOT-04 | High | Short-link write privileges | Isolated SQL hardening evidence historical | Verify effective grants and legacy policy interactions |
| BOT-05 | High | Full migration-chain repeatability | Previously open | Run ordered full chain from clean isolated DB and document exact result |
| BOT-06 | Critical | Telegram webhook acknowledgement/retry durability | Prior audit marked P0 design gate | Prove durable inbox/queue, retry semantics, dead-letter visibility and safe acknowledgement |
| BOT-07 | Critical | TG-BOT RLS/grants and sensitive table access | Prior audit marked P0 security gate | Verify roles/actions, anon/auth denial, service-role scope and current migrations |
| TGB-PR-STACK | High | Numerous stacked PRs and overlapping migration/workflow files | Confirmed from current open PR listing | Build dependency graph, inspect changed-file overlap, do not flatten or merge blindly |
| TGB-OUTBOX | High | Outbox retention/claim/retry semantics | PR #65 and prior reliability work | Verify durable delivery and revocation semantics with real isolated PostgreSQL tests |

### 8.3 APP product and runtime
| ID | Severity | Finding / impact | Current status | Next action |
|---|---|---|---|---|
| APP-UI-01 | High | Published UI reported older than approved Hybrid Experience; obsolete/disagreed elements remain visible | Owner-reported; current deployed build not verified in this snapshot | Map deployed commit to routes and owner-approved workspace/navigation; prepare visible redesign backlog |
| APP-ROUTES-01 | High | Many legacy/overlapping routes exist alongside target workspaces | Confirmed from current APP tree enumeration; impact needs route-level review | Build route inventory: active, duplicate, legacy, redirect, feature-flagged, broken |
| APP-DATA-01 | High | Need clear distinction between demo/mock/stale/live data | Historical audit risk; current UI state not yet fully inspected | Trace each Home/Discover/Intelligence metric to source, timestamp, freshness, and empty/error state |
| APP-ARB-01 | Medium | Arbitrage active-vs-archived status uncertain in historical audit | Not Verified on current head | Trace current imports/routes/migrations and mark active or archived without deleting |
| APP-PAY-01 | Critical | Stars identity/payment remediation and RLS integration | Branch-level work only | Preserve 6e65480 and 7d65524; reconcile PR #26; no live migration |
| APP-PR-26 | High | Existing premium-payment PR overlaps payment remediation and may be stale | Open at snapshot; head c5f3c5e | Inspect full diff/base/CI; owner decision before rebase/supersede |

### 8.4 Product and operations
| ID | Severity | Finding / impact | Current status | Next action |
|---|---|---|---|---|
| PROD-01 | High | Product navigation/feature density does not yet reflect the approved single-product Hybrid model | Owner-reported and route inventory supports review | Produce one coherent shell and prioritize 8 workspaces |
| PROD-02 | High | Broken/incomplete Moxi 3D and character experience | Owner-reported | Defer asset production to Stage 5; remove broken presentation from primary journey only after safe UX review |
| OPS-01 | High | Owner-visible progress must reflect actual code/CI/deployment/e2e state | Current master register established here | Maintain this file as canonical status |
| OPS-02 | High | Production commit/deployment provenance not proven across all repos | Not Verified | Map Vercel/Cloudflare deployed version to exact commit; no deploy |
| SEC-SECRET-01 | Critical | Historical secret/token exposure and rotation concern | Historical handoff says owner action required; current secret validity not verified | Never read or repeat secret values; owner rotates through provider UI; verify only non-secret result |
| E2E-01 | Critical | Full HUNT → SHIELD → APP/control center → approved private Telegram delivery not proven | Open / release blocker | Isolated end-to-end test with deterministic fixture, no real/public delivery |

---

## 9. Prioritized execution plan

This is the single active work queue. Reorder only with owner approval or when a verified dependency requires it.

### P0 — protect payment, balances, and delivery integrity
1. Review G5-01/G5-02 migrations and regression wiring on the Gate 5 branch.
2. Resolve G5-05: server-verifiable Telegram linking and client-write denial.
3. Reconcile G5-05 with payment branch 6e65480 and APP PR #26 without modifying either.
4. Locate authoritative credit_points/points_reason production DDL (G5-03).
5. Resolve intended P0004 handling (G5-09).
6. Refresh TG-BOT main and review current Outbox/webhook/idempotency PR stack.
7. Verify secret exposure/rotation status without reading or handling secret values.

### P1 — finish Stage 2 contract gates
1. Retrieve the original G1/G4/G7 definitions and exact acceptance criteria from TASK44/TASK44R evidence; do not invent missing definitions.
2. Reconcile G1/G4/G7 against current repository heads and existing branches.
3. Prove canonical contract distribution/adoption for HUNT, SHIELD, APP, TRADE and TG-BOT.
4. Verify freshness, provenance, envelope versioning, legacy adapter and drift tests.
5. Resolve migration provenance (G5-08) using authoritative schema evidence.
6. Run cross-project compatibility tests on current heads and focused PR heads.

### P2 — visible product preparation and first owner preview
1. Inventory APP routes and map them to the approved 8 workspaces.
2. Identify obsolete/duplicate routes and the smallest safe consolidation path.
3. Audit Home, Discover, Intelligence and Opportunities for real data, freshness, empty/loading/error states.
4. Review the current AppShell and navigation against Hybrid Experience.
5. Prepare a non-production visual preview branch with one cohesive owner-visible improvement only after route ownership and Agent 1 collision checks.
6. Keep all changes isolated and tested; no production deployment without approval.

### P3 — after Stage 2 exit
Proceed in order through Stage 3 integration, Stage 4 product experience, Stage 5 personas/assets, Stage 6 user intelligence, Stage 7 operations/payments, and Stage 8 E2E/owner approval.

---

## 10. Engineering collaboration and conflict-avoidance protocol

### Agent 1
- Sole delegated implementation agent.
- Must announce repository, branch, base SHA, intended file paths, and task ID before editing.
- Must not edit files reserved by the technical lead.
- Must report exact commits, tests, and status.

### Technical lead / independent engineering
- May inspect current GitHub source, review PRs, prepare architecture and issue documentation, and implement isolated changes when the environment supports full testing.
- Must create a separate branch/worktree.
- Must never edit Agent 1's active branch or dirty worktree.
- Must reserve file paths before implementation and communicate ownership.
- If local execution/testing is unavailable, do not label a source change as tested. Use read-only review or a Draft PR with CI evidence, and clearly state the limitation.

### File ownership reservation
Before parallel implementation, append a reservation:
- Task ID
- Repository
- Branch/base SHA
- Owned paths
- Start time
- Expected completion
- Release of reservation

No two agents may edit the same path concurrently.

### Branch discipline
- Never reset, force-push, delete, or overwrite.
- One branch per focused remediation.
- Preserve historical branches and PRs.
- Check current main and merge-base before every PR action.
- Draft PR only; no merge/deploy without owner approval.
- Never use exposed PATs or credential files.

---

## 11. Acceptance and evidence standards

Every task must carry these separate states:

| State | Meaning |
|---|---|
| Specified | Acceptance criteria written |
| Implemented | Code/config change exists |
| Tested | Relevant local/CI tests pass |
| Integrated | Cross-project behavior proven |
| Pushed | Commit exists on remote branch |
| Draft PR | Reviewable PR exists |
| Merged | Included in target default branch |
| Deployed | Exact commit deployed to target environment |
| Production Verified | Real production behavior verified with safe read-only evidence |

### Minimum evidence
- repository and exact SHA;
- exact changed paths;
- test commands and exit codes;
- CI run URL and result;
- before/after behavior for a bug fix;
- negative test proving the regression test catches the defect;
- integration proof when a boundary is involved;
- deployment commit mapping when claiming production state;
- explicit owner approval for gated operations.

### Completion rule
A task is not Done merely because a branch exists, a test fixture passes, or an agent reports success. A stage is not closed while required acceptance criteria are unknown or hidden behind unresolved blockers.

---

## 12. Owner decisions required

1. **APP PR #26:** retain/rebase/reposition/supersede decision after a fresh diff review; do not act until decided.
2. **Payment identity policy:** approve server-only Telegram identity linking and rejection of client-side telegram_id writes.
3. **G5-03/G5-08:** provide or authorize a safe read-only route to authoritative production schema/migration provenance if not present in accessible repositories.
4. **G5-09:** approve intended SQL error behavior after technical recommendation.
5. **Secret rotation:** owner performs rotation in provider UI; no secret value is shared.
6. **Production changes:** each merge, migration, deploy, package publish, or real Telegram action requires explicit approval.

---

## 13. Current status summary

### Done / evidenced
- Product scope and Hybrid Experience decisions are recorded.
- Repository responsibilities and current main SHAs have been refreshed.
- Existing payment, Gate 5, and TG-BOT FIX-01 branch reports are preserved.
- Current open TG-BOT PR stack and APP PR #26 are identified.
- A single master register has been established as the working coordination source.

### In progress
- Stage 2 contract/security closure.
- Gate 5 remaining remediation and provenance.
- Current PR stack review and branch collision analysis.
- APP visible-product route/data audit preparation.

### Blocked / not verified
- Authoritative production DDL for credit_points/points_reason.
- Production schema/migration provenance.
- Telegram identity linking security fix not yet implemented/verified on current remote branch.
- Full canonical contract adoption and distribution across all consumers.
- Full producer → Shield → APP/control-center → private Telegram E2E.
- Exact deployed commit and production behavior for all services.
- APP current deployed UI versus approved Hybrid Experience.

### Percentage
No overall completion percentage is published yet. The original Stage 2 G1/G4/G7 acceptance definitions and the complete gate denominator must first be reconciled from source evidence. Any percentage before that would be misleading.

---

## 14. Change log — append-only

| Date | Change |
|---|---|
| 2026-11-02 | Created canonical master vision/audit/execution register on a dedicated documentation branch. Refreshed GitHub default-branch SHAs for all seven core repositories and current open PR inventory for APP and TG-BOT. Independently inspected APP main and confirmed the G5-05 unverified Telegram ID auto-sync path in source. No application code, production environment, database, secret, or deployment changed. |

### Update protocol
Every future update must append:
- date/time;
- task/gate ID;
- repository/branch/base/head;
- files changed;
- tests and CI;
- result;
- remaining blocker;
- owner decision required.

Do not silently rewrite history. Correct old entries by appending a dated correction.
