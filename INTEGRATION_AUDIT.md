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
