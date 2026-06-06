"""Tour page content for Belize Shore Excursion."""
from belize_config import CATEGORY_IMAGES, INTRO_ALT, INTRO_IMG
from belize_helpers import content_tour_page
from belize_tours_data import TOURS


def _family_note(tour: dict) -> str:
    activity = tour["activity"]
    size = tour["size"]
    if activity == "Easy":
        return "Excellent for families and mixed ages"
    if activity == "Difficult":
        return "Best for fit adults; not ideal for young children"
    if size == "Private":
        return "Flexible pacing for families and private groups"
    if size == "Small":
        return "Good for families wanting smaller groups"
    return "Good for teens and active families; check age limits"


def _popular_types(category: str) -> str:
    mapping = {
        "cave": "Cave tubing, jungle treks, adventure combos",
        "zip": "Zip lines, canopy tours, adventure combos",
        "snorkel": "Barrier reef snorkel, Caye Caulker, marine life",
        "beach": "Beach breaks, island time, reef snorkel",
        "ruins": "Altun Ha, Mayan temples, cultural tours",
        "lamanai": "Lamanai ruins, river boat, eco adventures",
        "zoo": "Belize Zoo, wildlife, family-friendly tours",
        "jeep": "Jungle Jeep tours, countryside adventures",
        "city": "Belize City tours, rum factory, sightseeing",
        "wildlife": "Monkey sanctuaries, birdwatching, eco tours",
        "private": "Private cave tubing, custom group pacing",
        "combo": "Multi-activity combos, adventure packages",
    }
    return mapping.get(category, "Belize shore excursions, cruise port tours")


def _best_for(tour: dict) -> str:
    cat = tour["category"]
    title = tour["title"]
    if "Private" in tour["size"]:
        return "Groups wanting private pacing and dedicated guide"
    if cat == "cave":
        return "Adventure seekers and first-time Belize visitors"
    if cat == "snorkel" or cat == "beach":
        return "Reef lovers and relaxed Caribbean port days"
    if cat in ("ruins", "lamanai"):
        return "History buffs and culture-focused travelers"
    if cat == "zoo" or cat == "wildlife":
        return "Families and wildlife enthusiasts"
    if cat == "jeep":
        return "Active travelers wanting off-road adventure"
    if cat == "city":
        return "Short port windows and city explorers"
    if cat == "zip":
        return "Thrill seekers and canopy adventure fans"
    return f"Passengers booking {title} from Belize City"


def _intro(tour: dict) -> str:
    title = tour["title"]
    seg = tour["seg_desc"]
    size = tour["size"]
    duration = tour["duration"]
    size_note = (
        "This small-group departure keeps pacing personal and pickup straightforward at the Belize City tender port."
        if size == "Small"
        else "This private-format tour lets your group set the pace with a dedicated guide and vehicle from the Belize City cruise port."
        if size == "Private"
        else "Standard-group format with port pickup at Fort Street Tourism Village and return-to-ship timing built for cruise schedules."
    )
    return (
        f"{title} is one of the shore excursions cruise passengers book most from Belize City. "
        f"{seg} Operators meet you after your tender ride ashore and plan the {duration.lower()} itinerary "
        f"with buffer before your ship's all-aboard call. {size_note}"
    )


def _bullets(tour: dict) -> list[str]:
    duration = tour["duration"]
    activity = tour["activity"]
    size = tour["size"]
    bullets = [
        f"{duration} including transport from Belize City cruise port.",
        f"{activity} activity level — plan footwear and fitness accordingly.",
        "Port pickup at Fort Street Tourism Village after tender from ship.",
        "Return-to-ship guarantee with 60–90 minute buffer before all aboard.",
    ]
    if size == "Small":
        bullets.append("Small-group format for more personal guide attention.")
    elif size == "Private":
        bullets.append("Private excursion — your group, your pace, dedicated transport.")
    else:
        bullets.append("Easy booking with cruise-timed departures and clear meeting instructions.")
    return bullets


def _why_choose(tour: dict) -> list[str]:
    size = tour["size"]
    cat = tour["category"]
    points = [
        "Designed around Belize City tender port logistics — no guessing where to meet after you come ashore.",
        "Return-to-ship focus with operators who understand cruise all-aboard deadlines.",
        "Local guides who know inland travel times, reef conditions and rainforest trail pacing.",
    ]
    if size == "Private":
        points.append("Private format ideal when your group wants flexibility without sharing a large coach.")
    elif size == "Small":
        points.append("Smaller headcount means faster transitions and more time at each stop.")
    else:
        points.append("Straightforward booking and clear port-day instructions for first-time Belize visitors.")
    if cat in ("snorkel", "beach"):
        points.append("Reef and island routes timed for calmer morning water and reliable tender connections.")
    elif cat in ("ruins", "lamanai"):
        points.append("Mayan site access handled end-to-end — you focus on temples, not inland transport.")
    elif cat == "cave":
        points.append("Belize's signature cave tubing experience with gear, guides and safety briefing included.")
    elif cat in ("zoo", "wildlife"):
        points.append("Family-friendly wildlife encounters with rescue-centre ethics and educational guides.")
    return points


def _highlights(tour: dict, img: str, alt: str) -> list[tuple]:
    cat = tour["category"]
    title = tour["title"]
    cards = [
        (img, alt, title, tour["seg_desc"]),
        (INTRO_IMG, INTRO_ALT, "Belize City Port Pickup", "Meet at Fort Street Tourism Village after your tender ride — transport included on organised excursions."),
        (img, f"{title} shore excursion highlight for Belize cruise passengers", "Cruise-Timed Returns", "Itineraries built with buffer before all aboard so you can enjoy Belize without watching the clock."),
    ]
    if cat == "ruins":
        cards[0] = (img, alt, "Mayan Heritage", "Ancient temple plazas and jungle surroundings at Belize's premier archaeological sites.")
    elif cat == "snorkel":
        cards[0] = (img, alt, "Barrier Reef", "Clear Caribbean water, coral gardens and marine life at the Belize Barrier Reef.")
    elif cat == "cave":
        cards[0] = (img, alt, "Underground Caves", "Float through limestone cave systems once used in Mayan ceremonial rituals.")
    return cards


def _extra_links(tour: dict) -> list[tuple[str, str]]:
    cat = tour["category"]
    if cat in ("snorkel", "beach"):
        return [("belize-snorkeling-and-beach-excursions.html", "Snorkel &amp; Beach Guide")]
    if cat in ("ruins", "lamanai"):
        return [("belize-mayan-ruins-excursions.html", "Mayan Ruins Guide")]
    if cat == "private":
        return [("belize-private-tours.html", "Private Tours Guide")]
    if cat in ("cave", "zip", "jeep", "combo"):
        return [("best-belize-shore-excursions.html", "Compare Adventures")]
    return [("belize-cruise-port-guide.html", "Port Guide")]


def _tour_content(tour: dict) -> str:
    cat = tour["category"]
    img, alt = CATEGORY_IMAGES.get(cat, (INTRO_IMG, INTRO_ALT))
    alt = f"{tour['title']} Belize shore excursion for cruise passengers from Belize City port — {alt.split('—')[-1].strip() if '—' in alt else alt}"
    return content_tour_page(
        _intro(tour),
        _bullets(tour),
        _highlights(tour, img, alt),
        dict(
            best_for=_best_for(tour),
            activity_level=tour["activity"],
            family=_family_note(tour),
            popular=_popular_types(cat),
        ),
        img,
        alt,
        _why_choose(tour),
        badge=tour.get("badge"),
        highlights_subtitle=f"What to expect on {tour['title']} from Belize City cruise port.",
        extra_links=_extra_links(tour),
    )


def all_tour_content() -> dict[str, str]:
    return {f"{t['slug']}.html": _tour_content(t) for t in TOURS}


def comparison_rows() -> list[tuple]:
    featured = [t for t in TOURS if t.get("featured")]
    rows = []
    for t in featured:
        dur = t["duration"].replace(" Hours", " hrs").replace(" Hour", " hr").replace(" Minutes", " min")
        rows.append((
            t["title"],
            dur,
            t.get("badge", "Belize excursion").replace("Best ", ""),
            t["activity"],
            f"{t['slug']}.html",
        ))
    return rows
