# Phase 13F — Production readiness / live secrets + webhook (Belize)

Status: **COMPLETE** — production ready. **All gates remain locked.**  
No live money. No prod booking. No prod email. No SEG booking.

Worker: `belize-bookings-prod` · `https://belize-bookings-prod.dark-violet-8d91.workers.dev`  
Deployment version: `5b601c95-195c-41be-9c35-ef54bc1b2a55`  
Mode: `PAYMENTS_MODE=live`  
Gates: `LIVE_PAYMENTS_CODE_ENABLED=false` · `BOOKINGS_ENABLED=false` · `EMAIL_SENDING_ENABLED=false`

## PROD D1

| Name | UUID |
|------|------|
| `belize-bookings-prod` | `d9495ab8-4b22-4cb4-a0e6-c490f1eb7042` |

Migrations applied. Synthetic / TEST data in PROD: **NONE** (0 bookings, 0 email outbox).

Binding: PROD Worker → PROD D1 only. TEST D1 / other destination databases untouched.

## Secrets (names / presence only — values never recorded)

| Secret | Present |
|--------|---------|
| `STRIPE_SECRET_KEY` | YES (`sk_live_` — health `liveKeyPresent=true`) |
| `STRIPE_WEBHOOK_SECRET` | YES |
| `RESEND_API_KEY` | YES |
| Permanent `OPERATOR_TOKEN` / `OPERATOR_TEST_TOKEN` | **NONE** |

## Stripe LIVE webhook

| Field | Value |
|-------|-------|
| Endpoint ID | `we_1UD8QVBrD4jBSa7EBrNmpz3y` |
| URL | `https://belize-bookings-prod.dark-violet-8d91.workers.dev/api/stripe/webhook` |
| Status | enabled · livemode |
| Events | `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `payment_intent.payment_failed`, `charge.refunded`, `refund.updated` |

Barbados / Martinique / St Lucia / TEST Belize webhooks were not altered.

## Email config (send gate OFF)

- FROM: `Belize Shore Excursions <bookings@notifications.wowatour.com>`
- REPLY-TO: `hello@belizeshoreexcursion.com`
- `EMAIL_SENDING_ENABLED=false` — no production lifecycle email sent in 13F

## Locked probes

- Public / Worker checkout → `BOOKINGS_DISABLED` (no live Checkout Session)
- Unsigned webhook → `LIVE_PAYMENTS_BLOCKED` (code flag)
- Operator header confirm → `OPERATOR_FORBIDDEN` (live mode rejects header auth)
- Site book routes: checkout prepared and locked · `PRODUCTION_READY_LOCKED`

## Product / payment audit (static)

| Product | Price (cents) | Passenger rule | Max | Cancellation | Internal SEG |
|---------|---------------|----------------|-----|--------------|--------------|
| Cave Tubing | 8600 flat | Guests 8+ / 48"+; child/infant not sold | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZTUBE` |
| Turtle Snorkel | 11500 / 8500 | Adult 12+; Child 6–11; infants not sold; ≥1 adult | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZTURTLE` |
| Altun Ha | 8900 / 7900 | Adult 11+; Child 4–10; under-4 not sold; ≥1 adult | 10 | Free ≤14 days | `SEG_MANUAL` · `CABZALTUN` |

- Payment success state: `requested` / `paid` — **never** auto-confirmed
- Unable to confirm → decline + full refund (architecture; not executed on PROD)
- Stripe Checkout (future LIVE): USD · server-authoritative pricing · `payment_method_types: ["card"]` · `wallet_options.link.display="never"`
- Operator: booking-scoped single-use hashed review tokens only
- Fulfilment: `SEG_MANUAL` / internal codes / net UNKNOWN — **internal notes only**; no public SEG leak

## TEST evidence preserved

TEST Worker secrets retained. TEST D1 Phase 13E proof rows left intact (not destroyed; paid TEST not rerun in 13F).

## Safety evidence

- Automated tests: **60/60 PASS**
- Public QA: **42/42** protected routes · GREEN
- Public SEG / internal-code leak: **NONE**
- Secrets in git: **NONE**
- Real-money charge / live Checkout Session / SEG booking / prod refund / fake prod booking: **NONE**
- www DNS / schedules / CT-2 / other destinations: **untouched**

## Recommended next

**PHASE 13G — CONTROLLED PRODUCTION UNLOCK** (only when Graham authorises flipping the three gates and accepting first live traffic).
