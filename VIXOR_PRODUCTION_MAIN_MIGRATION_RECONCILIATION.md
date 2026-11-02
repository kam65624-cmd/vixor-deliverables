# VIXOR APP — Production vs Main Migration Reconciliation

Audit date: 2026-11-02
Repository: `kam65624-cmd/vixor-APP`
Production deployment commit: `10adce4fa21139673fd5e74e9fba1ebad02857f5`
Current `main`: `e746c4087823bb205cafc7988c54ae4c13ea3427`

## Code deployment gap — Confirmed
- The Vercel production deployment inspected for `vixor-app.vercel.app` is tied to commit `10adce4`.
- Current APP `main` is 94 commits ahead of that production commit and 0 commits behind it.
- Therefore, the production deployment does not contain the changes represented by current `main`.
- This is a code/deployment comparison only. It does not prove which database migrations were applied.

## Migration files added to APP main after production commit

The Git commit comparison from `10adce4` to `e746c40` identifies these four added migration files:

| Migration | Purpose | Risk / preflight |
|---|---|---|
| `20260928000000_add_paper_decisions.sql` | Creates `paper_decisions`, RLS owner policies, indexes | Verify table absence/presence, policies and indexes before any replay |
| `20260928000001_add_pending_trade_status.sql` | Replaces `trades_status_check`, adds `source`, `token_address`, `chain` | Confirm actual constraint definition and existing status values |
| `20260928000002_add_performance_indexes.sql` | Adds indexes on signal_tracking, trades, daily_signals, paper_decisions, analyses | Verify referenced columns and index definitions |
| `20261028000000_atomic_telegram_stars_fulfillment.sql` | Adds Stars pricing/bonus columns, unique payload constraint, payment RLS, atomic fulfillment RPC | Preflight duplicate payloads and pending non-UUID legacy invoice payloads; verify RPC and grants |

## Critical unknown — Production migration ledger
- No direct production database query or migration-ledger read has been performed in this audit.
- The repository migration files do not prove that a migration ran in production.
- Do not infer applied state from PR merge, Vercel deployment, application HTTP 200, or successful isolated PostgreSQL tests.
- Supabase access is available as a connection option but is not currently connected in this conversation.

## Required read-only production preflight

After the owner connects the correct Supabase project, run read-only checks first:

1. Read `supabase_migrations.schema_migrations` and record all versions after the production code baseline.
2. Inspect `paper_decisions` existence, columns, RLS enablement, policies, and indexes.
3. Inspect `trades_status_check`, all existing `trades.status` values, and the `source/token_address/chain` columns.
4. Inspect each target index definition and validity state.
5. Inspect `payments` duplicates by `payload`, pending non-UUID payloads, `stars_price`/bonus columns, current payment policies, function signatures, function owners, SECURITY DEFINER flags, search_path, and EXECUTE grants.
6. Compare actual schema to the exact migration definitions; document drift and legacy/manual DDL separately.

Do not run `supabase db push`, apply migrations, alter schema, or write production rows during this preflight.

## Release sequencing

- Do not deploy all 94 commits as one unreviewed jump.
- Establish a migration ledger/schema baseline first.
- Prepare a release manifest mapping each code change to required migration versions.
- Test that exact migration set against an isolated PostgreSQL 16 database.
- Build and preview the exact candidate commit; confirm Vercel environment bindings without exposing secret values.
- Require owner approval before production migration or deployment.

## Current proposed Gate 5 migration
- Recovery migration `20261102000000_gate5_security_and_stars_payer_binding.sql` exists only on APP Draft PR #32's branch.
- It has passed an isolated PostgreSQL 16 regression suite in CI, but it is not on `main` or production.
- It drops the legacy five-argument Stars RPC and introduces a six-argument payer-bound signature. Deploying only one side of this contract would fail closed; code and migration must be released as a coordinated, owner-approved unit.

## Status
- Production code SHA vs main SHA: **Confirmed gap (94 commits)**.
- Four post-baseline migration files: **Confirmed inventory**.
- Production migration ledger and actual applied schema: **Not verified**.
- Production release candidate and migration plan: **Not prepared**, pending database preflight.
- No production migration, deployment, secret change, or database write performed.
