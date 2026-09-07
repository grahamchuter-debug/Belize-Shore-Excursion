# Phase 13F — Production readiness / live secrets + webhook (Belize)

Status: **BLOCKED — awaiting Graham LIVE secrets** (infra audits otherwise GREEN).  
Gates remain locked. No live money. No prod booking. No prod email. No SEG booking.

Worker: `belize-bookings-prod` · `https://belize-bookings-prod.dark-violet-8d91.workers.dev`  
Mode: `PAYMENTS_MODE=live`  
Gates: `LIVE_PAYMENTS_CODE_ENABLED=false` · `BOOKINGS_ENABLED=false` · `EMAIL_SENDING_ENABLED=false`

Accepted baseline HEAD at start: `ca46762` (Phase 13E GREEN).

## PROD D1

| Name | UUID |
|------|------|
| `belize-bookings-prod` | `d9495ab8-4b22-4cb4-a0e6-c490f1eb7042` |

Migrations applied (none pending). Synthetic / TEST data in PROD: **NONE** (0 bookings, 0 email outbox).

Binding: PROD Worker → PROD D1 only. TEST D1 / other destination databases untouched.

## Secrets (names / presence only — values never recorded)

| Secret | Present on PROD |
|--------|-----------------|
| `STRIPE_SECRET_KEY` (`sk_live_` prefix required) | **NO** — blocked |
| `STRIPE_WEBHOOK_SECRET` (`whsec_` prefix) | **NO** — blocked |
| `RESEND_API_KEY` (`re_` prefix) | **NO** — blocked |
| Permanent `OPERATOR_TOKEN` / `OPERATOR_TEST_TOKEN` | **NONE** (correct) |

Health probe: `liveKeyPresent=false` (expected until LIVE key is put).

Siblings (St Lucia / Martinique / Barbados PROD) already hold LIVE Stripe + Resend secrets, but Cloudflare Worker secrets are write-only — they cannot be copied via `wrangler`. No `sk_live_` material exists on disk. Stripe MCP session is **testmode-only** until Graham re-consents LIVE.

### Graham — put PROD secrets via terminal only (do not paste into chat)

```bash
cd /Users/graham.chuter/Desktop/Caribbean-World-2.0/Belize-Shore-Excursion

npx wrangler secret put STRIPE_SECRET_KEY --config workers/bookings/wrangler.prod.jsonc
# paste sk_live_… only (same LIVE key as sibling PROD Workers)

npx wrangler secret put RESEND_API_KEY --config workers/bookings/wrangler.prod.jsonc
# paste production Resend key (same as sibling PROD Workers)

# Stripe Dashboard → LIVE mode → Developers → Webhooks → Add endpoint
# URL: https://belize-bookings-prod.dark-violet-8d91.workers.dev/api/stripe/webhook
# Events:
#   checkout.session.completed
#   checkout.session.async_payment_succeeded
#   checkout.session.async_payment_failed
#   payment_intent.payment_failed
#   charge.refunded
#   refund.updated
# Do NOT alter Barbados / Martinique / St Lucia / Belize TEST webhooks.

npx wrangler secret put STRIPE_WEBHOOK_SECRET --config workers/bookings/wrangler.prod.jsonc
# paste whsec_… from the new Belize LIVE endpoint only
```

Optional (so Cursor can create the LIVE webhook via Stripe MCP instead of Dashboard): enable LIVE mode for MCP at the Stripe access reconsent URL for this session, then say **continue**.

After secrets are set, say **continue** — agent will verify presence (prefix/health only), confirm webhook endpoint ID, re-check gates, and close Phase 13F GREEN.

## Stripe LIVE webhook

| Field | Value |
|-------|-------|
| Endpoint ID | **PENDING** (not created) |
| URL | `https://belize-bookings-prod.dark-violet-8d91.workers.dev/api/stripe/webhook` |
| Status | pending |
| Events (required) | `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `payment_intent.payment_failed`, `charge.refunded`, `refund.updated` |

Barbados / Martinique / St Lucia / TEST Belize webhooks: **not altered**.

## Email config (send gate OFF)

- FROM: `Belize Shore Excursions <bookings@notifications.wowatour.com>`
- REPLY-TO: `hello@belizeshoreexcursion.com`
- `EMAIL_SENDING_ENABLED=false` — no production lifecycle email sent in 13F
- `RESEND_API_KEY` not yet on PROD (blocked)

## Locked probes (evidence)

- `POST /api/bookings/checkout` → `BOOKINGS_DISABLED` (no live Checkout Session)
- `POST /api/stripe/webhook` (unsigned) → `LIVE_PAYMENTS_BLOCKED` (code flag)
- `POST /api/bookings/operator/confirm` + fake header → `OPERATOR_FORBIDDEN` (live mode rejects header auth)
- Public book UI: checkout prepared and locked; `js/commercial-config.js` → `PRODUCTION_READY_LOCKED`
- Health: `mode=live`, `liveKeyPresent=false`

## Product / payment audit (static)

| Product | Price (cents) | Passenger rule | Max | Cancellation | Internal SEG |
|---------|---------------|----------------|-----|--------------|--------------|
| Cave Tubing | 8600 flat | Guests 8+ / 48"+; child/infant not sold | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZTUBE` |
| Turtle Snorkel | 11500 / 8500 | Adult 12+; Child 6–11; infants not sold; ≥1 adult | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZTURTLE` |
| Altun Ha | 8900 / 7900 | Adult 11+; Child 4–10; under-4 not sold; ≥1 adult | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZALTUN` |

- `bookingMode: "request"` — payment success → `requested` / `paid` via `statusAfterPaymentSuccess("request")` — **never** auto-confirmed
- Unable to confirm → decline + full refund (architecture; not executed on PROD)
- Stripe Checkout (future LIVE): USD · server-authoritative pricing · `payment_method_types: ["card"]` · `wallet_options.link.display="never"`
- Terms: Payment is not confirmation · free cancellation up to 14 days
- Operator: booking-scoped single-use hashed review tokens only; live header auth hard-disabled
- Fulfilment notes internal only — no public SEG / CABZ leak

## TEST evidence preserved (untouched)

TEST Worker secrets retained. TEST D1 `belize-bookings-test` still holds Phase 13E proof rows (5 bookings / 8 outbox), including:

- `W2BZE-U46HGXGN` cave · confirmed/paid
- `W2BZE-ALFEEUEN` turtle · supplier_declined/refunded
- `W2BZE-5XFGYJFG` altun · requested/paid

No paid TEST rerun in 13F.

## Safety evidence (pre-secret)

- Automated tests: **60/60 PASS**
- Public QA: **42/42** protected routes · GREEN
- Public SEG / internal-code leak: **NONE**
- Secrets in git: **NONE**
- Real-money charge / live Checkout Session / SEG booking / prod refund / fake prod booking: **NONE**
- www DNS / schedules / CT-2 / other destinations: **untouched**
- All three gates remain **FALSE**

## Recommended next

1. Graham completes the three `wrangler secret put` commands + LIVE webhook (or MCP LIVE reconsent).
2. Agent resumes → verify → close **PHASE 13F GREEN**.
3. Then **PHASE 13G — CONTROLLED PRODUCTION UNLOCK** only when Graham explicitly authorises flipping the three gates.
