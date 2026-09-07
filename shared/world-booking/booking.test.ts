/**
 * Shared booking engine tests — Belize Phase 13D (three RTB products).
 */
import assert from "node:assert/strict";
import { test } from "node:test";
import { findBelizeBookingProduct, BELIZE_BOOKING_PRODUCTS, BELIZE_CANCELLATION_COPY } from "../destinations/belize-products";
import { belizeBookingCore } from "../destinations/belize";
import {
  assertClientTotalMatches,
  calculateBookingQuote,
  createBookingReference,
  destinationBrandFromCore,
  requestedCustomerEmail,
  statusAfterPaymentSuccess,
  supplierRequestEmail,
  validateCruise,
  validateCustomer,
} from "./index";

const brand = destinationBrandFromCore(belizeBookingCore);
const cave = findBelizeBookingProduct("belize-cave-tubing");
const turtle = findBelizeBookingProduct("turtle-snorkel-and-island-time");
const altun = findBelizeBookingProduct("altun-ha-and-belize-city-overview");
assert.ok(cave);
assert.ok(turtle);
assert.ok(altun);

test("three Belize product IDs present", () => {
  assert.equal(BELIZE_BOOKING_PRODUCTS.length, 3);
  assert.deepEqual(
    BELIZE_BOOKING_PRODUCTS.map((p) => p.id).sort(),
    ["altun-ha-and-belize-city-overview", "belize-cave-tubing", "turtle-snorkel-and-island-time"].sort(),
  );
});

test("Cave tubing flat USD 86; infants/children not sold as separate bands", () => {
  assert.equal(cave!.pricing.model, "flat_per_guest");
  assert.equal(cave!.pricing.pricePerGuest, 86);
  assert.equal(calculateBookingQuote(cave!, { adults: 1, children: 0, infants: 0 }).amountCents, 8600);
  assert.equal(calculateBookingQuote(cave!, { adults: 2, children: 0, infants: 0 }).amountCents, 17200);
  assert.throws(() => calculateBookingQuote(cave!, { adults: 1, children: 0, infants: 1 }));
});

test("Turtle adult 115 child 85; infants not sold; requires adult", () => {
  assert.equal(turtle!.pricing.adultAmount, 115);
  assert.equal(turtle!.pricing.childAmount, 85);
  assert.equal(turtle!.pricing.infantPricingStatus, "not_sold");
  assert.equal(calculateBookingQuote(turtle!, { adults: 1, children: 0, infants: 0 }).amountCents, 11500);
  assert.equal(calculateBookingQuote(turtle!, { adults: 1, children: 1, infants: 0 }).amountCents, 20000);
  assert.throws(() => calculateBookingQuote(turtle!, { adults: 0, children: 1, infants: 0 }));
  assert.throws(() => calculateBookingQuote(turtle!, { adults: 1, children: 0, infants: 1 }));
});

test("Altun adult 89 child 79; no under-4; requires adult", () => {
  assert.equal(altun!.pricing.adultAmount, 89);
  assert.equal(altun!.pricing.childAmount, 79);
  assert.equal(altun!.pricing.infantPricingStatus, "not_sold");
  assert.equal(calculateBookingQuote(altun!, { adults: 1, children: 0, infants: 0 }).amountCents, 8900);
  assert.equal(calculateBookingQuote(altun!, { adults: 1, children: 1, infants: 0 }).amountCents, 16800);
  assert.throws(() => calculateBookingQuote(altun!, { adults: 0, children: 2, infants: 0 }));
  assert.throws(() => calculateBookingQuote(altun!, { adults: 1, children: 0, infants: 1 }));
});

test("max 10 guests; zero party rejected", () => {
  for (const product of [cave!, turtle!, altun!]) {
    assert.equal(product.capacity.maxGuestsPerBooking, 10);
    assert.doesNotThrow(() => calculateBookingQuote(product, { adults: 10, children: 0, infants: 0 }));
    assert.throws(() => calculateBookingQuote(product, { adults: 11, children: 0, infants: 0 }));
    assert.throws(() => calculateBookingQuote(product, { adults: 0, children: 0, infants: 0 }));
  }
  assert.doesNotThrow(() => calculateBookingQuote(turtle!, { adults: 5, children: 5, infants: 0 }));
  assert.throws(() => calculateBookingQuote(turtle!, { adults: 5, children: 6, infants: 0 }));
});

test("client total must match server quote", () => {
  const quote = calculateBookingQuote(cave!, { adults: 2, children: 0, infants: 0 });
  assert.doesNotThrow(() => assertClientTotalMatches(quote, 17200));
  assert.throws(() => assertClientTotalMatches(quote, 1));
});

test("payment success status is requested not confirmed", () => {
  assert.equal(statusAfterPaymentSuccess("request"), "requested");
});

test("booking references use Belize W2BZE prefix", () => {
  assert.match(createBookingReference(belizeBookingCore), /^W2BZE-/);
  assert.equal(belizeBookingCore.bookingRefPrefix, "W2BZE");
});

test("customer and cruise validation", () => {
  assert.equal(
    validateCustomer({ name: "Alex Traveller", email: "alex@example.com", phone: "+447700900123" }),
    null,
  );
  assert.ok(validateCustomer({ name: "A", email: "x", phone: "1" }));
  assert.ok(validateCustomer({ name: "Alex Traveller", email: "bad", phone: "+447700900123" }));
  assert.ok(
    validateCruise({
      date: "nope",
      shipName: "Ship",
      shipSlug: "s",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    }),
  );
  assert.equal(
    validateCruise({
      date: "2026-12-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    }),
    null,
  );
});

test("14-day cancellation copy", () => {
  assert.match(BELIZE_CANCELLATION_COPY.customerCancellation, /14 days/);
  assert.doesNotMatch(BELIZE_CANCELLATION_COPY.customerCancellation, /7 days/);
  assert.match(BELIZE_CANCELLATION_COPY.unableToConfirm, /full refund/i);
});

test("customer requested email is not confirmation", () => {
  const email = requestedCustomerEmail({
    reference: "W2BZE-TESTREF1",
    product: cave!,
    cruise: {
      date: "2026-12-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    },
    guests: { adults: 2, children: 0, infants: 0 },
    amountLabel: "USD $172",
    customerName: "Alex",
    brand,
  });
  assert.match(email.subject, /request/i);
  assert.doesNotMatch(email.subject, /confirmed/i);
  const body = email.bodyLines.join("\n");
  assert.match(body, /not confirmed/i);
  assert.doesNotMatch(body, /\bSEG\b|CABZTUBE|Shore Excursions Group/i);
});

test("ops request email includes product and contact", () => {
  const email = supplierRequestEmail({
    reference: "W2BZE-TESTREF1",
    product: cave!,
    cruise: {
      date: "2026-12-15",
      shipName: "Celebrity Beyond",
      shipSlug: "not-listed",
      cruiseLine: "",
      isCustomShip: true,
      scheduleMatched: false,
    },
    guests: { adults: 2, children: 0, infants: 0 },
    customer: { name: "Alex Traveller", email: "alex@example.com", phone: "+447700900123" },
    amountLabel: "USD $172",
    operationalNotes: "Eligibility acknowledged",
    destinationLabel: "Belize Shore Excursions — new booking request",
  });
  assert.match(email.subject, /W2BZE-TESTREF1/);
  assert.match(email.shell.destinationLabel, /Belize/i);
});

test("request mode for all three products", () => {
  for (const product of BELIZE_BOOKING_PRODUCTS) {
    assert.equal(product.bookingMode, "request");
    assert.equal(product.availability, "live");
    assert.equal(product.pricing.currency, "USD");
  }
});
