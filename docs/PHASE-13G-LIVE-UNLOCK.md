# Phase 13G — Controlled production unlock (Belize)

Status: **COMPLETE** — live request-to-book enabled. Safe unpaid LIVE Checkout proven. **No live money charged.**

Worker: `belize-bookings-prod` · mode `live` · deployment `9e2e3a5e-73c7-4319-b5e5-4166855e3edf`  
Gates: `LIVE_PAYMENTS_CODE_ENABLED=true` · `BOOKINGS_ENABLED=true` · `EMAIL_SENDING_ENABLED=true`  
Public site: `BOOKING_ENABLED` on all three products

## What changed

| Gate / surface | Value |
|----------------|-------|
| Code flag `LIVE_PAYMENTS_CODE_ENABLED` | `true` |
| Prod Worker `BOOKINGS_ENABLED` | `true` |
| Prod Worker `EMAIL_SENDING_ENABLED` | `true` |
| Public `publicBookingStatus` (3 products) | `BOOKING_ENABLED` |

Deploy sequence (Belize PROD only): code flag → bookings → email → public site assets.

## Safe checkout proof (unpaid only)

| Field | Value |
|-------|-------|
| Session created | YES (exactly one LIVE Checkout Session) |
| Reference | `W2BZE-RFYJJTYU` |
| Product | Belize Cave Tubing · 1 guest |
| Amount | `8600` USD |
| Session | `cs_live_…` · status `open` · payment `unpaid` |
| D1 | `payment_pending` / `unpaid` · `payment_intent` null |
| Charge / card entry | **NONE** |
| Lifecycle email | **NONE** (email outbox 0) |
| Payment webhook transition | **NONE** |
| Operator action | **NONE** |
| SEG booking | **NONE** |

Hosted Checkout UI inspected: product **Belize Cave Tubing**, **US$86.00**, card payment available, Link not offered at session level, no SEG terminology. Card fields left empty.

## Products retained

| Product | Price (cents) |
|---------|---------------|
| Cave Tubing | 8600 flat |
| Turtle Snorkel | 11500 / 8500 |
| Altun Ha | 8900 / 7900 |

Passenger rules, cancellation (free ≤14 days), and payment≠confirmation language unchanged.

## Email (send gate ON)

- FROM: `Belize Shore Excursions <bookings@notifications.wowatour.com>`
- REPLY-TO: `hello@belizeshoreexcursion.com`
- No synthetic lifecycle emails were sent in this phase

## Stripe LIVE

- Currency: USD · server-authoritative amounts · `payment_method_types: ["card"]`
- Session-level `wallet_options.link.display="never"`
- Webhook `we_1UD8QVBrD4jBSa7EBrNmpz3y` unchanged (6 events)

## Safety evidence

- Automated tests: **60/60 PASS**
- Public QA: **42/42** protected routes · GREEN
- Public SEG / internal-code leak: **NONE**
- Secrets in git / values printed: **NONE**
- Real-money charge: **NONE**
- www DNS / schedules / CT-2 / other destinations: **untouched**
- Belize TEST Worker: not redeployed for unlock

## Recommended next

**CONTROLLED REAL-MONEY PROOF** — Graham manually completes **ONE** $86 Cave Tubing live payment on a controlled session. Do **not** refund by default. Do **not** place SEG booking. Leave **requested / paid**. Then Phase **13H** read-only close-out.
