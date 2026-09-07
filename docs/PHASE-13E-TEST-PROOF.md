# Phase 13E — Controlled Stripe TEST proof (Belize)

Status: **COMPLETE** — TEST lifecycle proven. Live payments remain locked.

Worker: `belize-bookings-test` · mode `test` · live key absent on TEST  
Prod: `belize-bookings-prod` · `BOOKINGS_ENABLED=false` · `EMAIL_SENDING_ENABLED=false` · no secrets · `LIVE_PAYMENTS_CODE_ENABLED=false`

## D1

| Env | Name | UUID |
|-----|------|------|
| TEST | `belize-bookings-test` | `c2473383-c8a2-4ea0-b679-9873716f07f7` |
| PROD | `belize-bookings-prod` | `d9495ab8-4b22-4cb4-a0e6-c490f1eb7042` |

Migrations applied to both. Existing destination D1 databases untouched.

## Stripe TEST webhook

- Endpoint ID: `we_1UD7XiBrD4jBSa7ERXSlXGO5`
- URL: `https://belize-bookings-test.dark-violet-8d91.workers.dev/api/stripe/webhook`
- Events: `checkout.session.completed`, `checkout.session.async_payment_succeeded`, `checkout.session.async_payment_failed`, `payment_intent.payment_failed`, `charge.refunded`, `refund.updated`
- Sibling destination webhooks left unchanged

## Checkout / payment proofs (TEST card 4242)

| Case | Ref | Amount | D1 after pay | After operator |
|------|-----|--------|--------------|----------------|
| Cave Tubing 1 guest | W2BZE-U46HGXGN | USD 8600 | requested / paid | confirmed / paid |
| Turtle 1 adult + 1 child | W2BZE-ALFEEUEN | USD 20000 | requested / paid | supplier_declined / refunded |
| Altun 1 adult + 1 child | W2BZE-5XFGYJFG | USD 16800 | requested / paid | left requested / paid |

Webhook: `checkout.session.completed` recorded once per paid booking (`processed_events`). No auto-confirm on payment.

Stripe Checkout QA (Cave session): currency `usd`, amount `8600`, `payment_method_types: ["card"]`, session `wallet_options.link.display=never`. Apple Pay wallet affordance observed in hosted UI (report-only; no account-wide change).

## Operator (TEST header token only)

- Confirm W2BZE-U46HGXGN → `confirmed` / paid · `customer_confirmed` sent once · no refund · duplicate confirm `duplicate:true`
- Decline W2BZE-ALFEEUEN → full Stripe TEST refund · amount 20000 · `supplier_declined` / `refunded` · `customer_declined` sent once · `charge.refunded` + `refund.updated` · duplicate decline safe

Altun W2BZE-5XFGYJFG left `requested` / `paid` (no operator action).

## Emails (TEST sending temporarily enabled + `TEST_ONLY_EMAIL_OVERRIDE` → `info@wowatour.com`)

| Booking | Outbox (each ×1, status sent) |
|---------|-------------------------------|
| Cave | `customer_requested`, `ops_request`, `customer_confirmed` |
| Turtle | `customer_requested`, `ops_request`, `customer_declined` |
| Altun | `customer_requested`, `ops_request` — no confirmed/declined |

Customer emails: payment received / request received / not yet confirmed wording; no SEG/CABZ codes. Reply-To configured as `hello@belizeshoreexcursion.com` via Worker vars. Ops emails may include INTERNAL SEG fulfilment notes (ops-only).

After proof: TEST `EMAIL_SENDING_ENABLED=false` redeployed (sibling hygiene). Secrets retained on TEST.

## Failures / validation (live TEST Worker)

Rejected: Cave ack false / zero guests / >10; Turtle child-only / infant-only / >10; Altun child-only / infant-only / >10; past date (`CRUISE`); missing ship; invalid product; price tamper (`PRICE`). Server price authoritative.

Webhook: invalid signature rejected; redelivery of processed `checkout.session.completed` returns `duplicate:true` with no extra emails/transitions.

Operator security: missing/wrong header token → `OPERATOR_FORBIDDEN`; unknown ref → `NOT_FOUND`; Altun unchanged.

## Automated / public

- Automated suite: **60/60 pass** (added past-date + Belize ops heading guard)
- Public QA: **42/42** · production checkout locked · no public SEG leak · www / extensionless / 404 / sitemap / robots OK

## Safety left after proof

- TEST: `EMAIL_SENDING_ENABLED=false` · bookings remain enabled for further TEST · secrets retained
- Prod unchanged / locked · site `PRODUCTION_READY_LOCKED` · no live money · no SEG booking · no other destination changes

## Recommended next

**PHASE 13F — PRODUCTION READINESS / LIVE SECRETS + WEBHOOK / REMAIN LOCKED**
