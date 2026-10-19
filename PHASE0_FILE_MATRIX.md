# Phase 0 — File-by-file Implementation Matrix

**As of:** 2026-10-20  
**Scope:** Read-only audit of integration-relevant files across VIXOR and tg-content-bot repositories. This is a plan, not authorization to change production. No production source, secrets, databases, live webhooks, or deployments were modified or tested in this review.

## Status key

- **KEEP** — retain as the current owner/source of truth.
- **REVIEW** — inspect more evidence before deciding.
- **MODIFY LATER** — likely needs a controlled change after Phase 0 and owner approval.
- **ADD LATER** — missing capability proposed for a later implementation PR.
- **DO NOT DELETE YET** — a file looks duplicated or misplaced, but migration/runtime/history evidence is incomplete.
- **BLOCKED** — cannot be marked complete with the available evidence.

## A. VIXOR application — `kam65624-cmd/vixor-APP`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `VIXOR_MASTER.pdf` in deliverables repo | Present, binary PDF; text not successfully extracted in this session | **BLOCKED** | P0 — master requirements cannot be reconciled yet | User should attach the PDF in chat or provide an extracted text version; record PDF SHA, page count and text checksum, then reconcile every conflict with GLM5/PODs |
| `.env` (repository root) | File path is present in the current Git tree; its contents were deliberately not read | **REVIEW immediately, securely** | P0 — potential secret exposure; presence alone does not prove a secret is inside | Authorized maintainer to inspect outside chat, check current contents and Git history, rotate any real credentials, then remove from tracking through an approved change if appropriate |
| `.gitignore` | Contains `.env*` ignore rule and allows `.env.example` | **KEEP; verify repository history** | P0 — ignore rules do not untrack an already committed file | Confirm whether `.env` is tracked across history and whether any credentials were exposed; run secret scanning in an authorized environment |
| `.env.example` | Present as a template | **KEEP** | P1 — template must never contain real secrets | Validate variable names and ensure no production values |
| `package.json` | Has build, lint, typecheck; no standalone `test` script in inspected scripts | **MODIFY LATER only if useful** | P2 — developer workflow inconsistency, not proof tests are absent | CI workflow directly invokes `pnpm vitest run`; keep that distinction in documentation and decide whether to add a convenience script later |
| `.github/workflows/ci.yml` | Defines typecheck, lint, Prettier check, Vitest, and build jobs | **KEEP; validate latest run** | P1 — latest visible CI success is 2026-09-30, not current proof | Inspect the latest run in Actions and save job conclusions/logs; run full CI on the intended candidate commit |
| `src/domains/arbitrage/**` | Expected active paths are absent from current `main` tree | **ADD/RESTORE only after trace** | P0 — documented active implementation does not match repository | Trace route tree, imports, commit history, generated route manifest, and CI before deciding whether to restore or re-port |
| `archive/domains/arbitrage/**` | Contains engine, strategies, executor, risk/config and three test files | **KEEP temporarily; DO NOT DELETE** | P0 — likely source of the archived arbitrage implementation | Compare archived files with the claimed Phase B.1 commit and active app wiring; confirm why they were archived |
| `archive/domains/arbitrage/tests/config.test.ts` | Present under archive | **REVIEW / relocate only with approved fix** | P1 — tests in archive may not prove the active app feature | Confirm Vitest includes these tests and that they run on the current commit |
| `archive/domains/arbitrage/tests/risk.test.ts` | Present under archive | **REVIEW / relocate only with approved fix** | P1 — same test-discovery uncertainty | Confirm current test discovery and coverage |
| `archive/domains/arbitrage/tests/strategies.test.ts` | Present under archive | **REVIEW / relocate only with approved fix** | P1 — same test-discovery uncertainty | Confirm current test discovery and coverage |
| `supabase/migrations/20260621000000_add_arbitrage_domain.sql` | Present; creates three tables, enables RLS, adds policies and grants | **MODIFY LATER after DB review** | P0/P1 — access-control and exposure risk | Review grants, roles, existing deployed schema and migration history in staging; never apply during Phase 0 |
| Policy `user_read_arb_stats` in that migration | `FOR SELECT USING (true)`; comment says authenticated global stats | **MODIFY LATER after intent confirmed** | P1 — policy predicate does not explicitly restrict role; exposure depends on grants and table privileges | Confirm intended visibility and effective grants in a disposable/staging DB |
| Policy `user_own_arb_opportunities` in that migration | Allows rows where `user_id IS NULL` to any role with SELECT grant | **REVIEW** | P1 — null-owner rows are globally readable to eligible roles | Confirm whether null-owner opportunities are meant to be public; restrict to intended roles if not |
| Grants in that migration | Grants SELECT/INSERT/UPDATE/DELETE to `authenticated` for opportunities/executions; RLS policies shown are SELECT-only | **REVIEW** | P1 — broad grants increase complexity; RLS may still block writes absent policies, but least privilege is unclear | Verify effective grants and service-role write paths; reduce grants only through tested migration |
| `src/shared/api-keys/admin-guard.ts` | Server-side admin allowlist helper exists | **KEEP; trace every caller** | P1 — helper existence does not prove every privileged handler uses it | Map admin guard + authentication middleware per sensitive server function |
| `src/server/config.server.ts` | Documents server-only environment access patterns | **KEEP** | P1 — avoid leaking provider/service keys to client | Verify all actual secret reads are server-only |
| Root CI / test / deploy evidence | Last visible CI success at commit `3e08e8e8d45842d5d16ce93879fe80874f737988` on 2026-09-30 | **REVIEW** | P1 — stale for current production assurance | Capture newest Actions run; verify deployment commit matches tested commit |

## B. Central command center — `kam65624-cmd/tg-content-bot`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `bot-worker/src/index.ts` | Routes webhook, links, media, AI, health; wildcard CORS; one-minute scheduled dispatcher runs multiple jobs | **KEEP; MODIFY LATER by route** | P0/P1 — route auth and scheduled-workload interactions | Build a route-by-route auth map and measure runtime, overlap, timeout and failure isolation before adding engine consumers |
| `bot-worker/src/http/auth.ts` | Validates Telegram Mini App HMAC, 24-hour age and owner allowlist | **MODIFY LATER after tests** | P1 — future `auth_date` is not explicitly rejected; helper correctness does not prove every route uses it | Add tests for future timestamps, expired payloads, bad signatures, missing owner, malformed user JSON and replay behavior |
| `bot-worker/src/http/ai-routes.ts` | Calls `verifyInitData` before dispatching AI routes | **KEEP; test object-level authorization** | P1 — route-level auth is present, but authorization for requested draft/channel IDs must also be checked | Verify each operation is restricted to owner-owned workspace/records; schema-validate request bodies |
| `bot-worker/src/telegram/webhook.ts` | Checks Telegram secret header; acknowledges quickly and processes in `waitUntil`; dedupe uses `idempotency_keys` | **MODIFY LATER after reliability design** | P0 — dedupe is explicitly fail-open when DB check fails; update is acknowledged before durable completion, so a failed background task may be lost and a DB outage can permit duplicates | Decide durable inbox/queue semantics, ack timing, retry policy and dead-letter handling; test duplicate update IDs and DB failure |
| `bot-worker/src/pipeline/publish.ts` | Checks prior published hash, sends to Telegram, then records published result | **MODIFY LATER after publish-flow consolidation** | P1 — check/send/record are separate operations; crash after send but before record can lead to duplicate retry | Prefer a single outbox state machine, reconciliation of uncertain Telegram responses, and tests for send success + DB write failure |
| `bot-worker/src/pipeline/outbox-publish.ts` | Outbox with claim/lease, retries and dead-letter behavior; caps work per cron | **KEEP; strengthen tests** | P1 — external send and DB state cannot be made one atomic transaction; concurrency/lease expiry edge cases remain | Test concurrent claims, expired leases, uncertain send outcome, retry caps and per-channel kill switch |
| `bot-worker/wrangler.toml` | Production Worker config; one-minute Cron; KV bindings; secrets are documented by name, not value | **KEEP; review config changes** | P1 — schedule adds workload and has production bindings | Confirm production/staging separation and that future integration consumers have bounded work and kill switches |
| `supabase/migrations/001_schema.sql` | Enables RLS but creates `anon_full_access` policies for all listed core tables | **P0 REVIEW / MODIFY LATER** | P0 — RLS enabled does not mean data is protected; the anon role receives full-table policy access where table grants allow it. A public anon key can be used outside the Mini App API | In staging, inventory grants and direct anon-key access; remove broad anon policies and replace with least-privilege policies/server-only operations through an approved migration |
| `supabase/migrations/020_auto_publisher.sql` | Present; sets auto-publish/radar defaults and indexes | **DO NOT RUN until migration history checked** | P1 — duplicate migration path exists | Determine applied state from Supabase migration ledger and deployment notes |
| `supabase/migrations/ADD_020_auto_publisher.sql` | Same Git blob SHA as `020_auto_publisher.sql`; contents therefore identical | **DO NOT DELETE YET** | P1 — two paths can confuse manual execution and future migration tooling | README describes SQL Editor/manual setup and setup range through 019; no repository migration runner was found in the tree query. Verify actual operator process and production ledger before choosing canonical file |
| `README.md` | Setup text says migrations 001–019 / `NEW_PROJECT_SETUP.sql`; does not document 020 clearly | **MODIFY LATER** | P1 — documented setup can omit the current publisher migration or invite inconsistent manual steps | Reconcile docs with actual production migration ledger and approved canonical setup |
| `supabase/migrations/001_schema.sql` + published/draft schema | Source-post uniqueness exists on `(tg_chat_id, tg_message_id)`; published content hash index exists | **KEEP; add integration constraints later** | P1 — current dedupe helps, but webhook fail-open and external-send boundary remain | Define canonical idempotency key for each external engine event and each destination-language publish attempt |
| Product/persona registry, event inbox, cross-engine auth and integration health | No evidence yet of a complete unified control-plane registry/contract in the inspected core files | **ADD LATER after Phase 0** | P1 — without these, integrations risk hard-coded channel routing and duplicated events | Design only after confirming existing schemas and owner decisions; avoid premature schema duplication |

## C. Specialized engines

### Hunt — `kam65624-cmd/vixor-hunt`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `src/index.ts` | Telegram webhook checks random path + secret header. `POST /engine/accel`, `/engine/filter`, `/engine/confluence` have no visible service-auth gate in the handlers; `/engine/presets` is public GET | **REVIEW; MODIFY LATER if endpoints become internal** | P1 — public stateless endpoints may be intentional, but must not be trusted as authenticated integration endpoints | Decide public-vs-internal contract; if internal, add signed service auth, rate limits, size limits and schema validation |
| `wrangler.toml` | Own D1 database, minute cron, `AUTO_PUBLISH=false` | **KEEP** | P1 — preserve independent runtime and data ownership | Confirm actual deployed config matches repo and cron budget |
| `.github/workflows/ci.yml` | Typecheck, unit tests, wording check, secret scan and bundle check are configured | **KEEP; latest run verification needed** | P1 — last visible CI run passed on 2026-10-09; current run status not exposed by the available Actions query | Obtain latest run in repository Actions and record per-job results |

### Shield — `kam65624-cmd/vixor-shield`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `src/index.ts` | Telegram webhook has secret/path check; `POST /ingest/blocklist` validates timestamped HMAC and caps body size; inserts use conflict handling | **KEEP; harden later** | P1 — timestamp window alone is not a replay store; payload item schema/JSON error handling needs testing | Test malformed JSON, malformed item types, replay of identical signed request within five minutes, key rotation and auth failures |
| `test/engine2.test.ts` | Latest retrieved test log: 147/148 passed; `punycode + shortener detected` expected factor `U03`, got no factor | **MODIFY only after reproducing** | P0 for integration readiness — risk scoring cannot be trusted as a hard publish gate while its relevant test is red | Re-run current CI; determine whether URL parser or test expectation is wrong; add regression tests for punycode and shorteners |
| `.github/workflows/ci.yml` | Typecheck, tests, wording check, secret scan and bundle check are configured | **KEEP; resolve current red run** | P0/P1 — last visible CI run failed on 2026-10-09 | Recheck current Actions run and require all required jobs green before connecting Shield to auto-publish |

### Trade — `kam65624-cmd/vixor-trade`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `src/index.ts` `GET /debug/brief` | Compares query parameter `k` with `WEBHOOK_SECRET` | **MODIFY LATER** | P1 — query secrets can appear in request logs, history and monitoring | Replace with header-based authenticated ops access and rate limiting in an approved PR |
| `src/index.ts` `POST /ingest/signals` | Timestamped HMAC (±5 minutes), body limit, batch writes and conflict handling by signal ID | **KEEP; strengthen contract** | P1 — `batch_id` is reported but not itself deduplicated; IDs upsert, so stale events may overwrite newer signal state; shape validation is shallow | Add schema validation, event ordering/version semantics, batch idempotency and replay tests |
| `wrangler.toml` | Own D1 database, minute cron, `AUTO_PUBLISH=false` | **KEEP** | P1 — maintain independent operation and explicit publish safety | Verify deployed env values without exposing secrets |
| `.github/workflows/ci.yml` | Typecheck, tests, wording policy, secret scan, bundle check are configured | **KEEP; capture latest full CI** | P1 — last visible run is scheduled batch-compute success on 2026-10-19, not full CI proof | Open latest CI workflow run in Actions; verify all jobs on current commit |

## D. Shared packages — `kam65624-cmd/vixor-packages`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| Root `package.json` | pnpm/Turbo scripts for build, typecheck and lint | **KEEP; inspect workspace** | P1 — no root test script shown | Inspect each package's scripts and workspace configuration; identify actual consumers and published versions |
| `packages/@vixor/auth`, `design-system`, `gamification`, `persona-config` (actual package directories to confirm) | Shared packages are documented in repository context, but actual use by Workers has not been proven | **REVIEW** | P1 — shared package repository does not automatically mean engines use it | Map import references, package versions, release process and compatibility before trying to centralize code |
| CI/workflow runs | No run listing was returned through the available Actions query for this private repo | **BLOCKED evidence** | P1 — absence of returned runs is not proof of no CI | Obtain latest Actions run via authenticated repository UI/maintainer and record commit + job conclusions |

## E. Deliverables and governance — `kam65624-cmd/vixor-deliverables`

| File / path | Observed state | Action | Priority / risk | Evidence still required |
|---|---|---|---|---|
| `GLM5_MASTER_PROMPT.md` | Reviewed; says Phase A and B.1 are complete and describes active arbitrage paths | **KEEP; reconcile claims** | P0 — documented completion conflicts with current active source tree | Update completion claims only after source/CI proof; keep historical plan distinguishable from verified state |
| Six `POD_*.md` files | Reviewed; provide role tasks and checklists, including tasks still unchecked | **KEEP; use as acceptance criteria** | P1 — checked items in docs are not runtime evidence | Convert only the integration-critical requirements into testable acceptance criteria |
| `INTEGRATION_AUDIT.md` | Updated with initial findings and this deep-evidence appendix | **KEEP / update after new evidence** | P1 — PDF and private Actions evidence remain open | Append only verified evidence and dates |
| `INTEGRATION_CONTRACTS.md` | Proposed event, risk, signal and publishing contracts | **KEEP as proposal** | P1 — contract is not implemented or validated | Review against actual endpoint schemas and security requirements before coding |
| `PHASE0_FILE_MATRIX.md` | This file | **KEEP; update at Phase 0 close** | P1 — documents proposed changes, not completed implementation | Add exact commit/test references and close every blocker before declaring Phase 0 done |
| `VIXOR_MASTER.pdf` | Present, extraction blocked in this session | **BLOCKED** | P0 | Attach the PDF or provide text extraction so requirements can be reconciled |

## F. CI evidence snapshot — 2026-10-20

| Repository | Latest visible workflow evidence | Interpretation |
|---|---|---|
| `vixor-APP` | CI run 36697373078, success, 2026-09-30, commit `3e08e8e8d45842d5d16ce93879fe80874f737988` | Stale relative to this review date; rerun/inspect current Actions before relying on it |
| `vixor-hunt` | CI run 37870183208, success, 2026-10-09, commit `ceeb2474d3b20cf556e45abd0e9798739a0d887f` | Passing historical run; not proof of current deployed health |
| `vixor-shield` | CI run 37870169067, failure, 2026-10-09, commit `5eefa4cf6d490d4b71c0991d8cbb318a70d54510` | Relevant test failure must be resolved/rechecked before integration |
| `vixor-trade` | Batch-compute run 39328574029, success, 2026-10-19, commit `6fab976c65bedf5b351cb65307b9d38dfdd2df96` | Scheduled compute only; not full CI |
| `vixor-packages` | No run returned by available Actions listing | **Unknown**, not a failure and not a pass |
| `tg-content-bot` | No run returned by available Actions listing | **Unknown**, not a failure and not a pass |
| `vixor-deliverables` | No run returned by available Actions listing | **Unknown**, not a failure and not a pass |

The connector's available Actions listing exposes public run results but did not return the private repositories' run lists. Combined commit-status queries returned no entries for the latest commits; an empty status list is not a green check. Private Actions evidence therefore remains a maintainer-side verification item.

## G. Phase 0 blockers and exit criteria

1. Extract and reconcile `VIXOR_MASTER.pdf` (blocked in this session; do not guess its contents).
2. Securely triage the tracked root `.env` in VIXOR without copying any value into chat or reports.
3. Reconcile GLM5's active arbitrage claim with the archive-only source tree, route generation and migration history.
4. Obtain current Actions run/job evidence for each private repository; recheck Shield's failure and current full CI for Trade.
5. Review effective Supabase grants/RLS for VIXOR arbitrage and tg-content-bot; the current tg-content-bot anon-full-access policies are a critical security blocker.
6. Define durable webhook inbox/dedupe and publish-outbox recovery behavior, including uncertain Telegram send outcomes.
7. Prove how migrations are applied and what is already applied before handling duplicate `020` files.
8. Deliver a verified implementation sequence with file-level scope, acceptance tests, rollback plan and explicit approval gates.

**No production code, production settings, secrets, database migrations, live webhooks or deployments were changed in producing this matrix.**


## H. Workflow-tree verification (additional evidence, 2026-10-20)

Recursive Git tree queries were performed for the current default branches. These are tree-level findings, not assumptions from an empty Actions API response.

| Repository | Current tree result | Audit consequence |
|---|---|---|
| `vixor-APP` | `.github/workflows/ci.yml` and `.github/workflows/block-force-push.yml` are present | CI is configured in GitHub Actions; the latest visible CI result is still 2026-09-30 |
| `vixor-hunt` | `.github/workflows/ci.yml` is present | CI is configured; latest visible run is 2026-10-09 |
| `vixor-shield` | `.github/workflows/ci.yml` is present | CI is configured; latest visible run is failing on 2026-10-09 |
| `vixor-trade` | `.github/workflows/ci.yml` is present | Full CI is configured; the most recent run we could retrieve was batch-compute, not that CI workflow |
| `tg-content-bot` | No `.github/workflows/` paths in current tree | No GitHub Actions workflow is defined in this repository tree. Verify any external Cloudflare/Vercel build pipeline and add a documented CI gate before integration changes |
| `vixor-packages` | No `.github/workflows/` paths in current tree | No GitHub Actions workflow is defined in this repository tree. Shared packages currently lack a repo-local CI gate in the inspected source |
| `vixor-deliverables` | No `.github/workflows/` paths in current tree | Documentation repo has no repo-local GitHub Actions workflow; this is not itself a production blocker |

This corrects the weaker earlier wording “no run returned” for tg-content-bot, vixor-packages and vixor-deliverables: the current default-branch trees contain no GitHub Actions workflow files. This does not rule out external provider build/deploy pipelines, which were not inspected.

## I. Revised Phase 0 risk order

1. **P0:** Securely triage the tracked VIXOR root `.env` without reading or exposing its values.
2. **P0:** Resolve tg-content-bot's broad anon-role RLS policies and webhook fail-open/early-ack reliability design before connecting engines.
3. **P0:** Extract `VIXOR_MASTER.pdf` and reconcile it with GLM5/PODs.
4. **P0/P1:** Reconcile archived-only Arbitrage source with the claimed active implementation and migration state.
5. **P1:** Obtain current private CI/deploy evidence; add repository-local CI for tg-content-bot and vixor-packages through approved changes.
6. **P1:** Resolve Shield's known red test and complete route-by-route authentication, replay and schema-validation review.
7. **P1:** Confirm migration history and the canonical `020_auto_publisher` file before any migration operation.
