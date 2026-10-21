# VIXOR Integration Contracts — Draft 0.1

**Status:** Proposal for review; not yet an approved runtime contract.  
**Purpose:** Agree on the smallest safe interface between Hunt, Shield, VIXOR Core/APP, Trade where applicable, and tg-content-bot without merging repositories.

## Guardrails

- This document does not claim that the integrations already exist or work.
- Keep each engine in its current repository and deployment boundary.
- No live trading, custody, or movement of user funds in this integration path.
- Human approval is required before publishing signals during the initial proof.
- Missing, stale, malformed, or unverifiable data must fail closed for publication.
- Never put secrets, private keys, access tokens, or credentials in payloads or logs.
- Clicks are not conversions; conversions are not confirmed commissions. Track each separately.
- Every side-effecting operation must be idempotent and leave an auditable outcome.

## 1. Common envelope

Each service-to-service message should carry these fields:

| Field | Meaning |
| --- | --- |
| `schema_version` | Contract version, initially `0.1` |
| `event_id` | Globally unique identifier for this event |
| `event_type` | Stable event name, such as `opportunity.detected` |
| `occurred_at` | UTC timestamp when the source event occurred |
| `produced_by` | Owning service: `hunt`, `shield`, `core`, `trade`, or `tg-content-bot` |
| `correlation_id` | Identifier shared across the full processing journey |
| `idempotency_key` | Stable key used to prevent duplicate side effects |
| `payload` | Event-specific data, validated against its schema |

Consumers must reject unsupported schema versions and record a safe, redacted error. Retries must reuse the same event and idempotency identifiers.

## 2. Hunt → Core: opportunity detected

Minimum payload:

- `opportunity_id`: stable unique identifier
- `asset_id`: canonical asset identity, preferably chain/network + contract or provider ID
- `symbol`: display symbol only; never use as the sole identity
- `source`: source/provider name and source record reference
- `observed_at`: timestamp of the underlying observation
- `market_data`: values plus units, currency, and timestamps where available
- `evidence_refs`: references to source evidence; do not embed credentials
- `quality_flags`: missing fields, staleness, or source conflicts

Hunt owns discovery and source provenance. It does not mark an opportunity as safe or publish-ready.

## 3. Core → Shield: risk assessment request

Minimum payload:

- `assessment_id`
- `opportunity_id`
- `asset_id`
- `requested_at`
- `market_data` and its freshness timestamps
- `evidence_refs`
- `policy_version`

Shield response must include:

- `assessment_id` and `opportunity_id`
- `decision`: `allow`, `reject`, or `review`
- `reason_codes`: machine-readable reasons
- `checked_at`
- `policy_version`
- `data_quality`: `valid`, `stale`, `incomplete`, or `conflicting`
- `expires_at`: when the assessment must no longer be relied upon

A missing response, unknown decision, expired assessment, or non-valid data quality must block publication. `allow` means only that the configured risk checks passed; it is not a promise of profit or a guarantee of safety.

## 4. Core → tg-content-bot: publication candidate

Minimum payload:

- `publication_id`
- `opportunity_id`
- `assessment_id`
- `channel_id`: approved internal identifier, not an arbitrary destination supplied by an event
- `template_id` and `template_version`
- `content`: rendered text/media references
- `buttons`: allow-listed action types and validated destinations
- `approval_state`: initially `pending_human`
- `expires_at`
- `idempotency_key`

Publication rules:

1. Verify the actor is authorized to approve.
2. Re-check that the assessment is valid and unexpired.
3. Store the approval decision and actor/time.
4. Use a durable unique key for the external Telegram send operation.
5. Record the Telegram message identifier and final status.
6. On timeout/unknown outcome, reconcile before retrying; do not blindly send again.
7. Log identifiers and outcomes only—never secrets or full sensitive headers.

## 5. Telegram publishing states

Suggested state sequence:

`candidate_created → pending_human → approved | rejected → publishing → published | failed | outcome_unknown`

- `outcome_unknown` requires reconciliation against Telegram and local records before retry.
- A repeated approval callback must not create another message.
- A repeated webhook/update must not duplicate its business side effect.
- Failure records should include a safe error category, retryability, and correlation ID.

## 6. Revenue measurement contract

Keep distinct records for:

- `click`: redirect was requested and validated
- `conversion_pending`: a provider reported a possible conversion
- `conversion_verified`: provider evidence confirms the conversion
- `commission_confirmed`: commission is confirmed under the provider's terms
- `commission_reversed`: commission was cancelled or reversed

Each record should include its event ID, provider/source, campaign/channel, destination or affiliate-link ID, event timestamp, and a privacy-minimized attribution reference. Do not infer conversions or commissions from click counts. Affiliate performance must not change risk decisions.

## 7. Minimum proof before expansion

1. Contract schemas are agreed and versioned.
2. A deterministic test opportunity traverses Hunt → Shield → Core.
3. Missing/stale data and Shield rejection prevent publication.
4. An approved test candidate reaches a Telegram test channel exactly once.
5. Duplicate delivery and retry tests prove no duplicate side effect.
6. Failure/recovery outcomes are visible through correlation IDs and redacted logs.
7. Click, verified conversion, and confirmed commission remain separately measurable.
8. No live trading or paid service is activated as part of this proof.

## 8. Open decisions to settle from code and configuration

- Canonical asset identity and source provenance fields already emitted by Hunt.
- Shield's actual decision vocabulary, expiry semantics, and policy versioning.
- Which component is the authoritative Core/orchestrator in the current deployment.
- Existing Telegram approval, scheduling, and deduplication primitives in tg-content-bot.
- Where durable idempotency records live and their retention period.
- Which free/approved source can provide verifiable conversion data for the first revenue experiment.

These are deliberately open until verified against implementation and deployment configuration.
