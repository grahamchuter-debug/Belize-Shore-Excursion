/**
 * Belize booking security / commercial gate tests (Phase 13D).
 * No live Stripe. Uses Worker preview mode + shared pricing authority.
 */
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";
import worker from "./index";
import { LIVE_PAYMENTS_CODE_ENABLED, liveCheckoutBlock, bookingsAreEnabled } from "./live-gate";
import { assertStripeTestSecret, StripeModeError } from "./stripe-guard";
import { findBelizeBookingProduct, BELIZE_BOOKING_PRODUCTS } from "../../../shared/destinations/belize-products";
import {
  assertClientTotalMatches,
  calculateBookingQuote,
  statusAfterPaymentSuccess,
  validateCruise,
  validateCustomer,
} from "../../../shared/world-booking";

const previewEnv = {
  PAYMENTS_MODE: "preview",
  BOOKINGS_ENABLED: "true",
  CORS_ALLOWED_ORIGINS: "http://localhost:8908",
  SITE_BASE_URL: "http://localhost:8908",
} as unknown as Env;

function payload(
  sessionId: string,
  guests = { adults: 2, children: 0, infants: 0 },
  overrides: Record<string, unknown> = {},
  productId = "belize-cave-tubing",
) {
  const product = findBelizeBookingProduct(productId)!;
  const quote = calculateBookingQuote(product, guests);
  return {
    productId,
    bookingSessionId: sessionId,
    guests,
    customer: { name: "Alex Traveller", email: "alex@example.com", phone: "+447700900123" },
    cruise: {
      date: "2026-12-15",
      shipName: "Celebrity Beyond",
      shipSlug: "celebrity-beyond",
      cruiseLine: "Celebrity Cruises",
      isCustomShip: true,
      scheduleMatched: false,
    },
    confirmationAcknowledged: true,
    eligibilityAcknowledged: productId === "belize-cave-tubing" ? true : undefined,
    clientDisplayedTotalCents: quote.amountCents,
    ...overrides,
  };
}

function jsonReq(url: string, body: unknown) {
  return new Request(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });
}

test("LIVE_PAYMENTS_CODE_ENABLED is false for Belize Phase 13D (locked)", () => {
  assert.equal(LIVE_PAYMENTS_CODE_ENABLED, false);
});

test("live checkout blocked while code flag is false", () => {
  const product = findBelizeBookingProduct("belize-cave-tubing")!;
  const block = liveCheckoutBlock(
    {
      PAYMENTS_MODE: "live",
      LIVE_PAYMENTS_UNLOCK: "BELIZE_LIVE_UNLOCK",
      BOOKINGS_ENABLED: "true",
      STRIPE_SECRET_KEY: "sk_live_fake",
      STRIPE_WEBHOOK_SECRET: "whsec_fake",
      SITE_BASE_URL: "https://belizeshoreexcursion.com",
      DB: {} as D1Database,
    },
    product,
  );
  assert.ok(block);
  assert.equal(block!.code, "LIVE_PAYMENTS_BLOCKED");
});

test("BOOKINGS_ENABLED=false kill switch", () => {
  assert.equal(bookingsAreEnabled({ BOOKINGS_ENABLED: "false" }), false);
});

test("all three products live request mode with USD currency", () => {
  for (const product of BELIZE_BOOKING_PRODUCTS) {
    assert.equal(product.availability, "live");
    assert.equal(product.bookingMode, "request");
    assert.equal(product.pricing.currency, "USD");
    assert.equal(product.capacity.maxGuestsPerBooking, 10);
  }
});

test("Cave tubing 8600 cents flat", () => {
  const product = findBelizeBookingProduct("belize-cave-tubing")!;
  assert.equal(Math.round((product.pricing.pricePerGuest ?? product.pricing.adultAmount) * 100), 8600);
  assert.equal(calculateBookingQuote(product, { adults: 1, children: 0, infants: 0 }).amountCents, 8600);
});

test("Turtle adult 11500 + child 8500", () => {
  const product = findBelizeBookingProduct("turtle-snorkel-and-island-time")!;
  assert.equal(calculateBookingQuote(product, { adults: 1, children: 0, infants: 0 }).amountCents, 11500);
  assert.equal(calculateBookingQuote(product, { adults: 1, children: 1, infants: 0 }).amountCents, 20000);
});

test("Altun adult 8900 + child 7900", () => {
  const product = findBelizeBookingProduct("altun-ha-and-belize-city-overview")!;
  assert.equal(calculateBookingQuote(product, { adults: 1, children: 0, infants: 0 }).amountCents, 8900);
  assert.equal(calculateBookingQuote(product, { adults: 1, children: 1, infants: 0 }).amountCents, 16800);
});

test("zero-adult booking rejected for adult/child products", () => {
  for (const id of ["turtle-snorkel-and-island-time", "altun-ha-and-belize-city-overview"]) {
    const product = findBelizeBookingProduct(id)!;
    assert.throws(() => calculateBookingQuote(product, { adults: 0, children: 1, infants: 0 }));
  }
});

test("max 10 guests ok; 11 guests rejected", () => {
  const product = findBelizeBookingProduct("belize-cave-tubing")!;
  assert.doesNotThrow(() => calculateBookingQuote(product, { adults: 10, children: 0, infants: 0 }));
  assert.throws(() => calculateBookingQuote(product, { adults: 11, children: 0, infants: 0 }));
});

test("preview Worker records requested booking (payment ≠ confirmed)", async () => {
  const sessionId = `bz-sess-${Date.now()}`;
  const first = await worker.fetch(
    jsonReq("http://bookings.test/api/bookings/request", payload(sessionId, { adults: 2, children: 0, infants: 0 })),
    previewEnv,
  );
  const firstJson = (await first.json()) as { ok: boolean; status: string; reference: string };
  assert.equal(firstJson.ok, true);
  assert.equal(firstJson.status, "requested");
  assert.equal(statusAfterPaymentSuccess("request"), "requested");
  assert.match(firstJson.reference, /^W2BZE-/);
});

test("turtle and altun also requestable in preview", async () => {
  for (const productId of ["turtle-snorkel-and-island-time", "altun-ha-and-belize-city-overview"] as const) {
    const guests = { adults: 1, children: 1, infants: 0 };
    const res = await worker.fetch(
      jsonReq("http://bookings.test/api/bookings/request", payload(`bz-${productId}-${Date.now()}`, guests, {}, productId)),
      previewEnv,
    );
    const data = (await res.json()) as { ok: boolean; status: string };
    assert.equal(data.ok, true, productId);
    assert.equal(data.status, "requested", productId);
  }
});

test("client price tampering rejected", async () => {
  const tampered = payload(`tamper-${Date.now()}`, { adults: 2, children: 0, infants: 0 }, { clientDisplayedTotalCents: 1 });
  const response = await worker.fetch(jsonReq("http://bookings.test/api/bookings/request", tampered), previewEnv);
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(data.ok, false);
  assert.equal(data.code, "PRICE");
});

test("unknown product rejected", async () => {
  const bad = payload(`unk-${Date.now()}`, { adults: 1, children: 0, infants: 0 }, { productId: "not-a-belize-product" });
  const response = await worker.fetch(jsonReq("http://bookings.test/api/bookings/request", bad), previewEnv);
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(data.ok, false);
  assert.equal(data.code, "UNKNOWN_PRODUCT");
});

test("missing consent rejected", async () => {
  const body = payload(`consent-${Date.now()}`, { adults: 1, children: 0, infants: 0 }, { confirmationAcknowledged: false });
  const response = await worker.fetch(jsonReq("http://bookings.test/api/bookings/request", body), previewEnv);
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(data.ok, false);
  assert.equal(data.code, "CONSENT");
});

test("invalid email / date / missing fields", () => {
  const product = findBelizeBookingProduct("belize-cave-tubing")!;
  assert.throws(() => calculateBookingQuote(product, { adults: 0, children: 0, infants: 0 }));
  assert.ok(validateCruise({ date: "nope", shipName: "Ship", shipSlug: "s", cruiseLine: "", isCustomShip: true, scheduleMatched: false }));
  assert.ok(validateCruise({ date: "2020-01-01", shipName: "Ship", shipSlug: "s", cruiseLine: "", isCustomShip: true, scheduleMatched: false }));
  assert.ok(validateCustomer({ name: "Alex Traveller", email: "bad", phone: "+447700900123" }));
  assert.equal(validateCustomer({ name: "Alex Traveller", email: "alex@example.com", phone: "+447700900123" }), null);
});

test("ops request heading is Belize not St Lucia", () => {
  const src = readFileSync(new URL("./notify.ts", import.meta.url), "utf8");
  assert.match(src, /NEW BELIZE BOOKING REQUEST/);
  assert.doesNotMatch(src, /NEW ST LUCIA BOOKING REQUEST/);
});

test("missing customer fields rejected by preview Worker", async () => {
  const body = payload(`miss-${Date.now()}`, { adults: 1, children: 0, infants: 0 }, {
    customer: { name: "", email: "alex@example.com", phone: "+447700900123" },
  });
  const response = await worker.fetch(jsonReq("http://bookings.test/api/bookings/request", body), previewEnv);
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(data.ok, false);
  assert.equal(data.code, "CUSTOMER");
});

test("assertClientTotalMatches rejects mismatch", () => {
  const product = findBelizeBookingProduct("belize-cave-tubing")!;
  const quote = calculateBookingQuote(product, { adults: 2, children: 0, infants: 0 });
  assert.throws(() => assertClientTotalMatches(quote, quote.amountCents - 100));
});

test("assertStripeTestSecret rejects live keys", () => {
  assert.equal(assertStripeTestSecret("sk_test_abc123"), "sk_test_abc123");
  assert.throws(
    () => assertStripeTestSecret("sk_live_abc123"),
    (error: unknown) => error instanceof StripeModeError && error.code === "LIVE_KEY_REJECTED",
  );
});

test("checkout kill switch returns BOOKINGS_DISABLED", async () => {
  const env = { ...previewEnv, PAYMENTS_MODE: "test", BOOKINGS_ENABLED: "false", STRIPE_SECRET_KEY: "sk_test_x" } as unknown as Env;
  const response = await worker.fetch(jsonReq("http://bookings.test/api/bookings/checkout", payload(`kill-${Date.now()}`)), env);
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(data.ok, false);
  assert.equal(data.code, "BOOKINGS_DISABLED");
});

test("bad webhook signature rejected (missing header)", async () => {
  const env = {
    PAYMENTS_MODE: "test",
    STRIPE_SECRET_KEY: "sk_test_abc",
    STRIPE_WEBHOOK_SECRET: "whsec_test",
    BOOKINGS_ENABLED: "true",
  } as unknown as Env;
  const response = await worker.fetch(
    new Request("http://bookings.test/api/stripe/webhook", { method: "POST", body: "{}" }),
    env,
  );
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(response.status, 400);
  assert.equal(data.code, "SIGNATURE");
});

test("bad webhook signature rejected (invalid signature)", async () => {
  const env = {
    PAYMENTS_MODE: "test",
    STRIPE_SECRET_KEY: "sk_test_abc",
    STRIPE_WEBHOOK_SECRET: "whsec_test",
    BOOKINGS_ENABLED: "true",
  } as unknown as Env;
  const response = await worker.fetch(
    new Request("http://bookings.test/api/stripe/webhook", {
      method: "POST",
      headers: { "Stripe-Signature": "t=1,v1=deadbeef" },
      body: '{"id":"evt_test"}',
    }),
    env,
  );
  const data = (await response.json()) as { ok: boolean; code: string };
  assert.equal(response.status, 400);
  assert.equal(data.code, "SIGNATURE");
});

test("TEST_ONLY_EMAIL_OVERRIDE applies only in PAYMENTS_MODE=test", async () => {
  const { resolveOutboundRecipient } = await import("./email");
  const intended = "synthetic.customer@example.com";
  const override = "info@wowatour.com";

  const inTest = resolveOutboundRecipient(
    { PAYMENTS_MODE: "test", TEST_ONLY_EMAIL_OVERRIDE: override },
    intended,
  );
  assert.equal(inTest.to, override);
  assert.equal(inTest.overridden, true);

  const inLive = resolveOutboundRecipient(
    { PAYMENTS_MODE: "live", TEST_ONLY_EMAIL_OVERRIDE: override },
    intended,
  );
  assert.equal(inLive.to, intended);
  assert.equal(inLive.overridden, false);

  const inPreview = resolveOutboundRecipient(
    { PAYMENTS_MODE: "preview", TEST_ONLY_EMAIL_OVERRIDE: override },
    intended,
  );
  assert.equal(inPreview.to, intended);
  assert.equal(inPreview.overridden, false);

  const noOverride = resolveOutboundRecipient({ PAYMENTS_MODE: "test" }, intended);
  assert.equal(noOverride.to, intended);
  assert.equal(noOverride.overridden, false);
});

test("Stripe Link disabled at Belize session level (checkout source)", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const src = readFileSync(join(here, "routes/checkout.ts"), "utf8");
  assert.match(src, /payment_method_types:\s*\[\s*["']card["']\s*\]/);
  assert.match(src, /wallet_options:\s*\{[\s\S]*link:\s*\{\s*display:\s*["']never["']/);
});

test("public HTML/JS leak scan — no SEG / internal codes in site assets", () => {
  const root = join(dirname(fileURLToPath(import.meta.url)), "../../..");
  const paths = [
    "js/commercial-config.js",
    "js/booking.js",
    "js/booking-received.js",
    "belize-cave-tubing.html",
    "turtle-snorkel-and-island-time.html",
    "altun-ha-and-belize-city-overview.html",
    "book/belize-cave-tubing/index.html",
    "book/turtle-snorkel-and-island-time/index.html",
    "book/altun-ha-and-belize-city-overview/index.html",
  ];
  const banned = /\bSEG\b|Shore Excursions Group|CABZTUBE|CABZTURTLE|CABZALTUN|SEG_MANUAL|shoreexcursionsgroup/i;
  for (const rel of paths) {
    const full = join(root, rel);
    try {
      const text = readFileSync(full, "utf8");
      assert.doesNotMatch(text, banned, rel);
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code === "ENOENT") continue;
      throw err;
    }
  }
});

test("internal product notes keep SEG_MANUAL codes off public paths", () => {
  for (const product of BELIZE_BOOKING_PRODUCTS) {
    const notes = (product.supplierReferenceNotes || []).join("\n");
    assert.match(notes, /SEG_MANUAL/);
    assert.doesNotMatch(product.productPath, /SEG|CABZ/i);
    assert.doesNotMatch(product.bookingPath, /SEG|CABZ/i);
  }
});

test("production gates remain locked in live-gate source", () => {
  const here = dirname(fileURLToPath(import.meta.url));
  const src = readFileSync(join(here, "live-gate.ts"), "utf8");
  assert.match(src, /LIVE_PAYMENTS_CODE_ENABLED\s*=\s*false/);
});

test("commercial-config defaults to PRODUCTION_READY_LOCKED", () => {
  const root = join(dirname(fileURLToPath(import.meta.url)), "../../..");
  const text = readFileSync(join(root, "js/commercial-config.js"), "utf8");
  assert.match(text, /defaultPublicBookingStatus:\s*"PRODUCTION_READY_LOCKED"/);
  assert.match(text, /publicBookingStatus:\s*"PRODUCTION_READY_LOCKED"/);
  assert.doesNotMatch(text, /CABZTUBE|CABZTURTLE|CABZALTUN|SEG_MANUAL|\bSEG\b/);
});
