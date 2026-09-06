#!/usr/bin/env python3
"""Build fully assembled static HTML for Belize Shore Excursion (World 2.0 Phase 13B)."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from belize_config import (  # noqa: E402
    ALTUN_HA_CLUSTER,
    BEST_ALT,
    BEST_IMG,
    CAVE_ALT,
    CAVE_IMG,
    DATE,
    DOMAIN,
    EMAIL,
    FAQ_ALT,
    FAQ_IMG,
    HOME_HERO,
    INTRO_ALT,
    INTRO_IMG,
    LAMANAI_ALT,
    LAMANAI_IMG,
    ONE_DAY_ALT,
    ONE_DAY_IMG,
    PORT_ALT,
    PORT_IMG,
    PRIORITY_A,
    PRIVATE_ALT,
    PRIVATE_IMG,
    RUINS_ALT,
    RUINS_IMG,
    SITE,
    SLUG_IMAGES,
    SNORKEL_ALT,
    SNORKEL_IMG,
)
from belize_pages import (  # noqa: E402
    FAQ_ITEMS,
    faq_body,
    faq_schema_entities,
    home_body,
    hub_best_body,
    hub_mayan_body,
    hub_private_body,
    hub_snorkel_body,
    not_found_body,
    one_day_body,
    port_guide_body,
    tour_body,
    trust_about_body,
    trust_contact_body,
    trust_methodology_body,
    trust_privacy_body,
    trust_terms_body,
)
from belize_shell import hero_home, hero_page, page_shell  # noqa: E402
from belize_tours_data import FEATURED_TOURS, TOUR_PAGES, TOURS  # noqa: E402

PROTECTED = [
    ("/", "index.html"),
    ("/best-belize-shore-excursions.html", "best-belize-shore-excursions.html"),
    ("/belize-cruise-port-guide.html", "belize-cruise-port-guide.html"),
    ("/one-day-in-belize-from-a-cruise-ship.html", "one-day-in-belize-from-a-cruise-ship.html"),
    ("/belize-private-tours.html", "belize-private-tours.html"),
    ("/belize-snorkeling-and-beach-excursions.html", "belize-snorkeling-and-beach-excursions.html"),
    ("/belize-mayan-ruins-excursions.html", "belize-mayan-ruins-excursions.html"),
    ("/belize-shore-excursions-faq.html", "belize-shore-excursions-faq.html"),
] + [(f"/{s}.html", f"{s}.html") for s in TOUR_PAGES]

TRUST = [
    ("about", "About Belize Shore Excursion", "Who we are and how this cruise planning guide works."),
    ("contact", "Contact Belize Shore Excursion", "Reach the Belize Shore Excursion editorial team."),
    ("privacy", "Privacy Policy", "How Belize Shore Excursion handles privacy for this editorial site."),
    ("terms", "Terms of Use", "Terms for using Belize Shore Excursion planning content."),
    ("methodology", "Methodology", "How Belize Shore Excursion researches and organises excursion guidance."),
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def crumbs(items: list[tuple[str, str]]) -> dict:
    elements = []
    for i, (name, url) in enumerate(items, start=1):
        elements.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@type": "BreadcrumbList", "itemListElement": elements}


def base_graph(title: str, description: str, canon: str) -> list:
    return [
        {
            "@type": "WebSite",
            "name": SITE,
            "url": f"{DOMAIN}/",
            "description": "Cruise-focused Belize shore excursion information and independent destination advice.",
            "inLanguage": "en",
            "publisher": {"@type": "Organization", "name": SITE, "url": f"{DOMAIN}/", "email": EMAIL},
        },
        {
            "@type": "Organization",
            "name": SITE,
            "url": f"{DOMAIN}/",
            "email": EMAIL,
            "description": (
                f"{SITE} provides cruise-focused excursion information and independent "
                "destination advice for passengers visiting Belize City. Not affiliated with any cruise line."
            ),
        },
        {
            "@type": "WebPage",
            "name": title.replace("&amp;", "&"),
            "url": canon,
            "description": description,
            "isPartOf": {"@type": "WebSite", "name": SITE, "url": f"{DOMAIN}/"},
            "inLanguage": "en",
        },
    ]


def tour_by_slug(slug: str) -> dict:
    for t in TOURS:
        if t["slug"] == slug:
            return t
    raise KeyError(slug)


def tour_priority(slug: str) -> str:
    if slug in PRIORITY_A:
        return "A"
    if slug in ALTUN_HA_CLUSTER or slug == "belize-party-bus":
        return "D"
    if slug in {
        "barrier-reef-snorkel",
        "xunantunich-and-cave-tubing",
        "private-tubing-expedition",
        "cave-tubing-and-jungle-trek-with-lunch",
        "jungle-zip-line",
        "belize-city-and-zoo-combo",
        "belize-zoo-and-jeep-adventure",
        "zip-line-and-belize-zoo-with-lunch",
        "howler-monkey-sanctuary",
        "baboon-sanctuary-and-jeep-adventure",
        "expedition-to-crooked-tree-wildlife-sanctuary",
    }:
        return "B"
    return "C"


def build_home() -> None:
    title = "Belize Shore Excursion | Cave Tubing, Ruins &amp; Reef from Belize City"
    desc = (
        "Plan Belize shore excursions for cruise passengers — cave tubing, Altun Ha Mayan ruins, "
        "barrier reef snorkelling and beach breaks from Belize City's tender port."
    )
    canon = f"{DOMAIN}/"
    schema = base_graph(title.replace("&amp;", "&"), desc, canon)
    html = page_shell(
        title=title,
        description=desc,
        canonical=canon,
        og_image=HOME_HERO,
        nav_key="home",
        hero=hero_home(),
        body=home_body(),
        schema=schema,
        preload=HOME_HERO,
    )
    write(ROOT / "index.html", html)


def build_hub(
    *,
    file: str,
    nav_key: str,
    title: str,
    description: str,
    h1: str,
    lead: str,
    image: str,
    alt: str,
    crumb: str,
    body: str,
    cta_href: str,
    cta_label: str,
    crumb_schema: list[tuple[str, str]],
) -> None:
    canon = f"{DOMAIN}/{file}"
    schema = base_graph(title.replace("&amp;", "&"), description, canon)
    schema.append(crumbs(crumb_schema))
    html = page_shell(
        title=title,
        description=description,
        canonical=canon,
        og_image=image,
        nav_key=nav_key,
        hero=hero_page(
            title=h1,
            lead=lead,
            image=image,
            alt=alt,
            crumb=crumb,
            cta_href=cta_href,
            cta_label=cta_label,
        ),
        body=body,
        schema=schema,
        preload=image,
    )
    write(ROOT / file, html)


def build_guides() -> None:
    build_hub(
        file="best-belize-shore-excursions.html",
        nav_key="excursions",
        title="Best Belize Shore Excursions | Compare Cave, Ruins &amp; Reef Options",
        description="Compare Belize shore excursion themes for cruise passengers — cave tubing, Mayan ruins, reef snorkel and beach breaks timed around a Belize City tender day.",
        h1="Best Belize Shore Excursions for Cruise Passengers",
        lead="Compare the main Belize City port-day themes, then drill into individual guides that match your energy, group size and all-aboard window.",
        image=BEST_IMG,
        alt=BEST_ALT,
        crumb="Best excursions",
        body=hub_best_body(TOURS),
        cta_href="/belize-cruise-port-guide.html",
        cta_label="Plan with the port guide",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("Best excursions", f"{DOMAIN}/best-belize-shore-excursions.html")],
    )
    build_hub(
        file="belize-mayan-ruins-excursions.html",
        nav_key="ruins",
        title="Belize Mayan Ruins Excursions | Altun Ha, Lamanai &amp; More",
        description="Explore Mayan ruins shore excursions from Belize City cruise port — Altun Ha, Lamanai, Cahal Pech and Xunantunich options for cruise schedules.",
        h1="Belize Mayan Ruins Excursions from the Cruise Port",
        lead="Choose between nearer Altun Ha day trips and longer river or inland routes to Lamanai, Cahal Pech or Xunantunich.",
        image=RUINS_IMG,
        alt=RUINS_ALT,
        crumb="Mayan ruins",
        body=hub_mayan_body(TOURS),
        cta_href="/best-belize-shore-excursions.html",
        cta_label="Compare all themes",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("Mayan ruins", f"{DOMAIN}/belize-mayan-ruins-excursions.html")],
    )
    build_hub(
        file="belize-snorkeling-and-beach-excursions.html",
        nav_key="snorkel",
        title="Belize Snorkeling and Beach Excursions | Reef &amp; Island Time",
        description="Plan Belize snorkeling and beach shore excursions from Belize City — Barrier Reef, Shark Ray Alley, Caye Caulker and coastal beach breaks.",
        h1="Belize Snorkeling and Beach Excursions",
        lead="Match reef time, island pace and boat logistics to your tender schedule from Fort Street Tourism Village.",
        image=SNORKEL_IMG,
        alt=SNORKEL_ALT,
        crumb="Snorkel &amp; beach",
        body=hub_snorkel_body(TOURS),
        cta_href="/one-day-in-belize-from-a-cruise-ship.html",
        cta_label="Plan one day in Belize",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("Snorkel & beach", f"{DOMAIN}/belize-snorkeling-and-beach-excursions.html")],
    )
    build_hub(
        file="belize-private-tours.html",
        nav_key="private",
        title="Belize Private Tours | Small-Group &amp; Private Shore Excursions",
        description="Explore private and small-group Belize shore excursion styles from Belize City cruise port — private tubing, jeep days and flexible pacing.",
        h1="Belize Private Tours for Cruise Passengers",
        lead="Private and small-group formats can help families and friends keep a shared pace on a tender-port day.",
        image=PRIVATE_IMG,
        alt=PRIVATE_ALT,
        crumb="Private tours",
        body=hub_private_body(TOURS),
        cta_href="/best-belize-shore-excursions.html",
        cta_label="Compare excursions",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("Private tours", f"{DOMAIN}/belize-private-tours.html")],
    )
    build_hub(
        file="belize-cruise-port-guide.html",
        nav_key="port",
        title="Belize Cruise Port Guide | Tender Logistics at Belize City",
        description="Belize City cruise port guide for passengers — tendering to Fort Street Tourism Village, tour pickup timing, distances and return planning.",
        h1="Belize Cruise Port Guide",
        lead="Ships typically anchor offshore and tender into Fort Street Tourism Village. Use this guide to plan shore time around tender queues and inland travel.",
        image=PORT_IMG,
        alt=PORT_ALT,
        crumb="Port guide",
        body=port_guide_body(),
        cta_href="/one-day-in-belize-from-a-cruise-ship.html",
        cta_label="Explore a one-day plan",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("Port guide", f"{DOMAIN}/belize-cruise-port-guide.html")],
    )
    build_hub(
        file="one-day-in-belize-from-a-cruise-ship.html",
        nav_key="one-day",
        title="One Day in Belize from a Cruise Ship | Port Day Planning",
        description="Plan one day in Belize from a cruise ship — sample timelines for cave tubing, ruins and reef themes around a Belize City tender call.",
        h1="One Day in Belize from a Cruise Ship",
        lead="Build a realistic port-day outline that leaves buffer for tenders, inland roads and your ship's all-aboard time.",
        image=ONE_DAY_IMG,
        alt=ONE_DAY_ALT,
        crumb="One day in Belize",
        body=one_day_body(),
        cta_href="/best-belize-shore-excursions.html",
        cta_label="Compare excursion themes",
        crumb_schema=[("Home", f"{DOMAIN}/"), ("One day in Belize", f"{DOMAIN}/one-day-in-belize-from-a-cruise-ship.html")],
    )

    faq_title = "Belize Shore Excursions FAQ | Tender Port Planning Answers"
    faq_desc = (
        "Answers to common Belize shore excursion questions for cruise passengers — tendering, timing, "
        "themes and how to choose between cave, ruins and reef days."
    )
    faq_canon = f"{DOMAIN}/belize-shore-excursions-faq.html"
    faq_schema = base_graph(faq_title.replace("&amp;", "&"), faq_desc, faq_canon)
    faq_schema.append(crumbs([("Home", f"{DOMAIN}/"), ("FAQ", faq_canon)]))
    faq_schema.append({"@type": "FAQPage", "mainEntity": faq_schema_entities()})
    write(
        ROOT / "belize-shore-excursions-faq.html",
        page_shell(
            title=faq_title,
            description=faq_desc,
            canonical=faq_canon,
            og_image=FAQ_IMG,
            nav_key="faq",
            hero=hero_page(
                title="Belize Shore Excursions FAQ",
                lead="Practical answers for cruise passengers planning a Belize City tender day.",
                image=FAQ_IMG,
                alt=FAQ_ALT,
                crumb="FAQ",
                cta_href="/belize-cruise-port-guide.html",
                cta_label="Read the port guide",
            ),
            body=faq_body(),
            schema=faq_schema,
            preload=FAQ_IMG,
        ),
    )


def build_tours() -> None:
    for tour in TOURS:
        slug = tour["slug"]
        pri = tour_priority(slug)
        img, alt = SLUG_IMAGES.get(slug, (INTRO_IMG, INTRO_ALT))
        title = f"{tour['title']} | Belize Shore Excursion Guide"
        desc = (
            f"{tour['seg_desc']} Editorial cruise-port guide for passengers visiting Belize City — "
            f"timing context for a typical tender day. Not a booking page."
        )
        # Soften any residual commerce tone in meta
        desc = desc.replace("book most", "consider").replace("booking", "planning")
        file = f"{slug}.html"
        canon = f"{DOMAIN}/{file}"
        schema = base_graph(title, desc, canon)
        schema.append(
            crumbs(
                [
                    ("Home", f"{DOMAIN}/"),
                    ("Best excursions", f"{DOMAIN}/best-belize-shore-excursions.html"),
                    (tour["title"], canon),
                ]
            )
        )
        # TouristTrip only when descriptive and without offers
        schema.append(
            {
                "@type": "TouristTrip",
                "name": tour["title"],
                "description": tour["seg_desc"],
                "touristType": "Cruise passengers",
                "itinerary": {
                    "@type": "ItemList",
                    "name": f"{tour['title']} themes",
                    "itemListElement": [
                        {"@type": "ListItem", "position": 1, "name": tour["category"]},
                        {"@type": "ListItem", "position": 2, "name": tour["duration"]},
                    ],
                },
            }
        )
        hub_map = {
            "cave": "/belize-cave-tubing.html",
            "zip": "/jungle-zip-line.html",
            "snorkel": "/belize-snorkeling-and-beach-excursions.html",
            "beach": "/belize-snorkeling-and-beach-excursions.html",
            "ruins": "/belize-mayan-ruins-excursions.html",
            "lamanai": "/belize-mayan-ruins-excursions.html",
            "zoo": "/best-belize-shore-excursions.html",
            "jeep": "/best-belize-shore-excursions.html",
            "city": "/belize-cruise-port-guide.html",
            "wildlife": "/best-belize-shore-excursions.html",
            "private": "/belize-private-tours.html",
            "combo": "/best-belize-shore-excursions.html",
        }
        write(
            ROOT / file,
            page_shell(
                title=title,
                description=desc,
                canonical=canon,
                og_image=img,
                nav_key="tour",
                hero=hero_page(
                    title=tour["title"],
                    lead=tour["seg_desc"],
                    image=img,
                    alt=alt,
                    crumb=f'<a href="/best-belize-shore-excursions.html">Excursions</a> · {tour["title"]}',
                    cta_href=hub_map.get(tour["category"], "/best-belize-shore-excursions.html"),
                    cta_label="Explore related guides",
                ),
                body=tour_body(tour, pri),
                schema=schema,
                preload=img,
            ),
        )


def build_trust() -> None:
    bodies = {
        "about": trust_about_body(),
        "contact": trust_contact_body(),
        "privacy": trust_privacy_body(),
        "terms": trust_terms_body(),
        "methodology": trust_methodology_body(),
    }
    images = {
        "about": (INTRO_IMG, INTRO_ALT),
        "contact": (PORT_IMG, PORT_ALT),
        "privacy": (FAQ_IMG, FAQ_ALT),
        "terms": (FAQ_IMG, FAQ_ALT),
        "methodology": (BEST_IMG, BEST_ALT),
    }
    for slug, label, desc in TRUST:
        img, alt = images[slug]
        canon = f"{DOMAIN}/{slug}/"
        title = f"{label} | {SITE}"
        schema = base_graph(label, desc, canon)
        schema.append(crumbs([("Home", f"{DOMAIN}/"), (label, canon)]))
        write(
            ROOT / slug / "index.html",
            page_shell(
                title=title,
                description=desc,
                canonical=canon,
                og_image=img,
                nav_key=slug,
                hero=hero_page(
                    title=label,
                    lead=desc,
                    image=img,
                    alt=alt,
                    crumb=label,
                ),
                body=bodies[slug],
                schema=schema,
                preload=img,
            ),
        )


def build_404() -> None:
    title = "Page not found | Belize Shore Excursion"
    desc = "The page you requested is not available. Explore Belize shore excursion planning guides from the homepage."
    html = page_shell(
        title=title,
        description=desc,
        canonical=f"{DOMAIN}/404.html",
        og_image=HOME_HERO,
        nav_key="404",
        hero="",
        body=not_found_body(),
        schema=[
            {
                "@type": "WebPage",
                "name": "Page not found",
                "url": f"{DOMAIN}/404.html",
                "description": desc,
            }
        ],
        robots="noindex, follow",
    )
    # Ensure 404 does not claim homepage canonical
    assert 'rel="canonical" href="https://belizeshoreexcursion.com/"' not in html
    write(ROOT / "404.html", html)


def build_sitemap_robots() -> None:
    urls = [f"{DOMAIN}/"]
    for path, _ in PROTECTED[1:]:
        urls.append(f"{DOMAIN}{path}")
    for slug, _, _ in TRUST:
        urls.append(f"{DOMAIN}/{slug}/")
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append("  <url>")
        body.append(f"    <loc>{u}</loc>")
        body.append(f"    <lastmod>{DATE}</lastmod>")
        body.append("  </url>")
    body.append("</urlset>")
    body.append("")
    write(ROOT / "sitemap.xml", "\n".join(body))
    write(
        ROOT / "robots.txt",
        f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""",
    )


def quarantine_antigua() -> None:
    dest = ROOT / "quarantine" / "antigua"
    dest.mkdir(parents=True, exist_ok=True)
    names = [
        "antigua-beaches.png",
        "antigua-cruise-port.png",
        "antigua-intro.png",
        "antigua-kayak-snorkel.png",
        "antigua-port-arrival.png",
        "best-antigua-excursions.png",
        "cades-reef.png",
        "classic-beach-day.png",
        "half-day-kayak-snorkel.png",
        "hero-antigua.png",
        "history-culture-tour.png",
        "nelsons-dockyard.png",
        "one-day-antigua.png",
        "panoramic-antigua.png",
        "shirley-heights.png",
        "the-antiguan-experience.png",
    ]
    for name in names:
        src = ROOT / "images" / name
        if src.exists():
            shutil.move(str(src), str(dest / name))
            print(f"  quarantined images/{name}")


def write_manifest() -> None:
    routes = []
    for path, file in PROTECTED:
        kind = "home" if path == "/" else (
            "hub" if file.startswith(("best-", "belize-mayan", "belize-snorkel", "belize-private")) else
            "planning" if file in {
                "belize-cruise-port-guide.html",
                "one-day-in-belize-from-a-cruise-ship.html",
                "belize-shore-excursions-faq.html",
            } else "product"
        )
        entry = {"path": path, "file": file, "kind": kind, "sitemap": True}
        if kind == "product":
            slug = file.replace(".html", "")
            entry["priority"] = tour_priority(slug)
            if slug in ALTUN_HA_CLUSTER:
                entry["cluster"] = "altun-ha"
            if slug == "belize-party-bus":
                entry["cluster"] = "party-bus"
        routes.append(entry)
    manifest = {
        "destination": SITE,
        "domain": DOMAIN,
        "canonical_host": "belizeshoreexcursion.com",
        "html_policy": "apex + .html",
        "phase": "13B",
        "expected_count": 42,
        "routes": routes,
        "trust_routes": [
            {"path": f"/{s}/", "file": f"{s}/index.html", "sitemap": True} for s, _, _ in TRUST
        ],
        "featured": FEATURED_TOURS,
        "faq_count": len(FAQ_ITEMS),
    }
    write(ROOT / "scripts" / "protected_routes.json", json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    print("Building Belize Shore Excursion World 2.0…")
    quarantine_antigua()
    build_home()
    build_guides()
    build_tours()
    build_trust()
    build_404()
    build_sitemap_robots()
    write_manifest()

    missing = []
    for path, file in PROTECTED:
        if not (ROOT / file).exists():
            missing.append(file)
    if missing:
        raise SystemExit(f"Missing protected files: {missing}")
    print(f"OK: {len(PROTECTED)} protected routes generated + trust + 404")


if __name__ == "__main__":
    main()
