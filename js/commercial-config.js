/**
 * Public commercial status for Belize Shore Excursion (Phase 13D).
 * INTERNAL supply refs must never be rendered on customer pages.
 *
 * Gate values:
 * - PRODUCTION_READY_LOCKED — journey visible; live Pay & request disabled
 * - BOOKING_ENABLED — live checkout allowed (requires Worker LIVE unlock too)
 */
window.BZ_COMMERCIAL = {
  bookingsApiUrl: "https://belize-bookings-prod.dark-violet-8d91.workers.dev",
  email: "hello@belizeshoreexcursion.com",
  siteName: "Belize Shore Excursions",
  /** Phase 13G — Graham-authorised live request-to-book unlock. */
  defaultPublicBookingStatus: "BOOKING_ENABLED",
  cancellation:
    "Free cancellation up to 14 days before your excursion. Cancellations made within 14 days of departure are non-refundable. If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.",
  paymentNotConfirmation:
    "After payment, we'll arrange your excursion and send your confirmation as soon as it is confirmed. Payment does not mean the excursion is confirmed yet.",
  unableToConfirm:
    "If we are unable to confirm your excursion after payment, you will receive a full refund to your original payment method.",
  meetingInstructions:
    "Meeting instructions will be provided with your confirmed excursion details.",
  overTenGuidance:
    "For groups larger than 10, email hello@belizeshoreexcursion.com before requesting.",
  products: {
    "belize-cave-tubing": {
      productId: "belize-cave-tubing",
      slug: "belize-cave-tubing",
      name: "Belize Cave Tubing",
      shortTitle: "Belize Cave Tubing",
      productPath: "/belize-cave-tubing.html",
      bookingPath: "/book/belize-cave-tubing/",
      receivedPath: "/book/belize-cave-tubing/received/",
      adultUsd: 86,
      childUsd: null,
      infantUsd: null,
      guestModel: "flat_guest",
      durationLabel: "About 5 hours",
      maxGuests: 10,
      requiresEligibilityAck: true,
      publicBookingStatus: "BOOKING_ENABLED",
      displayPrice: "$86 per eligible guest",
    },
    "turtle-snorkel-and-island-time": {
      productId: "turtle-snorkel-and-island-time",
      slug: "turtle-snorkel-and-island-time",
      name: "Turtle Snorkel and Island Time",
      shortTitle: "Turtle Snorkel and Island Time",
      productPath: "/turtle-snorkel-and-island-time.html",
      bookingPath: "/book/turtle-snorkel-and-island-time/",
      receivedPath: "/book/turtle-snorkel-and-island-time/received/",
      adultUsd: 115,
      childUsd: 85,
      infantUsd: null,
      guestModel: "adult_child",
      durationLabel: "About 5 hours",
      maxGuests: 10,
      publicBookingStatus: "BOOKING_ENABLED",
      displayPrice: "Adults (12+) $115 · Children (6–11) $85",
    },
    "altun-ha-and-belize-city-overview": {
      productId: "altun-ha-and-belize-city-overview",
      slug: "altun-ha-and-belize-city-overview",
      name: "Altun-Ha and Belize City Overview",
      shortTitle: "Altun-Ha and Belize City Overview",
      productPath: "/altun-ha-and-belize-city-overview.html",
      bookingPath: "/book/altun-ha-and-belize-city-overview/",
      receivedPath: "/book/altun-ha-and-belize-city-overview/received/",
      adultUsd: 89,
      childUsd: 79,
      infantUsd: null,
      guestModel: "adult_child",
      durationLabel: "About 4 hours",
      maxGuests: 10,
      publicBookingStatus: "BOOKING_ENABLED",
      displayPrice: "Adults (11+) $89 · Children (4–10) $79",
    },
  },
};
