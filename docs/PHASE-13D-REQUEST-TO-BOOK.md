# Phase 13D — Request-to-book (Belize)

Status: **13D COMPLETE** — architecture implemented; production remains locked.

## What was shipped (13D)

- Shared bookings Worker source (`belize-bookings-test` / `belize-bookings-prod`) + D1 migrations
- Product-config driven three tours (Cave Tubing / Turtle Snorkel / Altun-Ha)
- Site book journeys at `/book/{slug}/` + `/received/`
- Public product pages rewritten with pricing + Book now CTAs (URLs preserved)
- Terms / privacy aligned with 14-day cancellation / unable-to-confirm refund / request-to-book
- Live kill switch: `LIVE_PAYMENTS_CODE_ENABLED = false` + prod `BOOKINGS_ENABLED=false` + `EMAIL_SENDING_ENABLED=false` + public `PRODUCTION_READY_LOCKED`

## Infrastructure

| Resource | Value |
|----------|-------|
| Test Worker | `https://belize-bookings-test.dark-violet-8d91.workers.dev` — deployed |
| Prod Worker | `https://belize-bookings-prod.dark-violet-8d91.workers.dev` — deployed LOCKED |
| Test D1 | `belize-bookings-test` · `c2473383-c8a2-4ea0-b679-9873716f07f7` · migrations applied |
| Prod D1 | `belize-bookings-prod` · `d9495ab8-4b22-4cb4-a0e6-c490f1eb7042` · migrations applied |
| Booking refs | `W2BZE-…` |
| Unlock phrase | `BELIZE_LIVE_UNLOCK` (unused while code flag false) |
| Gates | `LIVE_PAYMENTS_CODE_ENABLED=false` · prod `BOOKINGS_ENABLED=false` · `EMAIL_SENDING_ENABLED=false` |
| Public lock | `PRODUCTION_READY_LOCKED` — journey visible; Pay disabled |
| Automated tests | **59/59 pass** |

## Public lock behaviour

- Product pages show **Book now** → `/book/{slug}/`
- Booking form journey is visible
- `publicBookingStatus = PRODUCTION_READY_LOCKED` disables Pay & request (shows “Checkout locked — opening soon”)
- Prod Worker: `BOOKINGS_ENABLED=false` + `LIVE_PAYMENTS_CODE_ENABLED=false` + `EMAIL_SENDING_ENABLED=false`
- No live Stripe charge path for customers

## Recommended next

**PHASE 13E — TEST / SANDBOX PROOF** (Stripe TEST + TEST Worker secrets + webhook + operator confirm/decline proofs)
