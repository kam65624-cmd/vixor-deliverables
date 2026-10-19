# VIXOR × tg-content-bot — Proposed Integration Contracts

**Task ID:** VIXOR-TG-INTEGRATION-P0  
**Status:** Proposal only — no endpoint or schema in this document is implemented or confirmed live.  
**Purpose:** Define a safe first contract boundary between VIXOR app, Hunt, Shield and tg-content-bot without merging databases.

## 1. Contract principles

- Use HTTPS JSON APIs between services; no direct cross-database reads. Existing Shield `POST /ingest/blocklist` and Trade `POST /ingest/signals` handlers already demonstrate timestamped HMAC headers (`x-vixor-timestamp`, `x-vixor-signature`); these are existing service-specific contracts, not a universal contract. Inspect their full validation behavior before reusing or standardizing them. Hunt's visible `/engine/*` POST routes do not show an equivalent auth check in the route handlers reviewed, so do not expose them as trusted integration endpoints without a security review.
- Treat each existing store as private to its owning service.
- Every event has a stable `event_id`, `schema_version`, `occurred_at`, `producer`, and trace/correlation ID.
- Authenticate service-to-service calls using scoped credentials and request signing (HMAC over method, path, timestamp, nonce and body digest) or a managed identity mechanism supported by the hosting platform. Never put service secrets in Mini App/browser code.
- Enforce timestamp tolerance, nonce/replay protection, request-size limits, schema validation, rate limits and explicit timeouts. Current Shield and Trade ingest handlers have a ±5 minute timestamp window, but a one-time nonce is not visible in the reviewed handlers; the proposed standard should close that gap. Trade's `GET /debug/brief` currently compares a query parameter with `WEBHOOK_SECRET`; do not copy this pattern into new contracts.
- Use idempotency keys and unique constraints for all event ingestion and publishing.
- Never treat missing risk data as safe. Use `unknown` and prevent automatic publication when risk cannot be verified.
- Do not send wallet private keys, service keys, full Telegram init data, or unnecessary personal data in event payloads.
- All proposed statuses and fields below are contract design, not assertions about existing implementations.

## 2. Proposed event envelope

```json
{
  "schema_version": "1.0",
  "event_id": "evt_<stable-unique-id>",
  "event_type": "signal.discovered",
  "producer": "vixor-hunt",
  "occurred_at": "2026-01-01T00:00:00Z",
  "correlation_id": "corr_<stable-id>",
  "idempotency_key": "signal:<chain>:<address>:<source-event-id>",
  "data": {}
}
```

Consumers must reject unsupported schema versions, invalid timestamps, missing required fields and replayed event IDs. Producers must retry transient failures with bounded exponential backoff and jitter; permanent 4xx validation/auth errors must not be retried blindly.

## 3. Signal discovery — Hunt → Integration API

### Proposed request data

```json
{
  "chain": "solana",
  "asset_address": "<canonical-mint-address>",
  "symbol": "EXAMPLE",
  "name": "Example Token",
  "source": "provider-name",
  "source_url": "https://example.invalid/source",
  "detected_at": "2026-01-01T00:00:00Z",
  "metrics": {
    "price_usd": null,
    "liquidity_usd": null,
    "volume_24h_usd": null,
    "market_cap_usd": null
  },
  "evidence": [],
  "expires_at": "2026-01-01T00:05:00Z"
}
```

Rules:
- Chain + normalized asset address are the primary identity; symbol is display-only and never unique.
- Unknown metrics are `null`, not zero.
- Evidence/source URLs must be treated as untrusted input and never fetched server-side without SSRF controls.
- The receiving service assigns/validates a canonical `signal_id`; the source's stable event ID remains available for dedupe.
- Validate provider timestamps and set a maximum accepted age.

## 4. Risk assessment — Integration API → Shield

### Proposed request

```json
{
  "chain": "solana",
  "asset_address": "<canonical-mint-address>",
  "signal_id": "sig_<id>",
  "requested_at": "2026-01-01T00:00:00Z",
  "context": "publication_review"
}
```

### Proposed response

```json
{
  "schema_version": "1.0",
  "chain": "solana",
  "asset_address": "<canonical-mint-address>",
  "risk_status": "assessed",
  "risk_score": 82,
  "severity": "high",
  "reason_codes": ["LIQUIDITY_LOW", "OWNER_RISK_REVIEW"],
  "assessed_at": "2026-01-01T00:00:00Z",
  "expires_at": "2026-01-01T00:02:00Z",
  "assessment_id": "risk_<id>"
}
```

Allowed status values: `assessed`, `unknown`, `unavailable`, `invalid_asset`. Define score direction and severity thresholds in a separately approved policy; do not assume a numeric score's meaning across services. A timeout, provider failure or expired result must map to `unknown/unavailable`, never a low-risk default. Keep reason codes machine-readable and human explanations non-authoritative.

## 5. Canonical signal lifecycle

Proposed states:

`discovered → enriching → reviewed → approved → queued → published`

Terminal or exception states:

`rejected`, `expired`, `risk_unavailable`, `publish_failed`, `cancelled`.

Rules:
- Only the selected canonical owner can transition signal approval state.
- All transitions record actor/service, timestamp, prior state, next state and reason.
- A signal must be unexpired at approval and immediately before publishing.
- Risk must be assessed within its TTL at approval and immediately before publishing.
- `published` requires Telegram's successful response and persisted chat/message IDs; a timeout after sending requires reconciliation before retrying.
- Retrying must not create a second post for the same idempotency key.

## 6. Publication request — Signal owner → tg-content-bot

### Proposed request

```json
{
  "schema_version": "1.0",
  "event_id": "evt_<stable-id>",
  "signal_id": "sig_<id>",
  "idempotency_key": "publish:<channel-id>:<signal-id>:<template-version>",
  "target": {
    "channel_id": "<internal-channel-id>",
    "template_version": "1"
  },
  "content": {
    "title": "Example signal",
    "body": "Reviewed summary.",
    "asset_address": "<canonical-address>",
    "chain": "solana",
    "risk_label": "High risk",
    "source_url": "https://example.invalid/source"
  },
  "valid_until": "2026-01-01T00:05:00Z",
  "approval": {
    "approved_by": "owner-or-authorized-reviewer",
    "approved_at": "2026-01-01T00:00:00Z"
  }
}
```

The exact endpoint path and storage target must be chosen after reviewing the current Worker routes and database schema. Prefer adding an authenticated internal ingestion route that creates a **draft** in the existing queue/outbox over calling Telegram's send API directly. Do not create a second publisher or bypass existing outbox logic.

### Proposed response

```json
{
  "accepted": true,
  "status": "queued_for_review",
  "publication_id": "pub_<id>",
  "idempotency_key": "publish:<channel-id>:<signal-id>:<template-version>"
}
```

A response of `accepted` means only that the request was validated and persisted; it does **not** mean the Telegram post was sent.

## 7. Telegram account linking — user ↔ VIXOR

Proposed flow:
1. User initiates linking from an authenticated VIXOR session.
2. Client supplies Telegram Mini App init data only to a server endpoint over HTTPS.
3. Server verifies Telegram's init-data signature/hash using the bot token and validates `auth_date` freshness.
4. Server issues a short-lived, one-time link challenge bound to the authenticated VIXOR user and verified Telegram user ID.
5. User explicitly confirms the link; server atomically consumes the challenge and creates the link.
6. Re-linking, unlinking, collisions and account recovery have documented policies and audit events.

Do not trust `telegram_user_id` sent as a plain client field. Never store the raw init data longer than needed. Do not expose Telegram IDs in public signal payloads. The owning identity service and exact table are to be decided only after inspecting existing auth tables/RLS.

## 8. Affiliate and click attribution

- Use opaque internal IDs for affiliate, signal, publication and click.
- Referral codes are configuration owned by the operator; seed placeholders such as `YOUR_AXIOM_REF` must be disabled until replaced with verified codes.
- Redirect endpoints must allowlist destinations or resolve them from trusted database configuration; never accept an arbitrary redirect URL from a request.
- Capture only required attribution fields: click ID, publication ID, channel ID, affiliate ID, timestamp and coarse anti-abuse metadata where lawful.
- Define attribution window and dedupe policy before reporting revenue.
- Do not pass Telegram user ID or wallet address in external affiliate URLs unless there is a separately approved, privacy-reviewed need.

## 9. Arbitrage data boundary

Arbitrage opportunities are highly time-sensitive. If surfaced in a bot or Mini App:
- Treat them as read-only informational cards.
- Include detected/expiry times, net-profit assumptions, source and a clear stale/expired state.
- Revalidate data on server side and suppress expired opportunities.
- Do not accept a publish event as an instruction to execute a trade.
- Keep wallet signing, execution credentials and live trading permissions outside the publishing worker.
- Maintain dry-run default and require explicit owner approval for any live execution, consistent with the master prompt.

## 10. Error model

Use a consistent response envelope:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request failed validation.",
    "retryable": false,
    "correlation_id": "corr_<id>"
  }
}
```

Suggested mapping:
- `400 VALIDATION_ERROR`: invalid schema/field; not retryable.
- `401 AUTHENTICATION_FAILED` / `403 NOT_AUTHORIZED`: stop retries and alert.
- `409 IDEMPOTENCY_CONFLICT`: retrieve/reconcile existing result; do not resend.
- `410 EXPIRED`: discard or re-review upstream.
- `429 RATE_LIMITED`: bounded backoff respecting Retry-After.
- `503 DEPENDENCY_UNAVAILABLE`: retry with backoff; do not downgrade risk status.
- `500 INTERNAL_ERROR`: log correlation ID; never return stack traces or secrets.

## 11. Minimum acceptance tests before staging integration

- Invalid HMAC/signature, old timestamp, reused nonce and wrong service identity are rejected.
- Invalid chain/address and unsupported schema version are rejected.
- Duplicate event delivery creates one canonical signal and one publication request.
- Risk service timeout yields `unknown/unavailable` and blocks automatic publication.
- Expired signal/risk result is rejected both at approval and at send time.
- Telegram send timeout triggers reconciliation before retry; no duplicate post is created.
- Untrusted source URL cannot cause server-side request forgery or open redirect.
- Telegram account linking fails for forged/expired init data and replayed challenge.
- No secrets, raw init data, private keys or unnecessary user identifiers appear in logs.
- Kill switch stops new ingestion/publication while preserving queued records.
- No test uses real wallet execution or sends to a production channel.

## 12. Decisions required before implementation

1. Which system owns the canonical signal and approval lifecycle: VIXOR Supabase or another existing service?
2. Which internal service authentication mechanism is approved and where will keys be stored/rotated?
3. Which Shield score policy and reason-code vocabulary are canonical?
4. Which channel(s) may be used for staging tests?
5. Who approves production auto-publishing and what is the rollback owner?
6. What is the retention policy for click attribution and Telegram account links?

Until these are approved and the PDF/source/schema evidence gaps are closed, these contracts remain design-only.
