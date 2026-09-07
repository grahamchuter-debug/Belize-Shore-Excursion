/**
 * Belize request-to-book form (Phase 13D).
 * Server-side pricing is authoritative — client total is for review only.
 * Public gate: PRODUCTION_READY_LOCKED blocks Pay & request (no live money).
 */
(function () {
  const form = document.getElementById("bz-booking-form");
  if (!form || !window.BZ_COMMERCIAL) return;

  const cfg = window.BZ_COMMERCIAL;
  const productId = form.dataset.productId || "";
  const product = cfg.products[productId];
  if (!product) return;

  const adultRate = Number(product.adultUsd || 0);
  const childRate = product.childUsd == null ? null : Number(product.childUsd);
  const max = Number(product.maxGuests || 10);
  const guestModel = product.guestModel || "adult_child";
  const status = product.publicBookingStatus || cfg.defaultPublicBookingStatus;
  const live = status === "BOOKING_ENABLED";
  const apiUrl = String(cfg.bookingsApiUrl || "").replace(/\/$/, "");
  const errEl = document.getElementById("booking-error");
  const submitBtn = document.getElementById("booking-submit");
  const lockedBtn = document.getElementById("booking-submit-locked");
  const ackEl = document.getElementById("booking_ack");
  const eligibilityEl = document.getElementById("booking_eligibility");

  form.dataset.live = live ? "1" : "0";
  const statusTitle = document.getElementById("booking-status-title");
  const statusBody = document.getElementById("booking-status-body");
  const footerNote = document.getElementById("booking-footer-note");

  function setControlVisible(el, visible) {
    if (!el) return;
    el.hidden = !visible;
    el.classList.toggle("hidden", !visible);
    el.setAttribute("aria-hidden", visible ? "false" : "true");
    if (!visible) el.style.display = "none";
    else el.style.removeProperty("display");
  }

  if (live) {
    if (lockedBtn) lockedBtn.remove();
    setControlVisible(submitBtn, true);
    if (ackEl) ackEl.disabled = false;
    if (eligibilityEl) eligibilityEl.disabled = false;
    if (statusTitle) statusTitle.textContent = "Book with confidence";
    if (statusBody) {
      statusBody.textContent =
        "Pay securely online to request your excursion. We'll confirm your places separately by email. If we're unable to confirm your excursion, you'll receive a full refund.";
    }
    if (footerNote) {
      footerNote.innerHTML =
        'Secure card payment via Stripe. Prefer to ask first? <a href="mailto:' +
        cfg.email +
        '">' +
        cfg.email +
        "</a>";
    }
  } else {
    setControlVisible(lockedBtn, true);
    setControlVisible(submitBtn, false);
    if (ackEl) ackEl.disabled = true;
    if (eligibilityEl) eligibilityEl.disabled = true;
    if (statusTitle) statusTitle.textContent = "Online checkout is prepared and locked.";
    if (statusBody) {
      statusBody.textContent =
        "Payment receives your request — it does not confirm the excursion. Confirmation is emailed after we arrange your places. If we cannot confirm, the payment is refunded in full to your original payment method. Live card payments are not enabled yet.";
    }
    if (footerNote) {
      footerNote.innerHTML =
        'Live payments remain locked on this product. Prefer to ask first? <a href="mailto:' +
        cfg.email +
        '">' +
        cfg.email +
        "</a>";
    }
  }

  function num(id, fallback) {
    const el = document.getElementById(id);
    return el ? Math.max(0, parseInt(el.value || String(fallback), 10) || 0) : fallback;
  }

  function refresh() {
    const adults = num("adults", guestModel === "flat_guest" ? 2 : 1);
    const children = guestModel === "adult_child" ? num("children", 0) : 0;
    const dateEl = document.getElementById("cruise_date");
    const shipEl = document.getElementById("ship_name");
    const set = (id, text) => {
      const n = document.getElementById(id);
      if (n) n.textContent = text;
    };
    set("rev-date", dateEl && dateEl.value ? dateEl.value : "—");
    set("rev-ship", shipEl && shipEl.value.trim() ? shipEl.value.trim() : "—");

    const childrenRow = document.getElementById("rev-children-row");
    if (guestModel === "flat_guest") {
      set("rev-adults", adults + " × $" + adultRate);
      if (childrenRow) childrenRow.hidden = true;
      const totalGuests = adults;
      const total = adults * adultRate;
      if (totalGuests > max) set("rev-total", "Too many guests (max " + max + ")");
      else set("rev-total", "USD $" + total);
      return { adults: adults, children: 0, totalGuests: totalGuests, totalCents: total * 100 };
    }

    set("rev-adults", adults + " × $" + adultRate);
    if (childrenRow) childrenRow.hidden = false;
    set("rev-children", children + " × $" + (childRate == null ? 0 : childRate));
    const totalGuests = adults + children;
    const total = adults * adultRate + children * (childRate || 0);
    if (totalGuests > max) set("rev-total", "Too many guests (max " + max + ")");
    else set("rev-total", "USD $" + total);
    return { adults: adults, children: children, totalGuests: totalGuests, totalCents: total * 100 };
  }

  function showError(msg) {
    if (!errEl) return;
    errEl.hidden = !msg;
    errEl.textContent = msg || "";
  }

  function sessionId() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    return "bz-" + Date.now() + "-" + Math.random().toString(36).slice(2, 10);
  }

  const cruiseDateInput = document.getElementById("cruise_date");
  if (cruiseDateInput) {
    const dateField = cruiseDateInput.closest("label") || cruiseDateInput;
    dateField.addEventListener("pointerdown", function (event) {
      if (event.button !== 0) return;
      try {
        if (typeof cruiseDateInput.showPicker === "function") cruiseDateInput.showPicker();
      } catch (_) {
        /* ignore */
      }
    });
  }

  form.addEventListener("input", refresh);
  form.addEventListener("change", refresh);
  refresh();

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    showError("");
    if (!live || !apiUrl || !productId) {
      showError(
        "Online checkout is prepared and locked. Live payment is not open yet. Email " + cfg.email + " if you need help.",
      );
      return;
    }

    const adults = num("adults", guestModel === "flat_guest" ? 1 : 1);
    const children = guestModel === "adult_child" ? num("children", 0) : 0;
    const totalGuests = adults + children;

    if (guestModel !== "flat_guest" && adults < 1) {
      showError("Please include at least one adult.");
      return;
    }
    if (totalGuests < 1 || totalGuests > max) {
      showError("Please choose between 1 and " + max + " guests. For larger groups, email " + cfg.email + ".");
      return;
    }

    const cruiseDate = (document.getElementById("cruise_date") || {}).value || "";
    const shipName = ((document.getElementById("ship_name") || {}).value || "").trim();
    const name = ((document.getElementById("lead_name") || {}).value || "").trim();
    const email = ((document.getElementById("lead_email") || {}).value || "").trim();
    const phone = ((document.getElementById("lead_phone") || {}).value || "").trim();
    const mobility = ((document.getElementById("mobility") || {}).value || "").trim();
    const special = ((document.getElementById("special_requirements") || {}).value || "").trim();

    if (!cruiseDate || !shipName || !name || !email || !phone) {
      showError("Please complete date, ship, and lead passenger details.");
      return;
    }
    if (!ackEl || !ackEl.checked) {
      showError("Please acknowledge that payment receives a request, not confirmation.");
      return;
    }
    if (product.requiresEligibilityAck && (!eligibilityEl || !eligibilityEl.checked)) {
      showError("Please confirm all participants meet the age and height requirements.");
      return;
    }

    const notes = [];
    if (mobility) notes.push("Mobility: " + mobility);
    if (special) notes.push("Special requirements: " + special);
    if (product.requiresEligibilityAck) {
      notes.push("Eligibility acknowledged: all participants ≥8 years and ≥48 inches tall");
    }

    const totalCents =
      guestModel === "flat_guest"
        ? adults * adultRate * 100
        : adults * adultRate * 100 + children * (childRate || 0) * 100;

    const payload = {
      productId: product.productId,
      bookingSessionId: sessionId(),
      guests: { adults: adults, children: children, infants: 0 },
      customer: {
        name: name,
        email: email,
        phone: phone,
        operationalNotes: notes.length ? notes.join(" | ") : undefined,
      },
      cruise: {
        date: cruiseDate,
        shipName: shipName,
        shipSlug: "not-listed",
        cruiseLine: "",
        isCustomShip: true,
        scheduleMatched: false,
      },
      confirmationAcknowledged: true,
      eligibilityAcknowledged: product.requiresEligibilityAck ? true : undefined,
      clientDisplayedTotalCents: totalCents,
    };

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "Connecting to secure checkout…";
    }

    try {
      const res = await fetch(apiUrl + "/api/bookings/checkout", {
        method: "POST",
        headers: { "content-type": "application/json", accept: "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await res.json().catch(function () {
        return {};
      });
      if (!res.ok || !data.ok) {
        showError((data && data.message) || "Checkout could not start. No payment was taken.");
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Pay & request";
        }
        return;
      }
      const checkoutUrl = data.checkoutUrl || data.url;
      if (!checkoutUrl) {
        showError("Checkout URL missing. No payment was taken.");
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Pay & request";
        }
        return;
      }
      window.location.assign(checkoutUrl);
    } catch (_) {
      showError("Network error starting checkout. No payment was taken.");
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Pay & request";
      }
    }
  });
})();
