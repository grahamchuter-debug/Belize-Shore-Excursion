"""Belize Shore Excursion site configuration."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://belizeshoreexcursion.com"
SITE = "Belize Shore Excursion"
DATE = "2026-06-06"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700"
    "&family=Source+Sans+3:wght@400;500;600;700&display=swap"
)
HERO_GRADIENT = (
    "linear-gradient(135deg, rgba(37, 99, 235, 0.75) 0%, "
    "rgba(249, 115, 22, 0.65) 50%, rgba(30, 58, 138, 0.55) 100%)"
)
ACCENT = "text-pr-300"

HOME_HERO = "images/hero-belize.png"
HOME_HERO_ALT = (
    "Turquoise Caribbean water and tropical coastline in Belize for cruise "
    "passengers planning shore excursions from Belize City cruise port"
)
PORT_IMG = "images/belize-cruise-port.png"
PORT_ALT = (
    "Belize City cruise port tender boats and Fort Street Tourism Village "
    "for cruise passenger shore excursion pickups in Belize"
)
PORT_ARRIVAL_IMG = "images/belize-port-arrival.png"
PORT_ARRIVAL_ALT = (
    "Cruise ship anchored off Belize City with tender boats shuttling "
    "passengers to Fort Street Tourism Village for shore excursions"
)
BEST_IMG = "images/best-belize-excursions.png"
BEST_ALT = (
    "Belize Barrier Reef and Mayan ruins representing the best Belize "
    "shore excursions for cruise passengers from Belize City port"
)
ONE_DAY_IMG = "images/one-day-belize.png"
ONE_DAY_ALT = (
    "Belize rainforest and Caribbean coastline for planning a one-day "
    "cruise ship shore excursion itinerary in Belize"
)
INTRO_IMG = "images/belize-intro.png"
INTRO_ALT = (
    "Belize tropical scenery with Caribbean water near Belize City cruise "
    "port for cave tubing, ruins and reef shore excursions"
)
CAVE_IMG = "images/belize-cave-tubing.png"
CAVE_ALT = (
    "Cave tubing through limestone caves in Belize rainforest on a "
    "shore excursion for cruise passengers from Belize City port"
)
ZIP_IMG = "images/belize-zip-line.png"
ZIP_ALT = (
    "Jungle zip line canopy adventure in Belize rainforest on a cruise "
    "passenger shore excursion from Belize City"
)
SNORKEL_IMG = "images/belize-snorkel.png"
SNORKEL_ALT = (
    "Snorkeling over coral reef and sea turtles in Belize Barrier Reef "
    "waters on a Caye Caulker shore excursion for cruise passengers"
)
BEACH_IMG = "images/belize-beach.png"
BEACH_ALT = (
    "White sand beach and turquoise water at Caye Caulker Belize on a "
    "cruise passenger beach break shore excursion"
)
ALTUN_HA_IMG = "images/altun-ha.png"
ALTUN_HA_ALT = (
    "Altun Ha Mayan temple ruins in Belize jungle visited on Mayan ruins "
    "shore excursions from Belize City cruise port"
)
LAMANAI_IMG = "images/lamanai.png"
LAMANAI_ALT = (
    "Lamanai Mayan archaeological site in Belize reached by river boat "
    "on a cruise passenger eco adventure shore excursion"
)
ZOO_IMG = "images/belize-zoo.png"
ZOO_ALT = (
    "Belize Zoo wildlife sanctuary with native animals on a family-friendly "
    "shore excursion for cruise passengers from Belize City"
)
JEEP_IMG = "images/belize-jeep.png"
JEEP_ALT = (
    "Jungle Jeep adventure through Belize rainforest countryside on a "
    "cruise passenger shore excursion from Belize City port"
)
PRIVATE_IMG = "images/belize-private.png"
PRIVATE_ALT = (
    "Private Belize shore excursion group with dedicated guide and vehicle "
    "for cruise passengers at Belize City cruise port"
)
FAQ_IMG = "images/belize-faq.png"
FAQ_ALT = (
    "Belize City waterfront and cruise port area for cruise passenger "
    "shore excursion planning and FAQ guidance"
)
RUINS_IMG = "images/belize-ruins.png"
RUINS_ALT = (
    "Ancient Mayan temple ruins surrounded by Belize rainforest on a "
    "cultural shore excursion for Belize cruise passengers"
)

CATEGORY_IMAGES = {
    "cave": (CAVE_IMG, CAVE_ALT),
    "zip": (ZIP_IMG, ZIP_ALT),
    "snorkel": (SNORKEL_IMG, SNORKEL_ALT),
    "beach": (BEACH_IMG, BEACH_ALT),
    "ruins": (ALTUN_HA_IMG, ALTUN_HA_ALT),
    "lamanai": (LAMANAI_IMG, LAMANAI_ALT),
    "zoo": (ZOO_IMG, ZOO_ALT),
    "jeep": (JEEP_IMG, JEEP_ALT),
    "city": (PORT_IMG, PORT_ALT),
    "wildlife": (ZOO_IMG, ZOO_ALT),
    "private": (PRIVATE_IMG, PRIVATE_ALT),
    "combo": (INTRO_IMG, INTRO_ALT),
}

ALL_IMAGES = [
    HOME_HERO, PORT_IMG, PORT_ARRIVAL_IMG, BEST_IMG, ONE_DAY_IMG, INTRO_IMG,
    CAVE_IMG, ZIP_IMG, SNORKEL_IMG, BEACH_IMG, ALTUN_HA_IMG, LAMANAI_IMG,
    ZOO_IMG, JEEP_IMG, PRIVATE_IMG, FAQ_IMG, RUINS_IMG,
]

SHIP_ICON = (
    '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">'
    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
    'd="M3 17h18M5 17l2-8h10l2 8M9 9l1-4h4l1 4"/></svg>'
)

PLACEHOLDER_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n"
    b"\xdb\x00\x00\x00\x00IEND\xaeB`\x82"
)

GUIDE_PAGES = [
    "belize-cruise-port-guide",
    "one-day-in-belize-from-a-cruise-ship",
    "best-belize-shore-excursions",
    "belize-private-tours",
    "belize-snorkeling-and-beach-excursions",
    "belize-mayan-ruins-excursions",
    "belize-shore-excursions-faq",
]
