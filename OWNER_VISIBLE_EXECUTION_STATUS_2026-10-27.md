# Owner-visible execution status — 2026-10-27

**Purpose:** Current evidence-backed work queue for the VIXOR × tg-content-bot ecosystem. This is a status snapshot, not a claim that every application is integrated or deployed.

## Owner summary

- **Verified green:** tg-content-bot PR #20 CI at commit 3e79428f7774caa40648060920b7af52b6a96af7; run 40440971027. The run passed PostgreSQL migration integration, bot-worker typecheck/smoke tests, and mini-app typecheck.
- **Not yet delivered to the default branch:** tg-content-bot PR #20 remains draft/open. Do not treat its code as part of main or the live app.
- **Cross-product integration is incomplete:** Hunt PR #1 and Shield PR #2 remain draft/open. The owner-facing end-to-end journey from producer → risk assessment → control-center intake → approved private-channel delivery has not been demonstrated against deployed services.
- **No production changes are claimed:** this status update does not merge PRs, deploy apps, run production migrations, publish content, or activate live trading.

## Task register

| ID | Area | Status | Evidence / current state | Next action / acceptance |
|---|---|---|---|---|
| BOT-01 | Telegram media album retry/recovery | CI green; review pending | PR #20; CI run 40440971027 success | Independently review failure propagation, buffer reopen behavior, retry timing and duplicate handling; keep draft until edge-case tests and review pass |
| BOT-02 | Telegram update processing lease | Implemented on PR branch; distributed behavior not proven | claimUpdateProcessing helper and webhook wiring included in PR branch | Test actual PostgreSQL/Supabase concurrent claims, lease expiry, stale worker/fencing and redrive-vs-webhook race |
| BOT-03 | Draft/classification idempotency | Migration/test coverage added on PR branch; real Supabase behavior unverified | migration 026 plus isolated PostgreSQL integration | Verify constraints against real Supabase-compatible schema in isolated staging; prove concurrent insert/upsert produces one logical result |
| BOT-04 | Short-link write privileges | SQL hardening added and isolated test green | migration 025; isolated PostgreSQL integration in CI | Review effective grants, legacy policy names, service-role behavior and production migration order before approval |
| BOT-05 | Full migration repeatability | **Open / blocker** | 008 and 009 rerun issues were fixed; only focused migration integration (008 + 025 + 026) is proven in CI | Run the full ordered migration chain from a clean isolated database, then rerun according to documented policy; record exact failing migration or full pass |
| BOT-06 | Telegram webhook delivery/recovery | **Open / P0 design gate** | Prior audit found early acknowledgement/background work and fail-open idempotency concerns | Define durable inbox/queue, retry semantics, dead-letter visibility and safe acknowledgement before production integration |
| BOT-07 | Supabase RLS/grants in control center | **Open / P0 security gate** | Prior audit identified broad anon_full_access policies in migration 001; no live grants inspection claimed | Map every sensitive table to roles/actions; test anon/authenticated denial and owner/service-role access in isolated staging; reviewed migration only after evidence |
| SHARED-01 | Shared integration contract | Partial / branches need reconciliation | Contract docs exist; Hunt PR embeds a contract copy and states a sync rule | Establish one canonical versioned contract package; add compatibility test preventing drift across Hunt, Shield, Trade and bot |
| SHIELD-01 | Risk assessment endpoint | Draft; CI/runtime integration pending | PR #2 (feat/assess-endpoint) claims fail-closed behavior and nonce migration 0006 | Verify latest CI, schema validation, replay behavior, nonce atomicity, expiry and engine failure; do not treat as mandatory gate until evidence is green |
| HUNT-01 | Deterministic test-opportunity emitter | Draft; no live E2E proof | PR #1 (feat/test-opportunity-emitter) includes fixture, HMAC sender and deterministic key | Verify contract equality against canonical package and run duplicate request against a test deployment: first accepted, replay rejected |
| TRADE-01 | Trade producer and security | Open / audit required | Current audit notes query-string secret risk at GET /debug/brief, batch replay/staleness and shallow validation concerns | Remove secrets from URLs, validate schema and timestamp ordering, add replay/concurrency tests; preserve DRY_RUN/no live execution |
| APP-01 | APP current default branch and route integrity | Recheck required | PR #25 handoff merged at b893b6299f3bc9cfd4e8ab0361d61e60f80cf661 (historical evidence) | Fetch latest default-branch SHA and CI; map active routes, auth boundaries, data provenance and mock-vs-live flags |
| APP-02 | Arbitrage module state | **Open / evidence blocker** | Prior source audit found Arbitrage under archive/domains/arbitrage/, not expected active src/domains/arbitrage/; migration presence alone does not prove deployed state | Trace imports/routes/history and migration ledger in isolated environment; do not delete archived files or claim feature active until reconciled |
| OPS-01 | Owner-visible progress and deliverables | In progress | This file records status, proof links and next acceptance steps | Keep this registry updated with commit, CI run, PR, test output and blocker; expose owner-facing progress in the control center only after source-of-truth data model is agreed |
| E2E-01 | Hunt → Shield → bot → private test destination | **Open / release blocker** | No verified deployed end-to-end run currently recorded | Send one deterministic fixture through real test endpoints; prove auth/signature, freshness, asset identity, risk gate, owner approval, private destination allowlist, idempotency and no duplicate delivery |
| DOC-01 | Master plan reconciliation | **Open** | Existing audit says VIXOR_MASTER.pdf text extraction/reconciliation was blocked; current CI evidence must be refreshed per repository | Extract PDF text and compare with GLM5/POD and actual source; update file matrix with evidence and exact SHAs |

## Cross-repository review queue

1. Refresh default branch SHA and latest CI for vixor-APP, vixor-deliverables, vixor-packages, vixor-hunt, vixor-shield, vixor-trade, and tg-content-bot.
2. Enumerate all open/draft PRs and agent branches. For each: compare against current base, inspect changed paths, identify overlap/conflicts, review test claims, and label as accept / request changes / blocked with evidence.
3. Confirm the canonical contract and compare all embedded copies byte-for-byte or with schema compatibility tests.
4. Test the complete route/data journey, including authorization, failure, retry, stale input, replay, and duplicate delivery.
5. Create an owner-visible release evidence page listing app URL, deployed commit, last successful CI, content/signal freshness, pipeline status, and last error. Do not show a green “connected” state merely because a producer repo exists; distinguish code present, CI passed, deployed, and end-to-end verified.

## Priority order

- **P0:** prove and close control-center RLS/grants; safe Telegram ack/retry/idempotency; verify secret handling; preserve owner approval and private destination allowlist.
- **P1:** full migration chain repeatability; real concurrent claim/idempotency/fencing tests; canonical shared contract; Shield fail-closed/replay tests.
- **P1:** refresh all repository CI and inspect all agent PRs for stale bases, path overlap, conflicting contract copies and unsupported completion claims.
- **P2:** APP route/data-source audit and active-vs-archived Arbitrage reconciliation.
- **P2:** owner-facing status/content dashboard based on persisted evidence, with freshness and explicit blocked/degraded states.

## Evidence links

- tg-content-bot PR #20: https://github.com/kam65624-cmd/tg-content-bot/pull/20
- tg-content-bot CI run 40440971027: https://github.com/kam65624-cmd/tg-content-bot/actions/runs/40440971027
- Hunt PR #1: https://github.com/kam65624-cmd/vixor-hunt/pull/1
- Shield PR #2: https://github.com/kam65624-cmd/vixor-shield/pull/2
- APP merged handoff PR #25: https://github.com/kam65624-cmd/vixor-APP/pull/25
- Existing integration audit: https://github.com/kam65624-cmd/vixor-deliverables/blob/main/INTEGRATION_AUDIT.md
- Existing file matrix: https://github.com/kam65624-cmd/vixor-deliverables/blob/main/PHASE0_FILE_MATRIX.md
- Task registry: https://github.com/kam65624-cmd/vixor-deliverables/blob/main/AGENT_TASK_REGISTRY_V1.md

## Completion rule

A task may be marked **Done** only when there is an exact commit SHA, the relevant test/CI run passes, the expected behavior is verified at the appropriate integration level, and its owner-facing result is reachable. A PR or a green isolated unit test alone is not proof of production delivery.


## Findings added during independent PR review — 2026-10-27

### CONFIRMED: tg-content-bot PR overlap / stale base

- tg-content-bot PR #2 (UX foundation) was based on main SHA 0bc925da9f9c474b32125f56d55465f15cd26497; current main at review time is 2d8933ed7cd92d23144099642497f32794340715.
- PR #2 and PR #20 both modify supabase/migrations/009_multi_bot_rbac_workflows.sql. PR #2 adjusts JSON handling for workspace_members; PR #20 adjusts anonymous-policy cleanup. These changes must be reconciled, not discarded.
- A review comment was posted to PR #2 requesting sync/rebase, preservation of both changes, and fresh typecheck/build/visual regression evidence.

### CONFIRMED: Shield response can violate the shared contract

- In vixor-shield PR #2, src/index.ts treats opportunity_id as optional and passes null to assessFromScan / assessEngineError.
- src/assess.ts declares and can return opportunity_id: string | null.
- The shared contract in vixor-packages PR #2 and the vendored contract validators in Hunt and tg-content-bot require opportunity_id to be a non-empty string.
- Therefore a correctly signed request with a valid subject/nonce but missing opportunity_id can produce HTTP 200 with a response that downstream contract validation rejects. This is a confirmed interface mismatch from source inspection; it has not been tested against a deployed endpoint.
- A review comment was posted to Shield PR #2 requesting required-field validation and a negative test, or an explicitly coordinated versioned contract change. It also requests validation that parsed JSON is a non-null object.

### Refreshed CI evidence

- vixor-APP main: commit b893b6299f3bc9cfd4e8ab0361d61e60f80cf661; CI run 40123959641 succeeded on 2026-10-24.
- vixor-hunt PR #1: CI run 39535211707 succeeded on its PR head; main CI run 37870183208 succeeded on 2026-10-09.
- vixor-shield PR #2: CI run 39534895611 succeeded on its PR head; main CI run 39361555785 succeeded on 2026-10-20.
- vixor-trade: latest listed run 40432184084 succeeded on main commit 6fab976c65bedf5b351cb65307b9d38dfdd2df96, but it is the scheduled batch-compute workflow, not a full CI suite.
- vixor-packages PR #2 is open/draft and has no current default-branch merge. Contract package and vendored copies therefore remain separate sources until consolidation is accepted and verified.
- tg-content-bot PR #20 CI run 40440971027 passed on its head; PR remains draft/open. tg-content-bot PR #2 is also open, not merged.

## Additional acceptance gates

- Resolve the tg-content-bot PR #2 / #20 overlap and refresh PR #2 against current main.
- Resolve Shield nullable opportunity_id versus shared contract mismatch, then run contract compatibility tests across package, Hunt, Shield and bot.
- Treat green PR CI as branch-level evidence only. No production deployment, live endpoint E2E, or public content publication is established by the listed runs.


## Fix started after the findings above

A targeted fix was committed to the existing Shield PR branch (not main):
- Commit 4da31dfee3ad9f6b01013d833dc40914ac907a6d adds pure request validation for nonce, subject and required opportunity_id.
- Commit 0c77897aae57c24522daead1c0c0ef8fe8e246f4 wires validation into POST /assess before the nonce is consumed, preventing malformed requests from burning a nonce and preventing nullable opportunity_id responses.
- Commit a1b884779e2b82191252535ccccd05b4946a999b adds tests for null/array/non-object input, missing/blank required fields, normalization, and size limits.
- CI was triggered for these commits (runs 40441695742, 40441713657, 40441729919); at the time this note was written, the newest run was queued/in progress. This fix is **not marked verified** until the run for the latest head completes successfully and its logs are inspected.


## Verification update — Shield targeted fix CI is green

The latest Shield PR head commit is a1b884779e2b82191252535ccccd05b4946a999b. CI run 40441729919 completed successfully: typecheck, unit tests, wording policy, secret scan and bundle-size check all passed. Earlier intermediate runs 40441695742 and 40441713657 also passed. This verifies the validator and unit-test changes on the PR branch; it does **not** verify a deployed HTTP endpoint or cross-repository E2E. Shield PR #2 remains draft/open and is not merged or deployed.

Next Shield acceptance: add/retain a route-level test proving invalid requests return 400 before nonce insertion, confirm canonical contract compatibility in the shared-contract integration suite, then run a test deployment E2E before the risk gate can be considered production-ready.


## Additional confirmed concurrency limitation — tg-content-bot

Source review of PR #20 confirms that the claim lease is represented by drive_claimed_at, but completion in markUpdateProcessed is keyed only by bot_label + update_id and does not verify that the completing worker still owns the same claim. A worker that runs longer than the five-minute lease could overlap with a redrive worker after lease expiry; the stale worker can still mark the row processed. The current fake-Supabase test does not establish distributed PostgREST concurrency or stale-worker fencing.

A review comment was posted on PR #20. Acceptance is blocked until a claim token/fencing generation or equivalent conditional completion is implemented and tested under real PostgreSQL concurrency. Do not mark BOT-02 complete based only on the current green CI.


## Trade security repair started — CI pending

A targeted security PR was opened: https://github.com/kam65624-cmd/vixor-trade/pull/2
- Branch: fix/ops-secret-header-20261027
- Head: 7faebe5bcc4b6b8ed81ae65b4bef4b73f4e4898a
- Replaces GET /debug/brief?k=... with POST /debug/brief and Authorization: Bearer header, adds unit tests for authorization parsing, and documents the new request method.
- CI run 40442004448 was queued at the time of this update; this fix is not marked verified until that exact head passes.
- Compatibility review remains required: no in-repository caller was found in README, deploy/setup scripts, CI workflows or scheduled compute workflow, but external/manual callers have not been ruled out.
- Follow-up security improvement: use a dedicated OPS_AUTH_SECRET rather than reusing WEBHOOK_SECRET; not included because that requires owner-approved secret provisioning.


## Verification update — Trade ops-secret repair CI is green

Trade PR #2 head 7faebe5bcc4b6b8ed81ae65b4bef4b73f4e4898a passed CI run 40442004448: typecheck, unit tests (including new bearer-auth tests), wording policy, secret scan and bundle-size check. See https://github.com/kam65624-cmd/vixor-trade/actions/runs/40442004448. The PR remains draft/open and no deployment was performed. Follow-up remains: decide whether to provision a dedicated OPS_AUTH_SECRET and check external/manual callers before merge.


## Verification update — Telegram stale-worker fencing CI is green

The tg-content-bot PR #20 branch now includes claim-token fencing:
- claimUpdateProcessing returns the exact lease token stored in drive_claimed_at.
- webhook and scheduled redrive pass that token to completion/error writes.
- markUpdateProcessed and recordProcessError condition their writes on the same token and refuse stale-worker repair-upserts when the token no longer matches.
- A regression test replaces the lease token and proves the stale worker cannot mark the row processed.
- Latest head: 56356a4c64e39535cb81b15b2e810c8e6e2c9681.
- CI run 40442224906 passed all three jobs: mini-app typecheck, PostgreSQL migration integration, and bot-worker typecheck/smoke + ALERT-01 regression. Smoke output: 92 passed / 0 failed; ALERT-01: 20 passed / 0 failed. https://github.com/kam65624-cmd/tg-content-bot/actions/runs/40442224906

This closes the stale-worker completion gap for tracked rows when a claim token is available. It does **not** close the separate fail-open path when ledger ingestion itself fails and the handler continues without a durable claim; durable inbox/ack/retry design and real Supabase concurrency remain open blockers. PR #20 is still draft/open, not merged or deployed.


## Contract-copy comparison result

The vendored contract files in Hunt PR #1 and tg-content-bot PR #20 were fetched from their current PR heads and compared directly. They are identical after the first repository-specific header line (Hunt file 13,352 bytes; bot file 13,306 bytes including the differing first line). This is a verified current match, but the match is not enforced automatically by cross-repository CI. The canonical @vixor/contracts package remains a draft PR, so package-to-vendored drift remains a future risk until a synchronization/compatibility gate is added.


## New P0 repair — Telegram durable inbox before acknowledgement (2026-10-27)

Source review confirmed a data-loss path: webhook acknowledged Telegram with HTTP 200 before inserting into `telegram_updates`; if that insert failed, routing continued without a durable inbox row and Telegram would not retry the acknowledged update.

A fix was committed on tg-content-bot PR #20 branch:
- `996474275510c3ddd9d35100a84b2e20eae58008`: move ledger ingestion before HTTP acknowledgement; return 503 + Retry-After when durable insert fails; return 400 if update_id is missing; duplicate ledger delivery returns 200 without routing; only after successful insert does routing move to waitUntil.
- `b7909d53f6bbcb6202422e91c1467fbc2636e065`: update regression tests to assert inbox exists before response and database failure returns 503 without routing, then successful retry persists and processes the update.
- `02d335d22f3844dd5e5954eae52e4a6e1d22d295`: align ledger comments/logging with fail-closed semantics.

Verification state at this update: CI run 40442724388 was pending on test commit b7909d5; run 40442696334 was in progress on implementation commit 9964742. The latest documentation-only commit 02d335d must also be checked for CI status before declaring the branch green. This repair is not yet marked verified.

This is a deliberate behavior change: webhook returns 503 if Supabase cannot durably store the update. Confirm Telegram retries this webhook status as expected and verify against an isolated integration environment before production deployment. No deployment performed.


## Verification update — durable Telegram inbox repair PASSED

Latest tg-content-bot head `02d335d22f3844dd5e5954eae52e4a6e1d22d295` passed CI run 40442740265:
- bot-worker typecheck + smoke: PASS, **92 passed / 0 failed**.
- ALERT-01 regression: **20 passed / 0 failed**.
- mini-app typecheck: PASS.
- PostgreSQL migration integration (025–026): PASS.
- New regression explicitly confirms failed `telegram_updates` ingestion returns HTTP 503, does not call routing/idempotency, and a later retry persists and processes the update.
CI: https://github.com/kam65624-cmd/tg-content-bot/actions/runs/40442740265

The Telegram durable-inbox P0 is now verified at worker/smoke-test level. It remains not production-verified: no live Telegram delivery retry or real Supabase failure-injection test was performed. PR #20 remains draft/open, not merged or deployed.


## Cross-repository CI freshness check — 2026-10-27

Current branch CI evidence:
- Hunt `feat/test-opportunity-emitter`: last run 39535211707 succeeded on 2026-10-21; no newer run found in the latest 3 runs.
- Packages `feat/contracts-package`: last run 39532340500 succeeded on 2026-10-21; no newer run found in the latest 3 runs.
- Shield `feat/assess-endpoint`: latest run 40441729919 succeeded on 2026-10-27.
- Trade `fix/ops-secret-header-20261027`: latest run 40442004448 succeeded on 2026-10-27.
- tg-content-bot `audit-fixes/buffer-retry-20261027`: latest run 40442740265 succeeded on 2026-10-27.

The older green Hunt/Packages runs are not evidence that their current contract copies and the current bot/Shield changes work together. Keep the end-to-end cross-repository acceptance gate open; refresh CI on current heads and run a deterministic Hunt → Shield → bot test in isolated infrastructure before merge/deploy.
