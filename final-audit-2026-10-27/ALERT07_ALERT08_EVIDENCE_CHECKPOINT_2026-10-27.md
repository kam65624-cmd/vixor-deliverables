# ALERT-07 / ALERT-08 — Evidence checkpoint (2026-10-27)

Scope: read-only audit only. No production code, database, migration, secret values, deployment, or merge action was performed.

## ALERT-07 — Cloudflare deployment/runtime

Status: BLOCKED_OWNER_ACTION — production deployment not independently verified.

### Evidence observed in repository at `tg-content-bot` commit `2d8933ed7cd92d23144099642497f32794340715`

- `bot-worker/wrangler.toml` declares Worker name `tg-content-bot`, entrypoint `src/index.ts`, and cron `* * * * *` (every minute).
- The same file comments the expected secret names: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `ANTHROPIC_API_KEY`, optional `NVIDIA_API_KEY`, optional `CUSTOM_AI_API_KEY`, and `OWNER_IDS`. These are names only, not proof that secrets exist in the live Worker.
- `.github/workflows/ci.yml` is the only workflow present in the repository's `.github/workflows` directory at this commit. It runs typecheck/tests; it does not establish that Cloudflare deployed a given SHA.
- Therefore, repository configuration is evidence of intended settings only. It cannot prove the live Worker version, active cron trigger, deployed bindings, secret presence, or the cause of the earlier outage.

### Owner evidence required

From Cloudflare Dashboard, Worker `tg-content-bot`, provide screenshots or copied metadata (redact all secret values):
1. Overview / Deployments: active production deployment, timestamp, version/commit if shown, and status.
2. Triggers: active cron schedule(s).
3. Settings / Variables and Secrets: variable/secret **names and whether configured only**; do not reveal values.
4. Relevant deployment/build event around the reported outage/recovery, including the prior failed build if visible.

Do not change settings or deploy as part of this evidence collection.

## ALERT-08 — Production schema preflight

Status: BLOCKED_OWNER_ACTION — no authorized read-only connection to the production Supabase database is available in this audit environment.

### Repository evidence

- At the audited commit, `supabase/migrations/017_meme_signals.sql` defines `public.meme_signals.updated_at`.
- That migration's `meme_signals` table definition does not declare `targets`, `max_multiple`, or `exit_reason`. This is repository-level evidence only; it does not establish the actual production schema or rule out out-of-band changes.
- The prepared read-only preflight query is recorded in `evidence/ALERT08_PREFLIGHT_READY_QUERY_2026-10-27.md`.

### Exact query to run in the SQL Editor for the production Supabase project

```sql
select column_name, data_type, column_default, is_nullable
  from information_schema.columns
 where table_schema = 'public'
   and table_name   = 'meme_signals'
   and column_name in ('targets','max_multiple','exit_reason','updated_at')
 order by column_name;
```

Return only the result rows. These are schema metadata, not credentials. If the query returns zero rows, first confirm the selected project is the intended production project and that `public.meme_signals` exists; do not infer that the table is missing until the target is confirmed.

No migrations or writes are authorized by this checkpoint. Regardless of result, ALERT-08 remains open until the output is recorded and reviewed. Any future migration requires a separate explicit owner approval and the existing rollout gates.

## Overall

Both alerts remain open. Repository configuration and CI evidence are not substitutes for Cloudflare production dashboard evidence or a query executed against the actual production database.
