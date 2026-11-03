# APP Release Manifest — 2026-11-03

**Status:** PARTIAL — code/deployment inventory verified; live database state is **NOT VERIFIED**.

## Release identity

| Field | Value |
|---|---|
| Repository | `kam65624-cmd/vixor-APP` |
| Branch / commit | `main` / `77b4613df0c3dd24de8bc1a5a48ba8d760bc7864` |
| Vercel project | `vixor-app` |
| Production deployment | `dpl_9VP8j9DuPiHYABBcjk2yigEHjyVX` |
| Deployment state | **READY** |
| Deployment URL | https://vixor-h9idqc3w4-goldarenax-7278s-projects.vercel.app |
| Runtime errors (last hour) | 0 found |
| Request path counts (last 50m) | `/`: 8 |
| Full route smoke after this deployment | **NOT VERIFIED** |
| Production Redis | **NOT VERIFIED** (separate Preview verification only) |
| Production aliases | `vixor-app-goldarenax-7278s-projects.vercel.app`, `vixor-app-git-main-goldarenax-7278s-projects.vercel.app` |

## Supabase target and access

The APP repository links to project ref **`lrbgxrfvjxaixtzkutxn`**, recorded in:

- `supabase/.temp/project-ref` — Git blob `fa7e745d966ef853c610b7aa9410da2ffe01f5c6`
- `supabase/.temp/linked-project.json` — Git blob `88c2aa9d0c478b5ad36092dfd04e2246af6a1b9e`

The currently connected Supabase account does not list this project. Direct project inspection and migration listing returned **permission denied**. The other visible project named `vixor` has a different ref and is not valid evidence for APP.

Therefore:

- Applied migration versions: **NOT VERIFIED**
- Production schema / constraints / indexes: **NOT VERIFIED**
- RLS policies / RPC ACLs / role grants: **NOT VERIFIED**
- No production SQL, migration, or database write was performed.

## Main migration inventory

At APP `main@77b4613`, the repository contains **40 migration files**. The table below records the Git blob SHA-1 for each file at this exact commit. These are source identities, **not proof that the migration was applied**.

| Migration file | Git blob SHA-1 |
|---|---|
| `supabase/migrations/004_watchlists.sql` | `9ae6d755d72a3d5f202846c29fa31d31b7204990` |
| `supabase/migrations/20260607190000_phase1_add_analysis_context.sql` | `df70888f3c92e439156f52e03c57497d5a3173f9` |
| `supabase/migrations/20260609120000_add_signal_badge_vixor_message.sql` | `5f8c2007a5cbf2137e0a216039f879c9dbefc300` |
| `supabase/migrations/20260609140000_add_price_alerts.sql` | `4dfa39536297404f43350d53879cac0c73983f5a` |
| `supabase/migrations/20260609140001_add_daily_signals.sql` | `b31a34ce7220693e31f41b733d293a4691b7d751` |
| `supabase/migrations/20260610000000_add_trading_notes.sql` | `9477e4ff38e587007de11480facbb721245e83d1` |
| `supabase/migrations/20260610010000_add_trades.sql` | `918121b254294522b8f85c95382d6f0a524eb86e` |
| `supabase/migrations/20260610020000_add_copilot_chats.sql` | `e81a0e6a023241ee7c8c6b96f824ecad1c7b66c5` |
| `supabase/migrations/20260610030000_add_daily_loop.sql` | `03383ac231f0cefcb191d9d4b58f678234c86524` |
| `supabase/migrations/20260611000000_enable_rls_daily_signals.sql` | `21717a5f381bf0323486bbad288be05ac51fa061` |
| `supabase/migrations/20260612000000_add_domain_events.sql` | `365331e2ca0c356aba8d41591dccbfe922f2a9ad` |
| `supabase/migrations/20260612010000_add_user_memories.sql` | `118f15166b7032ca804f47bb35b86e0d939e5908` |
| `supabase/migrations/20260618000000_add_quantdinger_reuse.sql` | `207b750e3f13f87264f56b360c3f096bedcb5308` |
| `supabase/migrations/20260618000001_add_experiments.sql` | `9489d1298f15681cd59a721fd844cac5a9dc1f98` |
| `supabase/migrations/20260620000000_add_payments_table.sql` | `52cb58805fb20de0615f61d5b6826bd44f53eb86` |
| `supabase/migrations/20260621000000_add_arbitrage_domain.sql` | `84c61634a3fbc80c1d611e0cf75301a3189dc50e` |
| `supabase/migrations/20260622000000_add_wallet_domain.sql` | `b72d6e9f0b4219ed5012a49a874d3d6ff9cf3ac8` |
| `supabase/migrations/20260623000000_add_discovery_domain.sql` | `2d2358470403a146d1e0586f80169176c0d2670a` |
| `supabase/migrations/20260624000000_add_vixor_decisions.sql` | `b2f27acd4e06555b0526b8915100a6763467240c` |
| `supabase/migrations/20260624010000_add_data_layer_tables.sql` | `b4710cb995a59b0980522228abc21b6bcdb1f2e2` |
| `supabase/migrations/20260629000000_add_signal_tracking.sql` | `b00288303b961a70c38d5f3b55e1d4497069979f` |
| `supabase/migrations/20260701000000_add_exchange_credentials.sql` | `0a1783f5e981e586bdd582ea8550d70d65072d45` |
| `supabase/migrations/20260708000000_add_moxi_personas.sql` | `ef51c345adf49d29c9be66e4755ded4fc76826da` |
| `supabase/migrations/20260715000000_add_broker_connections.sql` | `1697442b864f1bee9e25c9ed3f0f8def7d0961a1` |
| `supabase/migrations/20260803000000_add_missing_core_tables.sql` | `ee38c758a774ddd202669474cab2a17a7cfe61fa` |
| `supabase/migrations/20260803000001_add_commerce_tables.sql` | `f61cf26e45e8da0b63dc21d46ab1905dfdee7e1e` |
| `supabase/migrations/20260804000000_rename_copilot_to_moxi.sql` | `dca870d520f3368352e742c78b0a04d603e83dea` |
| `supabase/migrations/20260809000000_add_invalidated_to_signal_status.sql` | `14baaa997fe7a809607b0c72e8df302d3ff23ab5` |
| `supabase/migrations/20260811000000_add_signal_transitions.sql` | `b8ded911f1077a44963ea451a8b496fa3388c4db` |
| `supabase/migrations/20260811000001_execute_signal_transition_rpc.sql` | `419d0a867500e127d7eaa896c70e7e91ff63d049` |
| `supabase/migrations/20260824000000_enforce_hit_tp_status_invariant.sql` | `be567e21eb040a47f479fbc4216b49bf628e5868` |
| `supabase/migrations/20260829000000_add_shield_tables.sql` | `a6442bab3d6f500f5be80b28dd6389dda208758e` |
| `supabase/migrations/20260829000001_add_gamification_tables.sql` | `c8cd99aa6fa1097df3875f39641f4852b7b86d9c` |
| `supabase/migrations/20260829000002_extend_profiles_gamification.sql` | `03b13909998794140c56af352167247d9c09b736` |
| `supabase/migrations/20260901000000_add_integration_tables.sql` | `ac634dc808f557b9f3d7183a9c390041d5391383` |
| `supabase/migrations/20260901000001_add_scan_alerts_trades_tables.sql` | `4b13848b69d2e20063e8acdbce3a93c2ce2991d2` |
| `supabase/migrations/20260928000000_add_paper_decisions.sql` | `9b2ce01bf16d170f16ed57f5239b32d5b6a3e790` |
| `supabase/migrations/20260928000001_add_pending_trade_status.sql` | `dac76458b0e7a8edd7b53ec966f2225dce9f77d8` |
| `supabase/migrations/20260928000002_add_performance_indexes.sql` | `a57910c9a23ff44f45b7dbbf1ec4d121c5753f12` |
| `supabase/migrations/20261028000000_atomic_telegram_stars_fulfillment.sql` | `dc158332dc04f366f50335fa7739a8424b4f885a` |

Latest migration on main: `20261028000000_atomic_telegram_stars_fulfillment.sql`.

## Proposed Gate 5 migration — not part of main

APP Draft PR #32 contains:

- `supabase/migrations/20261102000000_gate5_security_and_stars_payer_binding.sql`
- Git blob SHA-1: `dfa1a3c0c0403ba5db9bbfd4840e6b9fbd8eecd1`
- Branch head: `cabe8048c44bbece1a718b59d8db400ed830054e`
- PR base: `e746c4087823bb205cafc7988c54ae4c13ea3427`
- 37 commits ahead / 68 commits behind current main in the current comparison.
- Isolated PostgreSQL integration CI: **PASS**.
- Full clean bootstrap of every migration: **NOT VERIFIED**.
- Production application: **NOT APPLIED**.

The migration coordinates payer identity, points-balance privileges, profile Telegram identity protection, and the service-role-only transition / Stars fulfillment RPCs. Because its branch is substantially behind current main, it must be rebased and reviewed before integration. The code and six-argument RPC migration must ship as one coordinated unit.

## Release gates

1. Obtain read-only access to the exact APP Supabase project ref.
2. Read the real migration ledger; inspect tables, columns, constraints, indexes, RLS, RPC definitions, owners, search paths and grants.
3. Reconcile all 40 main migration files against actual applied versions.
4. Rebase and re-review PR #32 against current main.
5. Run a complete clean bootstrap against isolated PostgreSQL before any production DDL decision.
6. Obtain owner approval before production migration.
7. Run route-specific Production smoke tests and verify Production Redis separately.

**Safety:** This manifest does not authorize or record any production migration. No production database changes were made.
