#!/usr/bin/env python3
"""Generate /book/{slug}/ and /book/{slug}/received/ pages for Belize RTB products."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from belize_shell import footer, nav  # noqa: E402

PRODUCTS = [
    {
        "id": "belize-cave-tubing",
        "name": "Belize Cave Tubing",
        "product_path": "/belize-cave-tubing.html",
        "price_list": "<li>Eligible guests (8+ / 48&quot;+) — $86</li><li>Infants — not permitted</li>",
        "guest_fieldset": """
        <fieldset class="booking-fieldset">
          <legend>How many people are travelling?</legend>
          <label for="adults">Guests <span class="muted">— $86 each</span>
            <input type="number" name="adults" id="adults" min="1" max="10" value="2" required />
          </label>
          <p class="help">All participants must be at least 8 years old and at least 48 inches tall. Infants are not permitted. Maximum 10 guests online. For larger groups email <a href="mailto:hello@belizeshoreexcursion.com">hello@belizeshoreexcursion.com</a>.</p>
        </fieldset>
        <label class="consent" id="eligibility-wrap">
          <input type="checkbox" name="eligibility" id="booking_eligibility" required />
          <span>I confirm all participants are at least 8 years old and at least 48 inches tall.</span>
        </label>
        <div class="booking-review" id="booking-review" aria-live="polite">
          <h3>Review</h3>
          <dl>
            <div><dt>Tour</dt><dd>Belize Cave Tubing</dd></div>
            <div><dt>Date</dt><dd id="rev-date">—</dd></div>
            <div><dt>Cruise ship</dt><dd id="rev-ship">—</dd></div>
            <div><dt>Guests</dt><dd id="rev-adults">—</dd></div>
            <div id="rev-children-row" hidden><dt>Children</dt><dd id="rev-children">—</dd></div>
            <div class="booking-total"><dt>Total</dt><dd id="rev-total">USD $0</dd></div>
          </dl>
          <p class="help">Displayed total is for review. The charge amount is always calculated server-side. This is a request — payment does not confirm the excursion.</p>
        </div>""",
        "duration": "About 5 hours",
        "meeting": "Meeting: Cruise Ship Tender Pier. Exact instructions after confirmation.",
    },
    {
        "id": "turtle-snorkel-and-island-time",
        "name": "Turtle Snorkel and Island Time",
        "product_path": "/turtle-snorkel-and-island-time.html",
        "price_list": "<li>Adults (12+) — $115</li><li>Children (6–11) — $85</li><li>Infants — not permitted</li>",
        "guest_fieldset": """
        <fieldset class="booking-fieldset">
          <legend>How many people are travelling?</legend>
          <label for="adults">Adults (12+) <span class="muted">— $115</span>
            <input type="number" name="adults" id="adults" min="1" max="10" value="2" required />
          </label>
          <label for="children">Children (6–11) <span class="muted">— $85</span>
            <input type="number" name="children" id="children" min="0" max="10" value="0" />
          </label>
          <p class="help">At least one adult is required. Children under 12 wear a life jacket and must be accompanied by an adult. Infants are not permitted. Maximum 10 guests online.</p>
        </fieldset>
        <div class="booking-review" id="booking-review" aria-live="polite">
          <h3>Review</h3>
          <dl>
            <div><dt>Tour</dt><dd>Turtle Snorkel and Island Time</dd></div>
            <div><dt>Date</dt><dd id="rev-date">—</dd></div>
            <div><dt>Cruise ship</dt><dd id="rev-ship">—</dd></div>
            <div><dt>Adults</dt><dd id="rev-adults">—</dd></div>
            <div id="rev-children-row"><dt>Children</dt><dd id="rev-children">—</dd></div>
            <div class="booking-total"><dt>Total</dt><dd id="rev-total">USD $0</dd></div>
          </dl>
          <p class="help">Displayed total is for review. The charge amount is always calculated server-side. This is a request — payment does not confirm the excursion.</p>
        </div>""",
        "duration": "About 5 hours",
        "meeting": "Meeting: about a 2-minute walk from the tender pier. Exact instructions after confirmation.",
    },
    {
        "id": "altun-ha-and-belize-city-overview",
        "name": "Altun-Ha and Belize City Overview",
        "product_path": "/altun-ha-and-belize-city-overview.html",
        "price_list": "<li>Adults (11+) — $89</li><li>Children (4–10) — $79</li><li>Under 4 — not sold online</li>",
        "guest_fieldset": """
        <fieldset class="booking-fieldset">
          <legend>How many people are travelling?</legend>
          <label for="adults">Adults (11+) <span class="muted">— $89</span>
            <input type="number" name="adults" id="adults" min="1" max="10" value="2" required />
          </label>
          <label for="children">Children (4–10) <span class="muted">— $79</span>
            <input type="number" name="children" id="children" min="0" max="10" value="0" />
          </label>
          <p class="help">At least one adult is required. Not recommended for children aged 3 and under — email <a href="mailto:hello@belizeshoreexcursion.com">hello@belizeshoreexcursion.com</a> before booking if you need advice. Maximum 10 guests online.</p>
        </fieldset>
        <div class="booking-review" id="booking-review" aria-live="polite">
          <h3>Review</h3>
          <dl>
            <div><dt>Tour</dt><dd>Altun-Ha and Belize City Overview</dd></div>
            <div><dt>Date</dt><dd id="rev-date">—</dd></div>
            <div><dt>Cruise ship</dt><dd id="rev-ship">—</dd></div>
            <div><dt>Adults</dt><dd id="rev-adults">—</dd></div>
            <div id="rev-children-row"><dt>Children</dt><dd id="rev-children">—</dd></div>
            <div class="booking-total"><dt>Total</dt><dd id="rev-total">USD $0</dd></div>
          </dl>
          <p class="help">Displayed total is for review. The charge amount is always calculated server-side. This is a request — payment does not confirm the excursion.</p>
        </div>""",
        "duration": "About 4 hours",
        "meeting": "Meeting: Cruise Ship Tender Pier. Exact instructions after confirmation.",
    },
]


def book_page(p: dict) -> str:
    pid = p["id"]
    name = p["name"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Book {name} | Belize Shore Excursions</title>
  <meta name="description" content="Request {name} online. Pay securely to request — confirmation is emailed separately." />
  <link rel="canonical" href="https://belizeshoreexcursion.com/book/{pid}/" />
  <meta name="robots" content="noindex,follow" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,600;7..72,700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body data-page="book" data-product-id="{pid}">
{nav("excursions")}
<main id="main" class="page-main">

<section class="section booking-flow">
  <div class="wrap booking-shell">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a> · <a href="{p["product_path"]}">{name}</a> · Booking
    </nav>
    <p class="eyebrow">Booking request</p>
    <h1>Book your excursion</h1>
    <p>Choose your cruise date and complete payment to send your booking request. Confirmation is emailed separately after we arrange your excursion.</p>
    <ol class="booking-steps" aria-label="Booking steps">
      <li class="is-current">Tour</li>
      <li>Date / cruise</li>
      <li>Guests</li>
      <li>Details</li>
      <li>Review</li>
      <li>Payment</li>
      <li>Received</li>
    </ol>
    <div class="booking-panel">
      <h2>{name}</h2>
      <ul class="price-list">{p["price_list"]}</ul>
      <p class="help">{p["duration"]}. {p["meeting"]}</p>
      <div class="booking-status-banner" id="booking-status-banner" role="status">
        <strong id="booking-status-title">Online checkout is prepared and locked.</strong>
        <p id="booking-status-body">Pay securely online to request your excursion. Your booking is confirmed separately after availability is checked. Live card payments are not enabled yet.</p>
      </div>
      <form class="booking-form" id="bz-booking-form" method="post" action="#" data-product-id="{pid}" data-live="0" novalidate>
        <fieldset class="booking-fieldset">
          <legend>Date / cruise</legend>
          <label for="cruise_date">Excursion date
            <input type="date" name="cruise_date" id="cruise_date" required min="2026-09-01" max="2028-12-31" />
          </label>
          <label for="ship_name">Cruise ship
            <input type="text" name="ship_name" id="ship_name" required maxlength="80" autocomplete="organization" placeholder="e.g. Celebrity Beyond" />
          </label>
          <p class="help">Enter your ship and date. We do not invent a published Belize ship-call schedule.</p>
        </fieldset>
{p["guest_fieldset"]}
        <fieldset class="booking-fieldset">
          <legend>Lead passenger details</legend>
          <label for="lead_name">Full name
            <input type="text" name="name" id="lead_name" required minlength="2" autocomplete="name" />
          </label>
          <label for="lead_email">Email
            <input type="email" name="email" id="lead_email" required autocomplete="email" />
          </label>
          <label for="lead_phone">Mobile / WhatsApp
            <input type="tel" name="phone" id="lead_phone" required autocomplete="tel" />
          </label>
          <label for="mobility">Mobility information
            <textarea name="mobility" id="mobility" rows="2" maxlength="500" placeholder="Any walking limits or mobility needs we should know about"></textarea>
          </label>
          <label for="special_requirements">Special requirements <span class="muted">(optional)</span>
            <textarea name="special_requirements" id="special_requirements" rows="2" maxlength="800"></textarea>
          </label>
          <p class="help">The booking contact must be an adult.</p>
        </fieldset>
        <div class="booking-honesty" id="booking-honesty">
          <h3>Subject to confirmation</h3>
          <p>After payment, we'll arrange your excursion and send your confirmation as soon as it is confirmed. Payment does not mean the excursion is confirmed yet.</p>
          <p>If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.</p>
          <p>Free cancellation up to 14 days before your excursion. Cancellations made within 14 days of departure are non-refundable.</p>
        </div>
        <label class="consent">
          <input type="checkbox" name="ack" id="booking_ack" required />
          <span>I understand this is a booking request. Payment is taken when I submit my request and does not confirm the excursion. Confirmation will be emailed separately when my places are confirmed. If the excursion cannot be confirmed, the amount paid will be refunded in full to my original payment method.</span>
        </label>
        <p id="booking-error" class="booking-error" hidden role="alert"></p>
        <div class="booking-actions">
          <a class="btn btn--outline" href="{p["product_path"]}">Back</a>
          <button type="submit" class="btn btn--solid" id="booking-submit" hidden>Pay &amp; request</button>
          <button type="button" class="btn btn--solid" id="booking-submit-locked" disabled title="Live checkout is locked">Checkout locked — opening soon</button>
        </div>
        <p class="help" id="booking-footer-note">Live payments remain locked on this product. Prefer to ask first? <a href="mailto:hello@belizeshoreexcursion.com">hello@belizeshoreexcursion.com</a></p>
      </form>
    </div>
  </div>
</section>

</main>
{footer()}
  <script src="/js/commercial-config.js" defer></script>
  <script src="/js/booking.js" defer></script>
  <script src="/js/nav.js" defer></script>
</body>
</html>
"""


def received_page(p: dict) -> str:
    pid = p["id"]
    name = p["name"]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Request received | Belize Shore Excursions</title>
  <meta name="description" content="Your Belize excursion payment was received. This is a booking request, not a confirmation." />
  <link rel="canonical" href="https://belizeshoreexcursion.com/book/{pid}/received/" />
  <meta name="robots" content="noindex,follow" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,500;7..72,600;7..72,700&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body data-page="book" data-product-id="{pid}">
{nav("excursions")}
<main id="main" class="page-main">

<section class="section">
  <div class="wrap booking-shell">
    <p class="eyebrow">Booking request</p>
    <h1>Request received</h1>
    <p>We've received your payment and your excursion request. This is not a booking confirmation. We're arranging your {name} and will email you again once it is confirmed.</p>
    <div id="booking-ref-wrap" class="booking-ref" hidden>
      <p class="eyebrow">Booking reference</p>
      <p id="booking-ref" class="booking-ref__code"></p>
    </div>
    <ul>
      <li>Payment successful — request awaiting confirmation</li>
      <li>Confirmation is emailed separately when places are arranged</li>
      <li>If we are unable to confirm, you will receive a full refund to your original payment method</li>
      <li>Meeting instructions will be provided with your confirmed excursion details</li>
    </ul>
    <div class="hero__actions">
      <a class="btn btn--solid" href="{p["product_path"]}">Back to tour</a>
      <a class="btn btn--outline" href="mailto:hello@belizeshoreexcursion.com">Contact us</a>
    </div>
  </div>
</section>

</main>
{footer()}
  <script src="/js/booking-received.js" defer></script>
  <script src="/js/nav.js" defer></script>
</body>
</html>
"""


def main() -> None:
    for p in PRODUCTS:
        book_dir = ROOT / "book" / p["id"]
        recv_dir = book_dir / "received"
        book_dir.mkdir(parents=True, exist_ok=True)
        recv_dir.mkdir(parents=True, exist_ok=True)
        (book_dir / "index.html").write_text(book_page(p), encoding="utf-8")
        (recv_dir / "index.html").write_text(received_page(p), encoding="utf-8")
        print(f"  wrote book/{p['id']}/")


if __name__ == "__main__":
    main()
