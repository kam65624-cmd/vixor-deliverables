# VIXOR × tg-content-bot — Phase 0 Integration Audit

**Task ID:** VIXOR-TG-INTEGRATION-P0  
**Status:** Initial repository-level audit; read-only review of source/configuration.  
**Scope:** `vixor-APP`, `vixor-deliverables`, `vixor-packages`, `vixor-hunt`, `vixor-shield`, `vixor-trade`, `tg-content-bot`.  
**Not performed:** local install/build/test, authenticated production checks, database queries, deploys, secret access, schema changes, or feature implementation.

## Executive summary

The repositories are separate deployable systems, not one runtime or one database today. The clearest architectural boundary is:

- **VIXOR app:** TanStack Start / React 19 / TypeScript / Vite / Nitro for Vercel; Supabase is its primary data/auth layer.
- **Hunt / Shield / Trade:** independent Cloudflare Workers, each configured with its own Cloudflare D1 database and Telegram bot credentials. Their package manifests use `grammy`, `hono`, and workspace packages such as `@vixor/core`, `@vixor/lexicon`, `@vixor/providers`; Hunt and Trade also use `@vixor/ta` in the visible manifests. Their READMEs say shared libraries are vendored locally for deployment independence.
- **tg-content-bot:** Cloudflare Worker + Telegram webhook/publishing pipeline + KV namespaces + Supabase/Postgres; separate Mini App under the same repository.
- **vixor-packages:** pnpm workspace of shared packages (auth, design system, gamification, persona config). It is not yet confirmed that the three bot repositories consume this repository directly; their READMEs instead describe locally embedded shared code. Do not assume workspace package parity.

**Recommendation:** do not merge databases or make cross-repository imports the first integration step. Start with a versioned, authenticated HTTPS contract and an explicit canonical record model. Keep each app's existing database as its system of record until entity ownership, user identity, access control, retry semantics, and migration/rollback have been tested.

## Repository inventory

| Repository | Verified from files | Initial assessment |
|---|---|---|
| [vixor-APP](https://github.com/kam65624-cmd/vixor-APP) | `package.json`, `vite.config.ts`, `.env.example`, Turbo config, arbitrage migration | TanStack Start app, React 19, TS, Vite/Nitro Vercel preset, Supabase, AI/web3 dependencies. Package scripts include build, lint, typecheck. README path returned 404 on default branch, so no README claims are relied on. |
| [vixor-deliverables](https://github.com/kam65624-cmd/vixor-deliverables) | README, GLM5 prompt, six POD files, PDF filename, script/patch names | Planning material and patch artifacts. README claims Phase A/B.1 work is ready/applied, but these claims are not independent proof that the current app contains the same code. |
| [vixor-packages](https://github.com/kam65624-cmd/vixor-packages) | root package, pnpm workspace and package manifests | pnpm 9/Turbo monorepo. Packages observed: `@vixor/auth`, `@vixor/design-system`, `@vixor/gamification`, `@vixor/persona-config`. Root scripts advertise build/typecheck/lint; execution not performed. |
| [vixor-hunt](https://github.com/kam65624-cmd/vixor-hunt) | package, README, Wrangler config, src listing, migrations | Independent Cloudflare Worker; D1 binding `DB`; cron each minute; AUTO_PUBLISH defaults false. Secrets documented separately from vars. |
| [vixor-shield](https://github.com/kam65624-cmd/vixor-shield) | package, README, Wrangler config, src listing, migrations | Independent Cloudflare Worker; D1 binding `DB`; cron each minute; public assets binding; AUTO_PUBLISH defaults false. Intended for token/link/message risk scanning. |
| [vixor-trade](https://github.com/kam65624-cmd/vixor-trade) | package, Wrangler config, src listing, migrations | Independent Cloudflare Worker; D1 binding `DB`; cron each minute; AUTO_PUBLISH defaults false. Bot identity/config differs from Hunt and Shield. |
| [tg-content-bot](https://github.com/kam65624-cmd/tg-content-bot) | Worker entrypoint/package/Wrangler config, migration 001, migrations 019/020 | Cloudflare Worker with Telegram webhook, publishing/outbox/workflow/radar/reminder pipelines, KV, Supabase JS; separate Mini App. Production var APP_URL points to Pages. |

## Observed architecture and boundaries

### vixor-APP

- Package name is `tanstack_start_ts`; Node engine >=20 and pnpm 9.15.
- Vite config enables TanStack Start, Nitro Vercel preset, Node 22 runtime, server/client import protection, and security headers/CSP.
- `.env.example` declares Supabase URL/anon/service role variables plus optional market-data, AI, Telegram and wallet/exchange integrations. Treat the service role and all provider keys as server-only secrets; verify actual usages before exposing any env variable to the browser.
- The deliverables describe an arbitrage domain and a migration creating opportunity/execution/stats tables. The migration text uses `auth.users` ownership references and describes RLS. The current file path requested for the arbitrage domain source returned 404; this is a **verification gap**, not proof that the domain is absent.
- Arbitrage opportunities are described as very short-lived (3–4 seconds). They should not be treated as durable trade instructions or republished without freshness, revalidation and expiry checks.

### Hunt / Shield / Trade

- Each `wrangler.toml` defines a distinct Worker and distinct D1 database ID. Their own README states independent repository/deployment/Cloudflare-account boundaries and locally embedded shared libraries.
- Their bot package manifests use `grammy` and `hono`, plus `workspace:*` dependencies. This creates a reproducibility question: confirm the root workspace/lockfile and deployment scripts resolve these dependencies in the deployed build, especially because READMEs say shared libraries are vendored locally.
- Each worker has a minute cron and separate Telegram bot/webhook secrets. Keep these bots isolated; never reuse bot tokens or assume the same Telegram bot identity across services.
- Hunt's AUTO_PUBLISH is false and its documented budget is 30,000/day; Shield's is false and budget 50,000/day; Trade's is false and budget 20,000/day. These are config targets, not measured usage or proof of live quotas.
- Migration numbering/contents differ by service. Do not run one bot's D1 migration against another bot's database.

### tg-content-bot

- Worker entrypoint imports webhook handling, media proxy, URL shortener, buffered media-group processing, scheduled publishing, publish outbox, workflow engine, AI routes, affiliate click tracking, ATH monitoring, auto-publisher/radar, daily recap, channel provisioning, reminders and command registration.
- Wrangler config sets production `ENVIRONMENT`, `APP_URL=https://tg-content-app.pages.dev`, two KV bindings and a per-minute cron. Secrets are documented for Telegram, Supabase and AI providers.
- Migration 001 creates the base channel/content pipeline, including `app_settings`, `niches`, `channels`, `content_types`, `source_posts`, and `classifications`. It uses UUID IDs, JSONB media/entities and source-post uniqueness by Telegram chat/message.
- Migration 019 introduces affiliate/airdrop/channel-template concepts and inserts seed affiliate records with obvious placeholder values such as `YOUR_AXIOM_REF`. Those placeholders must not be treated as real referral links.
- `020_auto_publisher.sql` and `ADD_020_auto_publisher.sql` were fetched in full and are **byte-for-byte identical** (3,295 characters, 71 lines). This is confirmed duplicate migration content, not merely a similar opening. Determine which file the migration runner actually discovers and retain one canonical path in a reviewed cleanup PR; do not run both blindly.
- CORS in the Worker entrypoint visibly allows `*` and includes `X-Telegram-Init-Data`. This is not by itself proof of exploitable access, but each affected endpoint must independently validate Telegram init data, authorization and request origin; CORS is not an auth boundary. The cron also runs scheduled publishing/outbox, workflow recovery, radar discovery and auto-publisher paths each minute; their safety gates and per-channel kill switches need code-path review before any cross-service event is connected.

### vixor-packages

- Root uses pnpm workspace packages under `packages/*`, Turbo and TypeScript.
- The auth package includes Supabase, Solana and JWT-related dependencies; design system and gamification have their own smaller dependency sets.
- No evidence yet proves that VIXOR app, Hunt, Shield, Trade and tg-content-bot share the same runtime package versions or authentication semantics. Do not introduce a shared package dependency until import maps, package exports, build packaging and deployment compatibility are validated.

## Proposed integration topology (not implemented)

1. **Discovery source:** Hunt emits a validated discovery event with stable event ID, chain, token/mint address, source timestamp, source URL and evidence/metrics.
2. **Risk enrichment:** Shield returns a risk assessment for that exact chain/address, including score, severity, reason codes, provider timestamps and expiry. Missing/timeout responses are explicitly `unknown`, never silently low-risk.
3. **Canonical signal record:** VIXOR app owns the user-facing signal history/entitlements if the app is the selected product source of truth; otherwise choose one owner before implementation. Do not make the bot's editorial post the canonical market signal.
4. **Publisher:** tg-content-bot consumes only approved, unexpired signal records and renders channel-specific copy. Publish through its existing outbox/idempotency mechanism; store the external Telegram message ID for reconciliation.
5. **Feedback and attribution:** record post ID, signal ID, channel ID, Telegram message ID, click/referral IDs and timestamps without leaking private user identifiers across public payloads.
6. **User identity:** link Telegram identity to a VIXOR account only after server-side verification of Telegram Mini App init data and a separate explicit account-link confirmation. Never trust a client-supplied Telegram ID alone.
7. **Arbitrage:** keep trade execution isolated from publishing. The bot/app may display a read-only opportunity card only after freshness/risk checks; never trigger live execution from a content-posting event.

## Key risks and controls

| Risk | Why it matters | Required control before integration |
|---|---|---|
| Separate D1 and Supabase stores | No shared transaction or automatic consistency | Explicit owner per entity, APIs, retry/outbox and reconciliation jobs |
| Cross-account Worker isolation | Internal service URLs and credentials differ | Per-service least-privilege credentials, request signing, replay protection, rate limits |
| Telegram identity spoofing | User ID can be forged if accepted from browser input | Verify init data server-side; short-lived, audience-bound link token; explicit confirmation |
| Duplicate posts/events | Cron retries and webhooks are at-least-once in practice | Stable event IDs, DB uniqueness, idempotent consumer/outbox |
| Stale market data | Signals/arbitrage are time-sensitive | Server-side TTL, timestamp checks and fail-closed behavior for stale risk data |
| Placeholder affiliate codes | Bad attribution and misleading links | Replace only with owner-verified codes; otherwise disable affiliate button |
| Migration ambiguity | Duplicate migration filenames may be run inconsistently | Compare full contents and migration history; one canonical migration path |
| Wildcard CORS | Could widen browser access if endpoint auth is weak | Endpoint-by-endpoint auth review; origin allowlist where appropriate |
| Secret leakage | Several services have high-privilege API keys | Secret manager only, scoped keys, rotation and secret scanning |
| Trading side effects | Publishing should never initiate financial actions | Separate service permissions; dry-run default; explicit approval for live trading |
| Claims vs actual state | Deliverables describe features as done | Verify source paths, CI runs and deployed commit before relying on claims |

## CI evidence snapshot (latest runs returned by GitHub API)

This is historical CI evidence from repository workflows, not a fresh test run in this audit:

| Repository | Latest returned run | Result | Interpretation |
|---|---|---|---|
| vixor-APP | CI on main, 2026-09-30, commit `3e08e8e8d45842d5d16ce93879fe80874f737988` | Success | Green at that commit, but not recent enough to certify current state. [Run](https://github.com/kam65624-cmd/vixor-APP/actions/runs/36697373078) |
| vixor-hunt | CI on main, 2026-10-09, commit `ceeb2474d3b20cf556e45abd0e9798739a0d887f` | Success | Green at that commit only. [Run](https://github.com/kam65624-cmd/vixor-hunt/actions/runs/37870183208) |
| vixor-shield | CI on main, 2026-10-09, commit `5eefa4cf6d490d4b71c0991d8cbb318a70d54510` | **Failure** | Bundle and typecheck passed; test suite failed 1 test: `test/engine2.test.ts` → “punycode + shortener detected”, expected factor `U03`, received empty list. 147 passed / 1 failed. [Run](https://github.com/kam65624-cmd/vixor-shield/actions/runs/37870169067) |
| vixor-trade | Batch compute workflow, 2026-10-19, commit `6fab976c65bedf5b351cb65307b9d38dfdd2df96` | Success | The returned latest runs were batch-compute jobs; this does **not** establish that the full test/typecheck/build CI is green. [Run](https://github.com/kam65624-cmd/vixor-trade/actions/runs/39328574029) |
| tg-content-bot | No workflow runs returned in the queried Actions endpoint | Unknown | Inspect workflow files and repository Actions configuration; do not infer that tests passed or that workflows do not exist. |
| vixor-packages | No workflow runs returned in the queried Actions endpoint | Unknown | Root package advertises build/typecheck/lint scripts, but they were not executed here. |
| vixor-deliverables | No workflow runs returned in the queried Actions endpoint | Unknown | Documentation-only repository; no test result inferred. |

The Shield failure is a concrete blocker for relying on its risk engine in a rollout. Reproduce/fix it in a separate Shield PR and get green CI before integrating risk scores; do not mix that repair into this documentation PR.

## Phase 0 blockers / evidence gaps

- **No runtime verification:** no package installation, typecheck, build, tests, browser testing, webhook request, D1 query, Supabase query or deployment check was run in this audit.
- **PDF extraction pending:** `VIXOR_MASTER.pdf` exists in deliverables, but the GitHub file tool returned encoded binary rather than extracted text. The architecture PDF must be extracted/read before implementation decisions.
- **Current deployed commits unknown:** repository contents do not prove which commit is running in Vercel/Cloudflare/Pages.
- **Database state unknown:** migrations do not prove they have been applied to live or staging databases.
- **Endpoint contracts only partly mapped:** Hunt exposes public POST calculation routes under `/engine/*`; Shield exposes `POST /ingest/blocklist` with timestamped HMAC; Trade exposes `POST /ingest/signals` with timestamped HMAC. No end-to-end authenticated request was executed. The ingest handlers use a five-minute timestamp window but no visible one-time nonce; database conflict handling helps idempotency for some records, but explicit replay/idempotency contract tests are still required. Trade also exposes `GET /debug/brief` guarded by the webhook secret in a query parameter; assess replacing query-string secret auth with a signed request/header because URLs can be captured in logs/history.
- **App source path gap:** the requested arbitrage index path returned 404; confirm current tree paths and branch before assessing the feature's existence.
- **No secret values were read or used.** This audit relies on variable names/configuration only.

## Recommended phased plan

### P0 — Complete evidence collection (read-only)
- Extract/read `VIXOR_MASTER.pdf`; compare it with GLM5 prompt and all six PODs.
- Capture default branches, latest commits, CI statuses and actual changed-file lists for each repo.
- Trace source-to-database writes and all public HTTP routes in Hunt, Shield, Trade and tg-content-bot.
- Inspect RLS policies, auth checks, migration history and full duplicate migration content.
- Record deployed commit IDs from owner-accessible dashboards only when authorized; do not change deployments.

### P1 — Contract design and security review
- Approve canonical event schema and entity ownership.
- Define service auth, signing, timestamps, idempotency, retry, TTL and error semantics.
- Build contract tests and a staging-only integration test plan; no production writes.

### P2 — Read-only vertical slice
- Hunt discovery → Shield risk enrichment → VIXOR read-only signal → tg-content-bot draft queue.
- Keep auto-publish off; no wallet or trade-execution permissions.
- Verify deduplication, expiry, risk-unavailable state and audit logging.

### P3 — Owner-approved publishing pilot
- Enable a single staging/test channel first.
- Require explicit owner approval before enabling any production auto-publish.
- Monitor duplicate rate, stale-signal rejection, risk service availability, Telegram delivery and rollback.

### P4 — Identity, attribution and broader rollout
- Implement verified Telegram-to-VIXOR account linking only after P1/P2 pass.
- Enable channel-by-channel rollout with kill switches and documented rollback.
- Consider shared package extraction only after dependency/build parity is proven.

## Rollback principle

Every integration must be independently disableable by config/feature flag. On error: stop consuming new events, leave queued records intact, disable publisher, retain audit history, and revert the integration PR. Do not delete source records or run destructive migrations as a rollback strategy.


---

## Phase 0 Evidence Update — 2026-10-20

This appendix records additional read-only repository checks performed after the initial audit. It does not supersede the need for local builds, full test runs, staging validation, or PDF review.

### Evidence reviewed

- Read `GLM5_MASTER_PROMPT.md` and all six POD files: AI/ML, Backend, DevOps, Frontend, Lead Developer, and QA/Security.
- Confirmed the six PODs describe the VIXOR implementation workflow and quality gates, but they are planning documents; checked boxes and stated completion in these documents are not independent proof that the code or deployed system satisfies them.
- Inspected current `vixor-APP` repository tree at main commit `3e08e8e8d45842d5d16ce93879fe80874f737988`.
- Inspected current `tg-content-bot` repository tree at main commit `925b4e40a6ad242446d7234e5e0b491c6ede9c20`, plus its Worker entry point and Telegram Mini App auth helper.
- Inspected the arbitrage migration `supabase/migrations/20260621000000_add_arbitrage_domain.sql` and the current VIXOR package scripts.
- Rechecked the existing documentation PR separately; it remains an open draft and has not been merged.

### Material findings and discrepancies

#### P0 — VIXOR arbitrage implementation does not match the master prompt's claimed active path

The master prompt states that Phase B.1 is complete and describes active files under `src/domains/arbitrage/` and an authenticated arbitrage route. The current `vixor-APP` main tree contains the arbitrage engine under `archive/domains/arbitrage/`; direct requests for `src/domains/arbitrage/index.ts`, `src/domains/arbitrage/engine.ts`, `src/domains/arbitrage/strategies/cross-dex.ts`, and `src/routes/_authenticated/arbitrage.tsx` returned 404. The arbitrage SQL migration is present under `supabase/migrations/`. Therefore, the repository proves that the migration and archived source exist, but does **not** prove the claimed active route/domain is deployed or wired. Treat Phase B.1 as **not verified / likely incomplete in the active source tree** until route tree, imports, migration application history, and a passing CI/test run establish otherwise. Do not delete archived files or re-port code during Phase 0.

#### P0 — Tracked `.env` path in VIXOR repository

The Git tree lists a root `.env` file in `vixor-APP` (blob SHA `769ebf2805af57a8e66acf4a1d25a4e2a6be556d`). Its contents were intentionally not read. This is a secret-hygiene incident candidate, not proof that the file contains a live credential. An authorized maintainer should inspect it in a secure environment, check history and ignore rules, and rotate any real credentials if present. Never copy values into reports or chat.

#### P1 — Package and test gate mismatch

The current `vixor-APP/package.json` advertises `build`, `lint`, and `typecheck`, but the inspected scripts block does not advertise a `test` script even though GLM5/POD quality gates require Vitest and CI tests. Test tooling/files exist in the tree, so this is a **workflow/script evidence gap**, not proof that no tests can run. Verify the actual CI workflow commands and package-manager invocation before treating the test gate as enforced. The latest inspected commit has no combined commit-status entries returned by the status endpoint; that response is not equivalent to a green CI run. Re-run or inspect workflow runs before making a current health claim.

#### P1 — Migration policy review required

The arbitrage migration enables RLS on all three arbitrage tables and creates SELECT policies. In particular, `user_read_arb_stats` uses `USING (true)`; the comment says stats are globally readable by authenticated users, but the policy predicate itself does not express that role restriction. Confirm table grants, role behavior, and intended public/authenticated visibility in a disposable/staging database before approving this migration. Also confirm that writes are restricted to the intended service role and that nullable `user_id` rows cannot disclose sensitive opportunity data. No database was queried and no migration was applied.

#### P1 — tg-content-bot's current tree and runtime shape

- The Worker has a one-minute Cron Trigger and invokes multiple jobs in sequence, including scheduled publishing, outbox publishing, workflow processing, ATH monitoring, radar discovery, auto-publisher, reminders, and notification dispatch. Before adding new engine consumers, map execution duration, idempotency, concurrency, and per-job failure isolation to avoid compounding the current scheduled workload.
- The Worker entry point sets `Access-Control-Allow-Origin: *`. CORS is not authentication; verify every route's auth/authorization individually. The Mini App auth helper verifies Telegram initData signature, freshness (24-hour limit), and owner allowlist, but this helper alone does not prove every AI/admin/publishing route calls it correctly.
- The current tree has both `supabase/migrations/020_auto_publisher.sql` and `supabase/migrations/ADD_020_auto_publisher.sql`. Their contents were not both re-fetched and compared in this update. The duplicate-path concern remains open; identify the migration runner's discovery rules and applied migration ledger before any cleanup or migration action.

#### P1 — Hunt / Shield / Trade integration gates

- Hunt's inspected `src/index.ts` includes deterministic `POST /engine/accel`, `/engine/filter`, and `/engine/confluence` endpoints without a visible service-auth gate in those handlers. Treat them as untrusted until route-level protection, request limits, schema validation, and abuse controls are verified. This is an integration-readiness finding, not an assertion that every route in the service is unprotected.
- Shield's current test file still contains the punycode test asserting factor `U03`. The previously recorded CI failure for this test must be rechecked against the latest workflow run and source revision. Until it passes for the current commit, Shield must not be treated as a mandatory trusted risk gate for auto-publishing.
- Trade's inspected `GET /debug/brief` compares a secret supplied as query parameter `k` to `WEBHOOK_SECRET`. This can leak through URL logs/history; replace with header-based authenticated ops access in a future approved change, not during this read-only audit.
- Trade's `POST /ingest/signals` uses timestamped HMAC according to the handler comments. End-to-end signature verification, timestamp skew, replay handling, request size limits, and idempotency remain to be proven with tests.

#### P1 — Binary master PDF remains a blocker

The GitHub file API returned the PDF as base64 content, while the standard text fetch endpoint rejects it because it is not UTF-8. This session has **not extracted or reviewed the actual PDF text**. Do not treat the PDF review requirement as complete. Use an authorized local download and PDF text extraction, then record the PDF SHA, page count, extracted text checksum, and any requirements that conflict with GLM5/PODs. Do not guess its contents.

### POD / master-prompt alignment summary

- **Lead Developer:** demands architecture review, CI quality gates, risk register, and approval before merges. This supports the audit-first sequence.
- **Backend:** requires Zod input validation, auth gates, RLS, webhook HMAC, rate limiting/circuit breakers, staging-tested migrations.
- **DevOps:** calls for separate staging resources, CI gates, backups, monitoring, runbooks, and rollback.
- **QA/Security:** requires unit/E2E/security/secret scans, OWASP review, and Web3-specific checks.
- **Frontend:** includes broad Web3 Terminal UI work and browser/responsive/accessibility tests; no evidence in this Phase 0 update establishes all listed UI tasks as complete.
- **AI/ML:** includes four agents, prompt versioning, feedback loops, and no PII sent to external LLMs; no evidence here establishes these as production-complete.
- **GLM5:** declares Phase A and B.1 complete, but the active-tree mismatch above means those declarations must be reconciled against commit history, route wiring, and CI rather than accepted as proof.

### Updated evidence register

| Item | Status | Evidence / next check |
|---|---|---|
| GLM5 master prompt | Read | Claims compared to active repository tree; contradictions recorded above |
| Six POD files | Read | Requirements summarized; completion claims still require implementation evidence |
| VIXOR_MASTER.pdf | **Blocked / not reviewed** | Obtain PDF text extraction through authorized local workflow |
| VIXOR active arbitrage domain/route | **Not verified** | Source paths absent under active `src/`; engine appears under `archive/`; trace route tree and CI |
| VIXOR arbitrage migration | Present, not applied here | Review grants/RLS and migration history in staging |
| VIXOR root `.env` path | **P0 hygiene check** | Do not read in chat; authorized secure review + rotate real credentials if present |
| VIXOR tests/CI current status | **Unverified** | Inspect latest workflow run; combined status returned no entries |
| tg-content-bot Cron workload | Verified in source | Measure execution budget/concurrency before adding consumers |
| tg-content-bot route auth coverage | Partial | Trace every route to auth helper and authorization policy |
| Duplicate publisher migration names | Both paths present | Compare bytes and migration discovery/applied-history before any cleanup |
| Hunt engine route auth | Needs review | Protect/limit endpoints before trusted integration |
| Shield punycode CI issue | Needs current recheck | Do not rely on Shield gate until current CI passes |
| Trade query-secret ops endpoint | Risk confirmed in source | Future approved hardening; no changes made |
| Production deployment / live integration | Not tested | No production changes, database access, live requests, or deployment performed |

### Phase 0 exit criteria

Phase 0 is **not complete** until: (1) PDF is extracted and reconciled, (2) latest CI results are captured for all relevant repositories, (3) active-vs-archived arbitrage status is resolved, (4) root `.env` is securely triaged, (5) route-by-route auth and RLS/grants are mapped, (6) duplicate migration handling is proven, and (7) a read-only file-by-file implementation matrix is delivered. No production code, production settings, live webhooks, or database migrations were changed as part of this update.
