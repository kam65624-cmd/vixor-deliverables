# VIXOR Core Contracts — Distribution and Adoption Audit

Audit date: 2026-11-02
Baseline: current `main` across repositories as read during this audit.
Status: Stage 2 open; no consumer integration or release is authorized by this document.

## Finding C-01 — Canonical package is not on packages/main
- `vixor-packages/main` does not contain `packages/vixor-contracts`.
- The package exists only on Draft PR #2 at `fda94303b4ee4efffa5e7b636c36bac887ff593e`.
- Its manifest declares `"private": true`, version `0.1.0`, and exposes TypeScript source paths directly.
- PR #2 reports CI success (run `40613280926`) but remains unmerged.
- Conclusion: source proposal exists; it is not yet a distributable dependency.

## Finding C-02 — Current consumers are not adopting the canonical package
- `vixor-hunt/main` depends on `@vixor/core`, `@vixor/lexicon`, and `@vixor/providers` via `workspace:*`.
- `vixor-shield/main` has the same local workspace dependencies.
- `vixor-trade/main` has the same local workspace dependencies plus `@vixor/ta`.
- These resolve to each repository's own `lib/*` packages, not `@vixor/contracts`.
- `vixor-APP/main` has no `@vixor/contracts` dependency.
- TG-BOT's contract work is still a vendored implementation on Draft PR #24; that PR is based on an older main SHA and is not merged.
- Conclusion: no current production-main consumer resolves or imports the proposed canonical package.

## Finding C-03 — Existing integration PRs are not adoption evidence
- HUNT PR #1 is Draft and does not add an `@vixor/contracts` dependency.
- SHIELD PR #2 is Draft, based on an older main SHA, and continues to use `@vixor/core`.
- TRADE PR #2 is Draft and concerns ops-secret transport, not contract adoption.
- TG-BOT PR #24 is Draft and stale relative to current main.
- PR-local parity tests or vendored file comparisons do not establish package distribution or consumer adoption.

## Distribution choices

### Option A — Public, standalone contracts package (recommended only if owner approves public source)
- Move only the dependency-free contract package to a dedicated repository/package.
- Publish versioned immutable releases to the public npm registry.
- Consumers install exact versions; CI checks supported schema version and contract conformance.
- No paid API/subscription is required for public npm distribution.
- Requires explicit owner approval to make the contract source public.

### Option B — Private GitHub Packages
- Keep source private and publish versioned package artifacts.
- Consumers need package-read access from each repository's CI/runtime build.
- Requires a supported cross-repository GitHub App/token permission strategy and owner-managed repository secrets.
- Do not introduce PATs or copy personal credentials into CI.

### Option C — Generated vendored snapshots (temporary fallback only)
- Keep one canonical source and generate consumer snapshots automatically.
- Add a CI drift check that fails when generated files differ from canonical.
- This is not equivalent to package adoption; treat it as a temporary controlled sync mechanism, not closure of the distribution gate.

## Required decision and acceptance criteria
1. Owner selects public package or private package distribution. Do not change repository visibility without explicit approval.
2. Canonical package is versioned and immutable; consumers pin exact versions.
3. HUNT, SHIELD, APP, TRADE, and TG-BOT adopt the same package or an explicitly approved generated adapter.
4. Clean install/build in every separate repository resolves the same release without workspace aliases or local path assumptions.
5. Contract compatibility tests reject unsupported versions, identity mismatch, stale/invalid risk assessment, duplicate idempotency keys, and unsafe publication state.
6. CI records exact package version and commit provenance in each consumer.
7. Only after all consumers pass may Stage 2 contract-distribution gate be marked complete.

## Safety
- No repository visibility change, package publication, dependency update, merge, or deployment performed.
- This audit is a decision artifact; it does not authorize consumer migrations.
