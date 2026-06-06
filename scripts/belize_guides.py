"""Guide and home page content for Belize Shore Excursion."""
from belize_config import (
    ALTUN_HA_ALT,
    ALTUN_HA_IMG,
    BEACH_ALT,
    BEACH_IMG,
    BEST_ALT,
    BEST_IMG,
    CAVE_ALT,
    CAVE_IMG,
    FAQ_ALT,
    FAQ_IMG,
    INTRO_ALT,
    INTRO_IMG,
    LAMANAI_ALT,
    LAMANAI_IMG,
    ONE_DAY_ALT,
    ONE_DAY_IMG,
    PORT_ARRIVAL_ALT,
    PORT_ARRIVAL_IMG,
    PORT_ALT,
    PORT_IMG,
    PRIVATE_ALT,
    PRIVATE_IMG,
    SNORKEL_ALT,
    SNORKEL_IMG,
)
from belize_helpers import card_grid, comparison_section, internal_links, snapshot_default
from belize_tours import comparison_rows
from belize_tours_data import FEATURED_TOURS, TOURS


def _featured_cards() -> str:
    cards = []
    for slug in FEATURED_TOURS:
        t = next(x for x in TOURS if x["slug"] == slug)
        from belize_config import CATEGORY_IMAGES
        img, alt = CATEGORY_IMAGES.get(t["category"], (INTRO_IMG, INTRO_ALT))
        cards.append((
            img, alt, t["title"], t["seg_desc"][:120] + "…",
            f"{slug}.html", "View Tour",
        ))
    return card_grid(cards[:4])


def content_home() -> str:
    best_cards = card_grid([
        (CAVE_IMG, CAVE_ALT, "Cave Tubing", "Belize's signature underground river float through Mayan ceremonial caves.", "belize-cave-tubing.html", "Cave Tubing"),
        (ALTUN_HA_IMG, ALTUN_HA_ALT, "Altun Ha Ruins", "Climb Mayan temples dating to 200 BC — Belize's most accessible ruins site.", "altun-ha-and-belize-city-overview.html", "Altun Ha"),
        (SNORKEL_IMG, SNORKEL_ALT, "Reef Snorkel", "Turtles, rays and clear water at the Belize Barrier Reef and Caye Caulker.", "turtle-snorkel-and-island-time.html", "Snorkel"),
        (BEACH_IMG, BEACH_ALT, "Beach Break", "Shark Ray Alley and laid-back island time on Caye Caulker.", "shark-ray-alley-and-caye-caulker-beach-break.html", "Beach"),
    ])
    featured = _featured_cards()
    snap = snapshot_default()
    return f"""<section class="pt-8 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-10">
    <div class="section-label mx-auto">Best Excursions</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-4">Best Belize Shore Excursions</h2>
    <p class="text-gray-600 text-sm max-w-2xl mx-auto">Ranked for cruise schedules — cave tubing, Mayan ruins, barrier reef snorkelling and beach breaks from Belize City's tender port.</p>
  </div>
  {best_cards}
  <p class="text-center mt-8"><a href="best-belize-shore-excursions.html" class="text-ocean-600 font-semibold text-sm">See full comparison →</a></p>
</div></section>
<section class="pt-4 pb-8 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <div class="inline-flex items-center gap-2 text-ocean-600 text-xs font-semibold tracking-widest uppercase mb-3"><div class="w-8 h-px bg-ocean-400"></div>Belize City Cruise Port</div>
    <h2 class="text-3xl sm:text-4xl font-display font-bold text-gray-900 mb-5">Why Cruise Passengers<br/><span class="text-ocean-600">Choose Belize</span></h2>
    <p class="text-gray-600 leading-relaxed mb-5">Belize puts dense rainforest, ancient Mayan temples and the <strong>second-largest barrier reef</strong> in the world within reach on a typical <strong>6–10 hour</strong> tender port call. Belize dollars (BZD) are official; <strong>USD</strong> is widely accepted at a fixed 2:1 rate near the cruise port.</p>
    <a href="belize-cruise-port-guide.html" class="btn-ocean inline-flex items-center gap-2 text-white font-semibold px-7 py-3.5 rounded-full text-sm shadow-lg">Port Guide</a>
  </div>
  <div class="info-image rounded-3xl aspect-[4/3] shadow-2xl overflow-hidden">
    <img src="{INTRO_IMG}" alt="{INTRO_ALT}" width="800" height="600" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 bg-amber-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div class="text-center mb-12"><h2 class="text-3xl font-display font-bold text-gray-900">Featured Excursions</h2>
  <p class="text-gray-600 text-sm mt-3 max-w-xl mx-auto">Most-booked shore excursions for Belize cruise passengers from Belize City.</p></div>
  {featured}
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-10">Top Things To Do In Belize</h2>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Cave Tubing</h3><p class="text-gray-600">Float through underground rivers in caves the Mayans used for ceremonies — Belize's signature adventure.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Altun Ha</h3><p class="text-gray-600">Mayan ruins dating to 200 BC with climbable temples about one hour inland from the cruise port.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Barrier Reef Snorkel</h3><p class="text-gray-600">Caye Caulker, Hol Chan and Shark Ray Alley — turtles, rays and nurse sharks in clear Caribbean water.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Lamanai</h3><p class="text-gray-600">River boat to one of Belize's largest Mayan sites — howler monkeys and jungle temples combined.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Belize Zoo</h3><p class="text-gray-600">Rescue-centre wildlife encounters with jaguars, tapirs and howler monkeys — family-friendly from port.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Jungle Jeep Tours</h3><p class="text-gray-600">Off-road adventures through rainforest, caves and countryside with cruise-timed returns.</p></div>
  </div>
</div></section>
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{CAVE_IMG}" alt="{CAVE_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
  <div>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Cave Tubing &amp; Rainforest Adventures</h2>
    <p class="text-gray-600 leading-relaxed mb-4">Belize invented the cave tubing experience — float on inner tubes through limestone cave systems that once served as Mayan ceremonial sites. Combo tours add zip lines and jungle treks for a full adventure day from the cruise port.</p>
    <p class="text-gray-600 leading-relaxed mb-5">Compare the <a href="cave-tubing-and-zip-line-combo.html" class="text-ocean-600 font-medium">Cave Tubing and Zip Line Combo</a> with the focused <a href="belize-cave-tubing.html" class="text-ocean-600 font-medium">Belize Cave Tubing</a> tour, or book a <a href="private-tubing-expedition.html" class="text-ocean-600 font-medium">Private Tubing Expedition</a> for your group.</p>
    <a href="belize-cave-tubing.html" class="text-ocean-600 font-semibold text-sm">Cave tubing excursions →</a>
  </div>
</div></div></section>
<section class="py-16 bg-sand-50"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Mayan Ruins &amp; Cultural Tours</h2>
    <p class="text-gray-600 leading-relaxed mb-4"><strong>Altun Ha</strong> sits about <strong>one hour</strong> inland from Belize City — climbable temples, jungle surroundings and the famous Jade Head discovery site. <strong>Lamanai</strong> reaches further with a scenic river boat through wildlife-rich waterways.</p>
    <p class="text-gray-600 leading-relaxed mb-5">The <a href="altun-ha-and-belize-city-overview.html" class="text-ocean-600 font-medium">Altun-Ha and Belize City Overview</a> fits most port calls. See our <a href="belize-mayan-ruins-excursions.html" class="text-ocean-600 font-medium">Mayan ruins guide</a> for distances and tour comparisons.</p>
    <a href="belize-mayan-ruins-excursions.html" class="text-ocean-600 font-semibold text-sm">Mayan ruins excursions →</a>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{ALTUN_HA_IMG}" alt="{ALTUN_HA_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-center">
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{SNORKEL_IMG}" alt="{SNORKEL_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
  <div>
    <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Snorkelling &amp; Beach Excursions</h2>
    <p class="text-gray-600 leading-relaxed mb-4">The Belize Barrier Reef sits just offshore — boat rides to <strong>Caye Caulker</strong> and <strong>Hol Chan Marine Reserve</strong> bring you face-to-face with sea turtles, sting rays and nurse sharks at Shark Ray Alley. Beach breaks add rum punch and island time.</p>
    <p class="text-gray-600 leading-relaxed mb-5">The <a href="turtle-snorkel-and-island-time.html" class="text-ocean-600 font-medium">Turtle Snorkel and Island Time</a> tour is a cruise favourite. Compare reef options in our <a href="belize-snorkeling-and-beach-excursions.html" class="text-ocean-600 font-medium">snorkel and beach guide</a>.</p>
    <a href="belize-snorkeling-and-beach-excursions.html" class="text-ocean-600 font-semibold text-sm">Snorkel &amp; beach excursions →</a>
  </div>
</div></div></section>
{comparison_section(comparison_rows())}
{home_faq_section()}
<section class="py-16 cta-gradient"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-white mb-4">Plan Your Belize Port Day</h2>
  <p class="text-white/85 text-sm mb-6">Compare excursions, read the Belize City port guide and build your itinerary before you tender ashore in Belize.</p>
  <div class="flex flex-col sm:flex-row gap-4 justify-center">
    <a href="best-belize-shore-excursions.html" class="btn-primary inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Compare Excursions</a>
    <a href="belize-cruise-port-guide.html" class="btn-outline inline-flex items-center justify-center text-white font-semibold px-8 py-4 rounded-full">Port Guide</a>
  </div>
</div></section>"""


def home_faq_section() -> str:
    return """<section class="py-16 bg-white"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-3xl font-display font-bold text-gray-900 text-center mb-8">Belize Shore Excursions FAQ</h2>
  <div class="space-y-4">
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Is Belize a tender port?</summary>
      <p class="mt-4 text-sm text-gray-500">Yes — cruise ships anchor offshore and you take a tender boat to Fort Street Tourism Village in Belize City. Build 20–30 minutes each way into your port day planning.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How far are the main attractions from the port?</summary>
      <p class="mt-4 text-sm text-gray-500">Reef and island excursions are a short boat ride. Inland sites like Altun Ha and cave tubing are about 45–90 minutes each way by road.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">What is the best excursion for first-time visitors?</summary>
      <p class="mt-4 text-sm text-gray-500">Cave tubing and Altun Ha ruins highlight Belize's two iconic experiences. Reef snorkelling at Caye Caulker is equally popular for water lovers.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">How long do cruise ships stay in Belize?</summary>
      <p class="mt-4 text-sm text-gray-500">Most Belize City port calls are 6 to 10 hours. Full-day combos like cave tubing and zip line need 5–6 hours; short city tours fit 2-hour windows.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">What currency is used in Belize?</summary>
      <p class="mt-4 text-sm text-gray-500">Belize dollars (BZD) are official, pegged 2:1 to USD. US dollars are widely accepted — carry small bills for tips and souvenirs.</p></details>
    <details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">Is Belize safe for shore excursions?</summary>
      <p class="mt-4 text-sm text-gray-500">Organised excursions with reputable operators are the standard approach. Guides handle transport, timing and return-to-ship logistics. See our <a href="belize-shore-excursions-faq.html" class="text-ocean-600">full FAQ</a>.</p></details>
  </div>
  <p class="text-center mt-8"><a href="belize-shore-excursions-faq.html" class="text-ocean-600 font-semibold text-sm">Read full FAQ →</a></p>
</div></section>"""


def home_faq_data() -> list[tuple[str, str]]:
    return [
        ("Is Belize a tender port for cruise ships?", "Yes — ships anchor offshore and passengers tender to Fort Street Tourism Village in Belize City."),
        ("How far are Mayan ruins from the Belize cruise port?", "Altun Ha is approximately one hour inland by road from Belize City."),
        ("How far is the Belize Barrier Reef from port?", "Reef and Caye Caulker excursions are a short boat ride from Belize City."),
        ("How long do cruise ships stay in Belize?", "Most port calls are 6 to 10 hours."),
        ("What currency is used in Belize?", "Belize dollars (BZD), pegged 2:1 to USD which is widely accepted."),
        ("What is the best Belize excursion for first-time visitors?", "Cave tubing, Altun Ha ruins, or barrier reef snorkelling."),
        ("Is Belize safe for cruise passengers on excursions?", "Organised shore excursions with return-to-ship guarantees are the recommended approach."),
    ]


def content_best_excursions() -> str:
    snap = snapshot_default(best_for="Comparing all excursion types", popular="See comparison table below")
    rankings = """<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Excursions by Traveler Type</h2>
  <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Families</h3><p class="text-gray-600 mb-3">Belize Zoo combos, Howler Monkey Sanctuary and easy city tours suit mixed ages.</p><a href="belize-city-and-zoo-combo.html" class="text-ocean-600 font-semibold">Zoo Combo →</a></div>
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Adventure Seekers</h3><p class="text-gray-600 mb-3">Cave tubing, zip lines and jungle Jeep tours — Belize's active port-day lineup.</p><a href="cave-tubing-and-zip-line-combo.html" class="text-ocean-600 font-semibold">Adventure Combo →</a></div>
    <div class="bg-sand-50 rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">First Timers</h3><p class="text-gray-600 mb-3">Altun Ha ruins, cave tubing or reef snorkel — Belize's three signature experiences.</p><a href="altun-ha-and-belize-city-overview.html" class="text-ocean-600 font-semibold">Altun Ha →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">Reef Lovers</h3><p class="text-gray-600 mb-3">Turtle snorkel, Shark Ray Alley and barrier reef trips to Caye Caulker.</p><a href="turtle-snorkel-and-island-time.html" class="text-ocean-600 font-semibold">Reef Snorkel →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">History Buffs</h3><p class="text-gray-600 mb-3">Altun Ha, Lamanai and Cahal Pech — Mayan archaeology from the cruise port.</p><a href="belize-mayan-ruins-excursions.html" class="text-ocean-600 font-semibold">Ruins Guide →</a></div>
    <div class="bg-ocean-50 rounded-3xl p-6 border border-ocean-100"><h3 class="font-display font-bold text-lg mb-2">Short Port Windows</h3><p class="text-gray-600 mb-3">2-hour city tours, rum factory tastings and party bus sightseeing.</p><a href="belize-city-and-rum-factory-tour.html" class="text-ocean-600 font-semibold">City Tour →</a></div>
  </div>
</div></section>"""
    cards = card_grid([
        (CAVE_IMG, CAVE_ALT, "Cave Tubing", "Underground river float through Mayan ceremonial caves.", "belize-cave-tubing.html", "Cave Tubing"),
        (ALTUN_HA_IMG, ALTUN_HA_ALT, "Altun Ha", "Mayan temples and Belize City overview.", "altun-ha-and-belize-city-overview.html", "Ruins"),
        (SNORKEL_IMG, SNORKEL_ALT, "Reef Snorkel", "Turtles and marine life at Caye Caulker.", "turtle-snorkel-and-island-time.html", "Snorkel"),
        (LAMANAI_IMG, LAMANAI_ALT, "Lamanai", "River boat to major Mayan archaeological site.", "lamanai-eco-adventure.html", "Lamanai"),
    ])
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <h2 class="text-3xl font-display font-bold text-gray-900 mb-4">Belize Shore Excursions</h2>
  <p class="text-gray-600 leading-relaxed text-sm">Operators meet at <strong>Fort Street Tourism Village</strong> after your tender ride and plan returns with buffer before all aboard on your Caribbean cruise.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
{comparison_section(comparison_rows())}
{rankings}
<section class="py-16 bg-white"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Popular Excursion Guides</h2>
  {cards}
  <div class="mt-12 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_port_guide() -> str:
    snap = snapshot_default(activity_level="Low at terminal; moderate on tours", popular="Tender boats, tour pickups, waterfront walking")
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 leading-relaxed text-sm">Cruise ships <strong>anchor offshore</strong> at Belize City — you tender to <strong>Fort Street Tourism Village</strong> on a typical <strong>6–10 hour</strong> port call.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Belize City Cruise Port Location</h2>
  <div class="info-image rounded-3xl aspect-[21/9] shadow-xl overflow-hidden mb-8 max-w-5xl mx-auto">
    <img src="{PORT_ARRIVAL_IMG}" alt="{PORT_ARRIVAL_ALT}" width="1200" height="514" loading="lazy" decoding="async" />
  </div>
  <div class="grid lg:grid-cols-3 gap-6 text-sm">
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Tender Port</h3><p class="text-gray-600">Ships do not dock at a pier — you take a tender boat to Fort Street Tourism Village. Allow 20–30 minutes each way including queues on busy ship days.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Tour Pickups</h3><p class="text-gray-600">Shore excursion operators meet inside or immediately outside the tourism village. Confirm your meeting point when booking — most tours depart within 30 minutes of tender arrival.</p></div>
    <div class="bg-white rounded-3xl p-6 border border-pr-100"><h3 class="font-display font-bold text-lg mb-2">Walking Belize City</h3><p class="text-gray-600">The tourism village has shops and facilities. Downtown Belize City landmarks are reachable on organised city tours rather than independent walking from the tender area.</p></div>
  </div>
</div></section>
<section class="py-12 bg-white"><div class="max-w-7xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Practical Port Day Info</h2>
  <div class="grid sm:grid-cols-3 gap-6 text-sm">
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Distance to Altun Ha</strong><p class="mt-2 text-gray-600">~30 miles / <strong>45–60 min</strong> inland to Mayan ruins.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Distance to Cave Tubing</strong><p class="mt-2 text-gray-600">~45–60 min into the rainforest from Belize City.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Distance to Reef</strong><p class="mt-2 text-gray-600">Boat ride to Caye Caulker — <strong>45–60 min</strong> each way typical.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Currency</strong><p class="mt-2 text-gray-600">Belize dollars (BZD) pegged 2:1 to USD. <strong>US dollars</strong> widely accepted.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Return Timing</strong><p class="mt-2 text-gray-600">Allow <strong>60–90 minutes</strong> before all aboard including tender ride back to ship.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Weather</strong><p class="mt-2 text-gray-600">Warm and humid year-round. Lightweight clothing, reef-safe sunscreen and insect repellent recommended.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Language</strong><p class="mt-2 text-gray-600">English is the official language — easy communication for cruise passengers.</p></div>
    <div class="bg-ocean-50 rounded-2xl p-6"><strong class="text-gray-900">Lamanai</strong><p class="mt-2 text-gray-600">~1.5 hours north including river boat — full-day excursion.</p></div>
    <div class="bg-sand-50 rounded-2xl p-6"><strong class="text-gray-900">Short Port Day?</strong><p class="mt-2 text-gray-600">2-hour city tours and rum factory tastings fit tighter schedules.</p></div>
  </div>
  <p class="text-center mt-8"><a href="one-day-in-belize-from-a-cruise-ship.html" class="text-ocean-600 font-semibold text-sm">One-day itinerary →</a> · <a href="best-belize-shore-excursions.html" class="text-ocean-600 font-semibold text-sm">Compare excursions →</a></p>
  <div class="mt-10 max-w-3xl mx-auto">{internal_links()}</div>
</div></section>"""


def content_one_day() -> str:
    snap = snapshot_default(best_for="Morning ruins or cave + afternoon reef if time allows")
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 text-sm">Sample timeline for a <strong>6–10 hour</strong> Belize City port call. Adjust for your ship's actual tender, gangway and all-aboard times.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold text-center mb-8">Classic Belize Port Day</h2>
  <ol class="space-y-4 text-sm">
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-pr-100"><span class="font-bold text-ocean-600 shrink-0">08:00</span><div><strong>Tender ashore</strong><p class="text-gray-600 mt-1">Allow 20–30 minutes for tender queue and ride to Fort Street Tourism Village.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-pr-100"><span class="font-bold text-ocean-600 shrink-0">08:30</span><div><strong>Meet excursion</strong><p class="text-gray-600 mt-1">Depart for Altun Ha, cave tubing or reef boat — morning starts beat afternoon rain and heat.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-pr-100"><span class="font-bold text-ocean-600 shrink-0">12:00</span><div><strong>Main activity peak</strong><p class="text-gray-600 mt-1">Temple climbing, cave float or reef snorkel depending on your chosen tour.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-pr-100"><span class="font-bold text-ocean-600 shrink-0">14:30</span><div><strong>Return inland / boat</strong><p class="text-gray-600 mt-1">Transport back toward Belize City with operator-managed timing.</p></div></li>
    <li class="flex gap-4 bg-white rounded-2xl p-5 border border-pr-100"><span class="font-bold text-ocean-600 shrink-0">16:00</span><div><strong>Tender back to ship</strong><p class="text-gray-600 mt-1">Allow margin before published all-aboard — shore excursions build this buffer in.</p></div></li>
  </ol>
  <div class="mt-8 bg-white rounded-2xl p-6 border border-pr-100">
    <h3 class="font-display font-bold text-lg mb-3">Suggested Excursions</h3>
    <ul class="space-y-2 text-sm text-gray-600">
      <li><a href="altun-ha-and-belize-city-overview.html" class="text-ocean-600 font-medium">Altun-Ha and Belize City Overview</a> — best compact ruins and city combo</li>
      <li><a href="belize-cave-tubing.html" class="text-ocean-600 font-medium">Belize Cave Tubing</a> — signature adventure experience</li>
      <li><a href="turtle-snorkel-and-island-time.html" class="text-ocean-600 font-medium">Turtle Snorkel and Island Time</a> — reef and Caye Caulker</li>
    </ul>
  </div>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_private_tours() -> str:
    snap = snapshot_default(best_for="Groups wanting custom pacing", popular="Private cave tubing, Jeep tours, small-group ruins")
    private_tours = [t for t in TOURS if t["size"] in ("Private", "Small")]
    links = "".join(
        f'<li><a href="{t["slug"]}.html" class="text-ocean-600 font-medium">{t["title"]}</a> — {t["duration"]}, {t["activity"]}</li>'
        for t in private_tours[:8]
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Private and small-group Belize shore excursions give cruise passengers more control over pacing, pickup timing and group composition. After you tender to Fort Street Tourism Village, a dedicated guide and vehicle meet your party — no waiting for a full coach to fill.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Private tubing</strong> — <a href="private-tubing-expedition.html" class="text-ocean-600">Private Tubing Expedition</a> for your group only.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Small-group Jeep</strong> — Jungle Jeep adventures with fewer guests per vehicle.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Return-to-ship focus</strong> — private operators still build all-aboard buffer.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Family groups</strong> — split cost across cabins to rival per-person coach pricing.</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{PRIVATE_IMG}" alt="{PRIVATE_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold mb-6">Private &amp; Small-Group Tours</h2>
  <ul class="space-y-3 text-sm text-gray-600">{links}</ul>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_snorkel_beach() -> str:
    snap = snapshot_default(best_for="Reef snorkel and island beach days", popular="Caye Caulker, Shark Ray Alley, Goff's Caye")
    snorkel_tours = [t for t in TOURS if t["category"] in ("snorkel", "beach")]
    links = "".join(
        f'<li class="flex gap-2 mb-2"><span class="text-ocean-500">✓</span><a href="{t["slug"]}.html" class="text-ocean-600 font-medium">{t["title"]}</a> — {t["duration"]}</li>'
        for t in snorkel_tours
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Belize sits along the <strong>Belize Barrier Reef</strong> — the second-largest reef system in the world. Cruise excursions boat to Caye Caulker, Hol Chan Marine Reserve and Goff's Caye for snorkelling with turtles, rays and nurse sharks, then add beach time with rum punch and fresh fruit.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Book morning</strong> — calmer water and better visibility early in port day.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Reef-safe sunscreen</strong> — required at marine reserves.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Return-to-ship</strong> — boat tours time returns including tender buffer.</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{SNORKEL_IMG}" alt="{SNORKEL_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold mb-6">Snorkelling &amp; Beach Excursions</h2>
  <ul class="space-y-2 text-sm text-gray-600">{links}</ul>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_ruins() -> str:
    snap = snapshot_default(best_for="Mayan archaeology and cultural tours", popular="Altun Ha, Lamanai, Cahal Pech, Xunantunich")
    ruins_tours = [t for t in TOURS if t["category"] in ("ruins", "lamanai")]
    links = "".join(
        f'<li class="flex gap-2 mb-2"><span class="text-ocean-500">✓</span><a href="{t["slug"]}.html" class="text-ocean-600 font-medium">{t["title"]}</a> — {t["duration"]}, {t["activity"]}</li>'
        for t in ruins_tours
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"><div class="grid lg:grid-cols-2 gap-12 items-start">
  <div>
    <p class="text-gray-600 leading-relaxed mb-6">Belize was the heartland of the ancient Mayan civilisation. <strong>Altun Ha</strong> is the most popular cruise-excursion ruins site — about one hour inland with climbable temples. <strong>Lamanai</strong> is larger and reached by river boat through jungle waterways teeming with howler monkeys and birdlife.</p>
    <ul class="space-y-3 mb-6 text-sm text-gray-600">
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Altun Ha</strong> — compact, fits most port calls, Temple of the Sun God.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Lamanai</strong> — full-day eco adventure, river boat access.</li>
      <li class="flex gap-2"><span class="text-ocean-500">✓</span><strong>Comfortable shoes</strong> — temple climbing and uneven paths throughout.</li>
    </ul>
  </div>
  <div class="card-media rounded-3xl overflow-hidden aspect-[4/3] shadow-lg">
    <img src="{LAMANAI_IMG}" alt="{LAMANAI_ALT}" width="600" height="450" loading="lazy" decoding="async" />
  </div>
</div></div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <h2 class="text-2xl font-display font-bold mb-6">Mayan Ruins Excursions</h2>
  <ul class="space-y-2 text-sm text-gray-600">{links}</ul>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def content_faq() -> str:
    snap = snapshot_default()
    faq_items = home_faq_data() + [
        ("Can I do multiple activities in one day?", "Combo tours like cave tubing and zip line are designed for multiple experiences. Ruins plus reef in one day is usually too rushed."),
        ("What should I bring for a Belize excursion?", "Comfortable clothing, reef-safe sunscreen, insect repellent, water shoes for cave tubing and a waterproof bag."),
        ("Are shore excursions worth it in Belize?", "Yes — inland and reef sites need organised transport. Excursions handle tender timing and return-to-ship logistics."),
    ]
    details = "".join(
        f'<details class="faq-item rounded-2xl border border-pr-100 p-5"><summary class="font-semibold text-gray-900 cursor-pointer">{q}</summary><p class="mt-4 text-sm text-gray-500">{a}</p></details>'
        for q, a in faq_items
    )
    return f"""<section class="pt-8 pb-4 bg-white"><div class="max-w-3xl mx-auto px-4 text-center">
  <p class="text-gray-600 text-sm">Answers to common questions from cruise passengers planning a Belize City port day.</p>
</div></section>
<section class="pb-8 bg-white"><div class="max-w-7xl mx-auto px-4">{snap}</div></section>
<section class="py-12 bg-sand-50"><div class="max-w-3xl mx-auto px-4">
  <div class="info-image rounded-3xl aspect-[21/9] shadow-lg overflow-hidden mb-8">
    <img src="{FAQ_IMG}" alt="{FAQ_ALT}" width="800" height="343" loading="lazy" decoding="async" />
  </div>
  <div class="space-y-4">{details}</div>
  <div class="mt-10">{internal_links()}</div>
</div></section>"""


def all_guide_content() -> dict[str, str]:
    return {
        "home.html": content_home(),
        "best-belize-shore-excursions.html": content_best_excursions(),
        "belize-cruise-port-guide.html": content_port_guide(),
        "one-day-in-belize-from-a-cruise-ship.html": content_one_day(),
        "belize-private-tours.html": content_private_tours(),
        "belize-snorkeling-and-beach-excursions.html": content_snorkel_beach(),
        "belize-mayan-ruins-excursions.html": content_ruins(),
        "belize-shore-excursions-faq.html": content_faq(),
    }
