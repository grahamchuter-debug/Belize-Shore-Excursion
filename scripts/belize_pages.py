"""World 2.0 editorial HTML body generators for Belize Shore Excursion."""
from __future__ import annotations

from html import escape

from belize_config import (
    ALTUN_HA_ALT,
    ALTUN_HA_CLUSTER,
    ALTUN_HA_IMG,
    BEACH_ALT,
    BEACH_IMG,
    BEST_ALT,
    BEST_IMG,
    CAVE_ALT,
    CAVE_IMG,
    EMAIL,
    FAQ_ALT,
    FAQ_IMG,
    INTRO_ALT,
    INTRO_IMG,
    LAMANAI_ALT,
    LAMANAI_IMG,
    ONE_DAY_ALT,
    ONE_DAY_IMG,
    PORT_ALT,
    PORT_IMG,
    PORT_ARRIVAL_ALT,
    PORT_ARRIVAL_IMG,
    PRIVATE_ALT,
    PRIVATE_IMG,
    SITE,
    SLUG_IMAGES,
    SNORKEL_ALT,
    SNORKEL_IMG,
    ZOO_ALT,
    ZOO_IMG,
)
from belize_shell import related_nav, snapshot
from belize_tours_data import TOURS


FAQ_ITEMS: list[tuple[str, str]] = [
    (
        "Is Belize City a tender port for cruise ships?",
        "Yes. Cruise ships anchor offshore and passengers travel by tender to Fort Street Tourism Village. Check your ship's daily instructions because tender queues and procedures can vary.",
    ),
    (
        "How long is a typical Belize City port call?",
        "A typical call is about 6–10 hours, but your ship's published arrival, tender and all-aboard information is the schedule that matters.",
    ),
    (
        "How much return time should I allow?",
        "As planning guidance, work backwards from all aboard and keep a 60–90 minute return buffer that includes the tender process. This is advice, not a guarantee.",
    ),
    (
        "How far are the main excursion areas from the tender port?",
        "Altun Ha and the cave area are typically about 45–60 minutes by road, reef boats commonly take about 45–60 minutes, and Lamanai involves a longer journey of roughly 1.5 hours.",
    ),
    (
        "Which Belize excursion theme suits a first visit?",
        "Cave tubing highlights the rainforest, Altun Ha offers an accessible Mayan ruins day, and reef or island routes suit passengers who want their time on the water.",
    ),
    (
        "Can I combine several Belize highlights in one port day?",
        "Purpose-built combinations such as cave tubing with zip line can fit their listed duration. Combining distant themes independently can make a tender day unnecessarily tight.",
    ),
    (
        "What should I bring for cave tubing?",
        "Wear secure footwear that can get wet and bring quick-drying clothing, sun protection, insect repellent and a dry place for essentials. Confirm equipment and restrictions directly with the tour provider.",
    ),
    (
        "What should I consider for snorkeling or a beach day?",
        "Consider swimming confidence, sea conditions, sun exposure and the boat transfer. Confirm equipment, marine-site rules and the day's operating plan before setting out.",
    ),
    (
        "Which Mayan site is easiest to fit into a cruise day?",
        "Altun Ha is the closest of the featured sites, typically about 45–60 minutes from Belize City. Lamanai, Cahal Pech and Xunantunich require more travel and a more generous port window.",
    ),
    (
        "Are private tours automatically faster?",
        "Not necessarily. Private touring can give a group more control over pacing, but road, boat, weather and tender constraints still apply.",
    ),
    (
        "What currency and language are used in Belize?",
        "English is the official language. The Belize dollar is pegged at BZD 2 to USD 1; clarify the currency before paying for anything.",
    ),
    (
        "Is this website affiliated with a cruise line?",
        f"No. {SITE} is an independent editorial planning guide and is not affiliated with any cruise line.",
    ),
]


PRIORITY_A_COPY: dict[str, str] = {
    "cave-tubing-and-zip-line-combo": (
        "Cave Tubing and Zip Line Combo puts two distinct rainforest experiences into a listed six-hour route: canopy activity above the forest and a cave float below it. The appeal is variety, but the useful comparison is pace. Passengers should expect more transitions, equipment changes and active movement than on a cave-only day, with the tender and inland drive still framing the excursion."
    ),
    "belize-cave-tubing": (
        "Belize Cave Tubing is the focused version of the country's signature rainforest experience. Its listed five-hour format centres the underground river rather than adding a second major activity, which may suit passengers who prefer a clearer rhythm: tender ashore, travel inland, walk and float, then return toward Belize City with a deliberate margin."
    ),
    "turtle-snorkel-and-island-time": (
        "Turtle Snorkel and Island Time combines reef-focused swimming with time around Caye Caulker in a listed five-hour outing. Wildlife sightings can never be promised, so the route is best understood as a marine and island day whose character depends on sea conditions, visibility and the operating plan, not a checklist of guaranteed encounters."
    ),
    "altun-ha-and-belize-city-overview": (
        "Altun-Ha and Belize City Overview pairs the most accessible featured Mayan site with city context in a listed four-hour route. Altun Ha is typically about 45–60 minutes inland, making this a more compact ruins choice than Belize's farther archaeological sites while still requiring sensible tender and road-time planning."
    ),
    "shark-ray-alley-and-caye-caulker-beach-break": (
        "Shark Ray Alley and Caye Caulker Beach Break by Boat divides a listed five-hour day between a marine stop and island time. Treat nurse sharks, rays and other wildlife as possible encounters rather than scheduled attractions, and compare this route with a snorkel-led option if water time matters more than the beach break."
    ),
    "lamanai-eco-adventure": (
        "Lamanai Eco Adventure is the most travel-intensive Priority A route: a listed six-hour day built around a major Mayan site and river approach. With Lamanai roughly 1.5 hours from Belize City in the planning evidence, this is a route for a generous call and careful tender timing rather than a day to combine casually with other distant stops."
    ),
    "kukumba-beach-and-city": (
        "Kukumba Beach and City offers a listed five-hour land-based contrast to the offshore cayes, combining beach time with Old Belize and city context. It suits passengers who want a lighter activity level without making a reef snorkel the centre of the day, while still leaving room for transport and tender logistics."
    ),
}


CATEGORY_GUIDANCE = {
    "cave": (
        "Rainforest and cave",
        "Expect an inland transfer, a guided approach to the cave system and time in or beside the water. Surfaces can be wet and uneven.",
        "Compare cave routes by activity mix, listed duration and whether a focused float or a broader combination better fits your group.",
    ),
    "zip": (
        "Canopy adventure",
        "The route centres on zip-line activity in the rainforest, with briefings, equipment and transitions forming part of the day.",
        "Consider comfort with heights, moderate activity and the inland transfer before choosing a canopy-led day.",
    ),
    "snorkel": (
        "Reef and island",
        "Expect a boat transfer, a water briefing and snorkel time shaped by sea and weather conditions, with island time where the route includes it.",
        "Marine life is wild and sightings are never certain; compare the balance of swimming, boat time and time ashore.",
    ),
    "beach": (
        "Beach and water",
        "These routes balance beach or island time with snorkeling, a city component or another stop depending on the itinerary.",
        "Check whether the beach or the water activity is the main purpose, and plan for sun, swimming confidence and boat conditions where relevant.",
    ),
    "ruins": (
        "Mayan heritage",
        "Expect road travel, guided archaeological context and walking over warm, sometimes uneven ground at the site.",
        "Compare sites by travel burden and by the second theme—city, river, wildlife or Jeep—rather than treating every ruins title as the same day.",
    ),
    "lamanai": (
        "Lamanai and river",
        "This longer-distance route combines a river approach with archaeological exploration at one of Belize's major Mayan sites.",
        "Lamanai is roughly 1.5 hours away in the planning evidence, so use a generous port call and read the tender schedule carefully.",
    ),
    "zoo": (
        "Belize wildlife",
        "The route combines native wildlife interpretation at Belize Zoo with city or countryside elements named in the itinerary.",
        "It can suit mixed-interest groups, but confirm walking conditions and do not assume any particular animal will be visible.",
    ),
    "wildlife": (
        "Wildlife and habitat",
        "Expect habitat-led interpretation, with the route focused on monkeys, birds, river scenery or other native wildlife.",
        "Wildlife is not scheduled. Choose this theme for the landscape and guide context as much as for possible sightings.",
    ),
    "jeep": (
        "Jungle and countryside",
        "Jeep routes use the drive itself as part of the experience and may add a cave, river, beach, ruins or city stop.",
        "Compare the named stops carefully: similar Jeep titles can produce very different days, and rougher travel may not suit every passenger.",
    ),
    "city": (
        "Belize City",
        "These shorter routes focus on city context, sightseeing or a named cultural stop rather than a long inland or offshore journey.",
        "They are useful comparisons for tighter calls, although tender time still reduces the hours available ashore.",
    ),
    "private": (
        "Private pacing",
        "A private format keeps the listed cave-tubing route within one group rather than changing the underlying travel distances.",
        "Use the format to discuss pace and needs, while keeping the same conservative return planning as any other excursion.",
    ),
    "combo": (
        "Multi-activity day",
        "Combination routes join two or more headline activities, so transitions and transport are a meaningful part of the listed duration.",
        "Choose the combination because both themes matter to you, not simply because it contains more stops.",
    ),
}


def _img(path: str, alt: str) -> str:
    return (
        f'<div class="media-frame"><img src="{path}" alt="{escape(alt)}" '
        'width="900" height="675" loading="lazy" decoding="async" /></div>'
    )


def _theme(href: str, image: str, alt: str, title: str, text: str) -> str:
    return f"""<a class="theme-link" href="{href}">
  <div class="theme-link__media"><img src="{image}" alt="{escape(alt)}" width="640" height="400" loading="lazy" decoding="async" /></div>
  <div class="theme-link__body"><h3>{escape(title)}</h3><p>{text}</p></div>
</a>"""


def _tour_link(tour: dict) -> str:
    return f"/{escape(tour['slug'])}.html"


def _tour_cards(tours: list[dict], limit: int | None = None) -> str:
    selected = tours[:limit] if limit else tours
    cards = []
    for tour in selected:
        image, alt = SLUG_IMAGES.get(tour["slug"], (INTRO_IMG, INTRO_ALT))
        cards.append(
            _theme(
                _tour_link(tour),
                image,
                alt,
                tour["title"],
                f"{escape(tour['seg_desc'])} <span class=\"muted\">{escape(tour['duration'])} · {escape(tour['activity'])}.</span>",
            )
        )
    return "\n".join(cards)


def _find(slug: str, tours: list[dict] | None = None) -> dict:
    return next(t for t in (tours or TOURS) if t["slug"] == slug)


def _compare_table(tours: list[dict]) -> str:
    rows = []
    for tour in tours:
        focus = CATEGORY_GUIDANCE.get(tour["category"], ("Belize day", "", ""))[0]
        rows.append(
            "<tr>"
            f'<td><a href="{_tour_link(tour)}">{escape(tour["title"])}</a></td>'
            f"<td>{escape(tour['duration'])}</td><td>{escape(focus)}</td>"
            f"<td>{escape(tour['activity'])}</td><td>{escape(tour['size'])}</td>"
            "</tr>"
        )
    return f"""<table class="compare">
  <thead><tr><th scope="col">Route</th><th scope="col">Listed duration</th><th scope="col">Main focus</th><th scope="col">Activity</th><th scope="col">Format</th></tr></thead>
  <tbody>{''.join(rows)}</tbody>
</table>"""


def home_body() -> str:
    featured = [_find(slug) for slug in PRIORITY_A_COPY]
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose">
    <p class="eyebrow">Belize City · Tender port</p>
    <h2>Choose the shape of the day first</h2>
    <p class="lead">Belize brings rainforest caves, Mayan sites and Caribbean reef routes within reach of a single port call—but not all within the same sensible itinerary.</p>
    <p>Ships tender to Fort Street Tourism Village. A typical call is 6–10 hours, so compare the real mix of transfer time, activity and return margin before choosing a route.</p>
    <p class="note">{SITE} is an independent editorial guide and is not affiliated with any cruise line.</p>
  </div>
  {_img(INTRO_IMG, INTRO_ALT)}
</div></section>

<section class="section section--alt"><div class="wrap">
  <p class="eyebrow">Top themes</p><h2>Four ways to explore Belize</h2>
  <div class="grid-4">
    {_theme("/belize-cave-tubing.html", CAVE_IMG, CAVE_ALT, "Cave tubing", "Plan a focused cave float or compare it with a zip-line combination.")}
    {_theme("/belize-mayan-ruins-excursions.html", ALTUN_HA_IMG, ALTUN_HA_ALT, "Mayan ruins", "Compare nearby Altun Ha with longer journeys to Lamanai, Cahal Pech and Xunantunich.")}
    {_theme("/belize-snorkeling-and-beach-excursions.html", SNORKEL_IMG, SNORKEL_ALT, "Snorkel and beach", "Explore reef-led, wildlife-led and island-time routes from Belize City.")}
    {_theme("/belize-private-tours.html", PRIVATE_IMG, PRIVATE_ALT, "Private touring", "Understand what flexible pacing can—and cannot—change on a tender day.")}
  </div>
</div></section>

<section class="section"><div class="wrap">
  <p class="eyebrow">Priority routes</p><h2>Featured starting points</h2>
  <p class="lead">Use these seven route guides as editorial comparisons, then confirm current details directly with the relevant provider.</p>
  <div class="grid-3">{_tour_cards(featured)}</div>
</div></section>

<section class="section section--alt"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Rainforest</p><h2>Caves reward a focused plan</h2>
    <p>The cave area is typically 45–60 minutes inland. A cave-only route gives the float more space; a zip-line combination adds variety and more transitions.</p>
    <a class="btn btn--outline" href="/belize-cave-tubing.html">Explore cave tubing</a>
  </div>{_img(CAVE_IMG, CAVE_ALT)}
</div></section>

<section class="section"><div class="wrap grid-2">
  {_img(ALTUN_HA_IMG, ALTUN_HA_ALT)}
  <div class="prose"><p class="eyebrow">Mayan heritage</p><h2>Distance separates the ruins choices</h2>
    <p>Altun Ha is typically 45–60 minutes from Belize City. Lamanai is roughly 1.5 hours away, while Cahal Pech and Xunantunich also call for a generous schedule.</p>
    <a class="btn btn--outline" href="/belize-mayan-ruins-excursions.html">Compare Mayan routes</a>
  </div>
</div></section>

<section class="section section--alt"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Barrier reef</p><h2>Choose water time or island balance</h2>
    <p>Reef boats commonly involve a 45–60 minute transfer. Compare routes by the balance of snorkeling, wildlife possibilities and time ashore; sea conditions shape every marine day.</p>
    <a class="btn btn--outline" href="/belize-snorkeling-and-beach-excursions.html">Explore reef and beach</a>
  </div>{_img(SNORKEL_IMG, SNORKEL_ALT)}
</div></section>

<section class="section"><div class="wrap grid-2">
  {_img(PORT_ARRIVAL_IMG, PORT_ARRIVAL_ALT)}
  <div class="prose"><p class="eyebrow">Port planning</p><h2>The tender is part of the itinerary</h2>
    <p>Use your ship's daily programme for tender procedures and all aboard. As planning advice, many passengers keep 60–90 minutes before all aboard for the return and tender process; no editorial guide can guarantee the outcome.</p>
    <a class="btn btn--primary" href="/belize-cruise-port-guide.html">Plan the port day</a>
  </div>
</div></section>

<section class="section section--deep"><div class="wrap grid-2">
  <div><p class="eyebrow">Why use this site</p><h2>Comparison without invented certainty</h2>
    <p>We organise route evidence around duration, activity, group format, transfer burden and theme overlap. We avoid fabricated scores, invented prices and promises about ship return.</p>
  </div>
  <div><h3>Continue planning</h3>
    <p><a class="btn btn--primary" href="/best-belize-shore-excursions.html">Compare excursions</a></p>
    <p><a class="btn btn--outline" href="/methodology/">Explore our methodology</a></p>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <p class="eyebrow">Quick answers</p><h2>Belize shore excursion FAQ</h2>
  <div class="faq">
    {''.join(f"<details><summary>{escape(q)}</summary><p>{a}</p></details>" for q, a in FAQ_ITEMS[:4])}
  </div>
  <p><a class="btn btn--outline" href="/belize-shore-excursions-faq.html">Explore all questions</a></p>
  <p class="note">Travel conditions, tender operations and third-party route details can change. Confirm current information for your specific call.</p>
  {related_nav()}
</div></section>
"""


def hub_best_body(tours: list[dict]) -> str:
    featured = [t for t in tours if t.get("featured")]
    return f"""
<section class="section"><div class="wrap prose">
  <p class="eyebrow">Comparison hub</p><h2>Start with theme, then test the timing</h2>
  <p class="lead">There is no universal “best” Belize shore excursion. The useful choice is the route that matches your interests, activity comfort and actual tender-day window.</p>
  <p>Featured routes below span cave, ruins, reef, beach and private formats. Listed durations come from the route inventory; they are comparison inputs, not a promise for a particular date.</p>
  {snapshot([("Port setup", "Tender to Fort Street Tourism Village"), ("Typical call", "About 6–10 hours; confirm your ship"), ("Planning lens", "Theme, transfer, activity and return margin")])}
</div></section>
<section class="section section--alt"><div class="wrap">
  <h2>Featured route comparison</h2>{_compare_table(featured)}
</div></section>
<section class="section"><div class="wrap">
  <p class="eyebrow">Browse by travel style</p><h2>Match the day to your priorities</h2>
  <div class="grid-3">
    {_theme("/belize-cave-tubing.html", CAVE_IMG, CAVE_ALT, "Rainforest adventure", "Compare focused cave tubing, zip line and multi-activity combinations.")}
    {_theme("/belize-mayan-ruins-excursions.html", ALTUN_HA_IMG, ALTUN_HA_ALT, "History and ruins", "Compare archaeological sites by road time, format and companion stops.")}
    {_theme("/belize-snorkeling-and-beach-excursions.html", BEACH_IMG, BEACH_ALT, "Water and island time", "Compare reef snorkeling with beach-led and mixed marine days.")}
    {_theme("/belize-private-tours.html", PRIVATE_IMG, PRIVATE_ALT, "Private and small group", "Explore pacing, group format and realistic flexibility.")}
    {_theme("/belize-cruise-port-guide.html", PORT_IMG, PORT_ALT, "Tender-day planning", "Understand Fort Street Tourism Village and conservative return planning.")}
    {_theme("/one-day-in-belize-from-a-cruise-ship.html", ONE_DAY_IMG, ONE_DAY_ALT, "One-day framework", "Build an itinerary from your ship's actual tender and all-aboard times.")}
  </div>{related_nav()}
</div></section>
"""


def hub_mayan_body(tours: list[dict]) -> str:
    mayan = [t for t in tours if t["category"] in ("ruins", "lamanai") or "Xunantunich" in t["title"]]
    altun = [t for t in mayan if "altun" in t["slug"]]
    others = [t for t in mayan if t not in altun]
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Mayan ruins hub</p><h2>Compare sites by distance and depth</h2>
    <p class="lead">Altun Ha is the compact cruise-day choice; Lamanai, Cahal Pech and Xunantunich ask more of the port window.</p>
    <p>Altun Ha is typically 45–60 minutes from Belize City. Lamanai is roughly 1.5 hours away and adds a river approach. The listed Cahal Pech and Xunantunich routes run six hours or more, so check the tender schedule before treating them as interchangeable.</p>
  </div>{_img(ALTUN_HA_IMG, ALTUN_HA_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  <h2>Four archaeological directions</h2>
  <div class="grid-4">
    {_theme("/altun-ha-and-belize-city-overview.html", ALTUN_HA_IMG, ALTUN_HA_ALT, "Altun Ha", "The closest featured ruins route, with city context in a listed four-hour day.")}
    {_theme("/lamanai-eco-adventure.html", LAMANAI_IMG, LAMANAI_ALT, "Lamanai", "A longer river-and-ruins route for a generous port call.")}
    {_theme("/journey-to-cahal-pech.html", BEST_IMG, BEST_ALT, "Cahal Pech", "A listed six-hour cultural route with Belize City context.")}
    {_theme("/xunantunich-and-cave-tubing.html", BEST_IMG, BEST_ALT, "Xunantunich", "A listed six-and-a-half-hour combination with cave tubing.")}
  </div>
</div></section>
<section class="section"><div class="wrap">
  <h2>Altun Ha variations</h2><p class="lead">These overlapping routes preserve different second themes—city, river, wildlife, zoo or Jeep. Compare the companion stop and listed duration rather than assuming duplication means the same experience.</p>
  <div class="grid-3">{_tour_cards(altun)}</div>
  <h2>Longer-site routes</h2><div class="grid-3">{_tour_cards(others)}</div>
  {related_nav([("/altun-ha-and-belize-city-overview.html", "Explore Altun Ha"), ("/lamanai-eco-adventure.html", "Explore Lamanai")])}
</div></section>
"""


def hub_snorkel_body(tours: list[dict]) -> str:
    water = [t for t in tours if t["category"] in ("snorkel", "beach")]
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Reef and beach hub</p><h2>Decide how much of the day belongs in the water</h2>
    <p class="lead">Belize routes range from snorkel-led reef days to beach-led island or city combinations.</p>
    <p>A reef boat commonly takes about 45–60 minutes. Weather, sea state and visibility can change the plan, and wildlife encounters are possibilities rather than guarantees.</p>
    <ul class="checklist"><li>Compare swimming intensity and time ashore.</li><li>Plan for sun and a wet boat environment.</li><li>Confirm equipment and marine-site rules directly.</li></ul>
  </div>{_img(SNORKEL_IMG, SNORKEL_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  <h2>Snorkel and beach routes</h2><div class="grid-3">{_tour_cards(water)}</div>
  {related_nav([("/turtle-snorkel-and-island-time.html", "Explore turtle snorkel"), ("/shark-ray-alley-and-caye-caulker-beach-break.html", "Compare Shark Ray Alley")])}
</div></section>
"""


def hub_private_body(tours: list[dict]) -> str:
    private = [t for t in tours if t["size"] in ("Private", "Small")]
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Private and small-group hub</p><h2>Use flexibility to simplify the day</h2>
    <p class="lead">Private or small-group formats can improve pacing and communication, but they do not shorten Belize's roads, boat transfers or tender process.</p>
    <p>The inventory contains one explicitly private route—Private Tubing Expedition—and several small-group routes. Treat those labels distinctly and confirm the actual operating format for your date.</p>
    <ul class="checklist"><li>Share mobility and activity needs.</li><li>Agree the route focus before leaving port.</li><li>Keep a conservative return margin.</li></ul>
  </div>{_img(PRIVATE_IMG, PRIVATE_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  <h2>Private and small-group route guides</h2><div class="grid-3">{_tour_cards(private)}</div>
  {related_nav([("/private-tubing-expedition.html", "Explore private tubing")])}
</div></section>
"""


def port_guide_body() -> str:
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Cruise port guide</p><h2>Belize City begins with a tender</h2>
    <p class="lead">Cruise ships anchor offshore and passengers come ashore at Fort Street Tourism Village.</p>
    <p>Use your ship's daily programme for tender distribution, meeting instructions and all aboard. Tender queues can compress a nominal 6–10 hour call, so count usable time ashore rather than the headline port window.</p>
  </div>{_img(PORT_ARRIVAL_IMG, PORT_ARRIVAL_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  {snapshot([("Arrival", "Tender to Fort Street Tourism Village"), ("Typical port call", "About 6–10 hours"), ("Altun Ha", "Typically 45–60 minutes by road"), ("Cave area", "Typically 45–60 minutes by road"), ("Reef boat", "Typically 45–60 minutes"), ("Lamanai", "Roughly 1.5 hours"), ("Currency", "BZD 2 to USD 1"), ("Language", "English is official"), ("Return advice", "Plan a 60–90 minute buffer; not a guarantee")])}
</div></section>
<section class="section"><div class="wrap grid-3">
  <div class="prose"><h2>Before tendering</h2><p>Note the final tender and all-aboard times, carry the information you need offline, and identify the exact meeting instruction for your chosen route.</p></div>
  <div class="prose"><h2>At Fort Street</h2><p>Orient yourself before leaving the tourism village. Similar route names do not establish a meeting point; use the instructions supplied for your day.</p></div>
  <div class="prose"><h2>For the return</h2><p>Work backwards from all aboard. A 60–90 minute margin is conservative planning advice, not a return promise or substitute for current conditions.</p></div>
</div></section>
<section class="section section--deep"><div class="wrap prose">
  <h2>No guide can remove port-day uncertainty</h2><p>Traffic, weather, sea conditions, tender operations and third-party decisions all matter. Confirm details and choose a plan whose margin you are comfortable keeping.</p>
  <a class="btn btn--primary" href="/one-day-in-belize-from-a-cruise-ship.html">Plan one day in Belize</a>
  {related_nav()}
</div></section>
"""


def one_day_body() -> str:
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">One-day framework</p><h2>Build from all aboard backwards</h2>
    <p class="lead">A useful Belize itinerary is a decision framework, not a fictional clock.</p>
    <p>Start with your ship's actual all-aboard time, set aside a 60–90 minute planning buffer for the return and tender, then account for getting ashore. What remains is your usable excursion window.</p>
  </div>{_img(ONE_DAY_IMG, ONE_DAY_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  <h2>Choose one anchor theme</h2>
  <div class="grid-3">
    {_theme("/belize-cave-tubing.html", CAVE_IMG, CAVE_ALT, "Rainforest anchor", "Allow for the typical 45–60 minute inland drive plus the listed route duration.")}
    {_theme("/altun-ha-and-belize-city-overview.html", ALTUN_HA_IMG, ALTUN_HA_ALT, "Ruins anchor", "Altun Ha is the most compact featured ruins direction from Belize City.")}
    {_theme("/belize-snorkeling-and-beach-excursions.html", BEACH_IMG, BEACH_ALT, "Water anchor", "Allow for the boat transfer and a plan that can respond to sea conditions.")}
  </div>
</div></section>
<section class="section"><div class="wrap prose">
  <h2>A practical sequence</h2>
  <ol><li>Confirm tender procedure and all aboard.</li><li>Protect your preferred 60–90 minute return margin.</li><li>Compare listed duration and transfer burden.</li><li>Choose one anchor theme, adding only combinations already designed as a single route.</li><li>Recheck the plan if the tender ashore takes longer than expected.</li></ol>
  <p class="note">Do not copy sample clock times from another ship call. Your daily programme is the relevant schedule.</p>
  {related_nav()}
</div></section>
"""


def faq_body() -> str:
    items = "".join(
        f"<details><summary>{escape(question)}</summary><p>{answer}</p></details>"
        for question, answer in FAQ_ITEMS
    )
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">Planning FAQ</p><h2>Answers for a Belize tender day</h2>
    <p class="lead">These answers explain the planning evidence without promising a particular operator, schedule or outcome.</p>
  </div>{_img(FAQ_IMG, FAQ_ALT)}
</div></section>
<section class="section section--alt"><div class="wrap">
  <div class="faq">{items}</div>{related_nav()}
</div></section>
"""


def _unique_intro(tour: dict) -> str:
    if tour["slug"] in PRIORITY_A_COPY:
        return PRIORITY_A_COPY[tour["slug"]]
    focus, _, lens = CATEGORY_GUIDANCE.get(tour["category"], ("Belize excursion", "", "Compare the route with nearby alternatives."))
    return (
        f"{escape(tour['title'])} is a listed {escape(tour['duration'].lower())} "
        f"{focus.lower()} route with a {escape(tour['activity'].lower())} activity level "
        f"and {escape(tour['size'].lower())} format. {escape(tour['seg_desc'])} {lens}"
    )


def _cluster_note(tour: dict, priority: str) -> str:
    slug = tour["slug"]
    if slug in ALTUN_HA_CLUSTER or (priority.upper().startswith("D") and "altun-ha" in slug):
        return (
            '<p class="note">This guide sits within a group of overlapping Altun Ha routes. '
            'The shared ruins focus is intentional; compare the second theme and listed duration '
            'to distinguish this version, then use the Mayan ruins hub for the wider context.</p>'
        )
    if slug == "belize-party-bus":
        return (
            '<p class="note">This route preserves a sightseeing-and-music intent rather than an '
            'inland, reef or archaeological excursion. Compare it with the broader hub when deciding '
            'whether a short city-focused experience matches your port-day priorities.</p>'
        )
    return ""


def tour_body(tour: dict, priority: str) -> str:
    title = escape(tour["title"])
    category = tour["category"]
    focus, expectation, lens = CATEGORY_GUIDANCE.get(
        category, ("Belize excursion", "Expect a guided route from Belize City.", "Compare timing and activity.")
    )
    image, alt = SLUG_IMAGES.get(tour["slug"], (INTRO_IMG, INTRO_ALT))
    strong = priority.upper().startswith("A") or tour["slug"] in PRIORITY_A_COPY
    category_hub = (
        "/belize-mayan-ruins-excursions.html"
        if category in ("ruins", "lamanai")
        else "/belize-snorkeling-and-beach-excursions.html"
        if category in ("snorkel", "beach")
        else "/belize-private-tours.html"
        if category == "private"
        else "/best-belize-shore-excursions.html"
    )
    timing = (
        "Allow for a typical 45–60 minute reef boat transfer and for conditions to reshape the water plan."
        if category in ("snorkel", "beach")
        else "Lamanai is roughly 1.5 hours away, making the tender and return margin central to this route."
        if category == "lamanai"
        else "Altun Ha is typically 45–60 minutes from Belize City; longer-site combinations need an especially generous call."
        if category == "ruins"
        else "The cave area is typically 45–60 minutes inland, before activity and return time are counted."
        if category in ("cave", "zip", "private") or "cave" in tour["slug"]
        else "Count the tender process and all transfers inside the port-day window, not outside it."
    )
    extra = ""
    if strong:
        extra = f"""
<section class="section section--alt"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">How to compare it</p><h2>What makes this route distinct</h2>
    <p>{lens}</p>
    <ul class="checklist"><li>Protect the activity that matters most.</li><li>Count transitions as part of the experience.</li><li>Check that the listed duration fits your usable time ashore.</li></ul>
  </div>
  <div class="prose"><p class="eyebrow">Cruise-day fit</p><h2>Test the whole journey</h2>
    <p>{timing}</p><p>Use a 60–90 minute return buffer as planning guidance, not as a guarantee.</p>
  </div>
</div></section>"""
    return f"""
<section class="section"><div class="wrap grid-2">
  <div class="prose"><p class="eyebrow">{escape(focus)} · Editorial route guide</p><h2>Plan the experience, not just the title</h2>
    <p class="lead">{_unique_intro(tour)}</p>
    {_cluster_note(tour, priority)}
  </div>{_img(image, alt)}
</div></section>
<section class="section section--alt"><div class="wrap">
  {snapshot([("Listed duration", escape(tour["duration"])), ("Activity", escape(tour["activity"])), ("Format", escape(tour["size"])), ("Theme", escape(focus)), ("Arrival", "Tender to Fort Street Tourism Village"), ("Planning status", "Editorial guide; confirm current details")])}
</div></section>
<section class="section"><div class="wrap grid-2">
  <div class="prose"><h2>What to expect</h2><p>{expectation}</p><p>{escape(tour['seg_desc'])}</p>
    <p class="note">The inventory does not establish current inclusions, equipment, accessibility rules, meeting times or operating conditions. Confirm those details directly.</p>
  </div>
  <div class="prose"><h2>Cruise timing notes</h2><p>{timing}</p>
    <ul class="checklist"><li>Use the ship's daily tender instructions.</li><li>Work backwards from all aboard.</li><li>Keep a margin that reflects current conditions.</li></ul>
  </div>
</div></section>
{extra}
<section class="section section--deep"><div class="wrap prose">
  <h2>Continue the comparison</h2><p>Place {title} beside routes with the same theme, then compare listed duration, activity level, group format and transfer burden.</p>
  <a class="btn btn--primary" href="{category_hub}">Compare related routes</a>
  <a class="btn btn--outline" href="/belize-cruise-port-guide.html">Plan with the port guide</a>
  {related_nav([(_tour_link(tour), title)])}
</div></section>
"""


def trust_about_body() -> str:
    return f"""
<section class="section"><div class="wrap prose">
  <p class="eyebrow">About</p><h2>Independent Belize cruise-day guidance</h2>
  <p>{SITE} organises Belize City excursion evidence around tender logistics, listed duration, activity level, group format and theme. The aim is to make route differences understandable before passengers seek current operating details elsewhere.</p>
  <p>We are not affiliated with any cruise line. This site does not present live inventory, prices, supplier endorsements or guaranteed outcomes.</p>
  <p><a class="btn btn--outline" href="/methodology/">Explore our methodology</a></p>
  {related_nav()}
</div></section>
"""


def trust_contact_body() -> str:
    return f"""
<section class="section"><div class="wrap prose">
  <p class="eyebrow">Contact</p><h2>Contact the editorial site</h2>
  <p>For corrections or questions about this planning guide, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
  <p class="note">We cannot confirm third-party schedules, places, prices or ship-side meeting arrangements. Contact the relevant cruise line or provider for current operational details.</p>
  <a class="btn btn--primary" href="mailto:{EMAIL}">Explore contact by email</a>
</div></section>
"""


def trust_privacy_body() -> str:
    return f"""
<section class="section"><div class="wrap prose">
  <p class="eyebrow">Privacy</p><h2>How basic site data is handled</h2>
  <p>This is an informational website. If you email <a href="mailto:{EMAIL}">{EMAIL}</a>, your address and message are used to respond to the enquiry. We do not sell personal data.</p>
  <p>Hosting and security services may process standard technical logs such as IP address, user agent and requested URL. Any future analytics or material change to this practice should be described on this page.</p>
</div></section>
"""


def trust_terms_body() -> str:
    return f"""
<section class="section"><div class="wrap prose">
  <p class="eyebrow">Terms</p><h2>Informational use</h2>
  <p>Content on this site is general editorial information for planning a Belize cruise day. Tender operations, roads, weather, sea conditions and third-party route details can change.</p>
  <p>Confirm all operational information with your cruise line and relevant providers. You remain responsible for choosing an appropriate plan and returning to your ship on time; this site does not guarantee any return outcome or third-party service.</p>
  <p>{SITE} is not affiliated with any cruise line. Questions may be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>
"""


def trust_methodology_body() -> str:
    return """
<section class="section"><div class="wrap prose">
  <p class="eyebrow">Methodology</p><h2>How route guides are structured</h2>
  <p>We compare the documented tour inventory by title, description, listed duration, activity level, group format, category and featured status. Destination context is limited to supported planning facts such as the tender at Fort Street Tourism Village and evidenced travel-time ranges.</p>
  <p>Priority A routes receive deeper editorial treatment. Overlapping Altun Ha variants and the party-bus route retain their distinct search intent while linking back to broader hubs for clarity.</p>
  <p>We do not invent prices, suppliers, capacities, schedules, ratings or guarantees. Descriptive badges are not treated as independent rankings. Pages should be updated when stronger repository evidence becomes available.</p>
  <p>Images and their source notes are documented in <a href="/images/ATTRIBUTION.md">image attribution</a>.</p>
</div></section>
"""


def not_found_body() -> str:
    return """
<section class="page-404"><div class="wrap">
  <p class="eyebrow">404</p><h1>This route is not on the map</h1>
  <p class="lead">The address may be outdated. Explore the excursion comparison or return to the Belize City port guide.</p>
  <p><a class="btn btn--primary" href="/best-belize-shore-excursions.html">Explore excursions</a>
  <a class="btn btn--outline" href="/belize-cruise-port-guide.html">Plan with the port guide</a></p>
</div></section>
"""


def product_body(tour: dict, priority: str = "B") -> str:
    """Alias used by the World 2.0 build orchestrator."""
    return tour_body(tour, priority)


def faq_schema_entities() -> list:
    return [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in FAQ_ITEMS
    ]


def hub_best_body_default() -> str:
    return hub_best_body(TOURS)


def hub_mayan_body_default() -> str:
    return hub_mayan_body(TOURS)


def hub_snorkel_body_default() -> str:
    return hub_snorkel_body(TOURS)


def hub_private_body_default() -> str:
    return hub_private_body(TOURS)
