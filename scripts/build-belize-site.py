#!/usr/bin/env python3
"""Build fully assembled static HTML for Belize Shore Excursion (World 2.0 / Phase 13B)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from belize_config import (  # noqa: E402
    BEST_ALT,
    BEST_IMG,
    DOMAIN,
    EMAIL,
    FAQ_ALT,
    FAQ_IMG,
    HOME_HERO,
    HOME_HERO_ALT,
    ONE_DAY_ALT,
    ONE_DAY_IMG,
    PORT_ALT,
    PORT_IMG,
    PRIVATE_ALT,
    PRIVATE_IMG,
    RUINS_ALT,
    RUINS_IMG,
    SITE,
    SLUG_IMAGES,
    SNORKEL_ALT,
    SNORKEL_IMG,
    CATEGORY_IMAGES,
    INTRO_IMG,
    INTRO_ALT,
)
from belize_pages import (  # noqa: E402
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
    product_body,
    trust_about_body,
    trust_contact_body,
    trust_methodology_body,
    trust_privacy_body,
    trust_terms_body,
)

from belize_shell import hero_home, hero_page, page_shell  # noqa: E402
from belize_tours_data import TOURS  # noqa: E402

MANIFEST = json.loads((ROOT / "scripts" / "protected_routes.json").read_text(encoding="utf-8"))
PRIORITY_BY_SLUG = {
    r["file"].removesuffix(".html"): r.get("priority", "B")
    for r in MANIFEST["routes"]
    if r.get("kind") == "product"
}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print(f"  wrote {path.relative_to(ROOT)}")


def org_graph() -> list:
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
    ]


def build_home() -> None:
    schema = org_graph()
    html = page_shell(
        title="Belize Shore Excursion | Cave Tubing, Ruins & Reef from Belize City",
        description=(
            "Plan Belize shore excursions for cruise passengers — cave tubing, Altun Ha, "
            "barrier reef snorkelling and beach breaks from Belize City's tender port."
        ),
        canonical="/",
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
    title: str,
    description: str,
    nav_key: str,
    hero_title: str,
    lead: str,
    image: str,
    alt: str,
    crumb: str,
    body: str,
    cta_href: str,
) -> None:
    html = page_shell(
        title=title,
        description=description,
        canonical=f"/{file}",
        og_image=image,
        nav_key=nav_key,
        hero=hero_page(
            title=hero_title,
            lead=lead,
            image=image,
            alt=alt,
            crumb=crumb,
            cta_href=cta_href,
            cta_label="Explore guides",
        ),
        body=body,
        schema=org_graph(),
    )
    write(ROOT / file, html)


def build_planning_pages() -> None:
    build_hub(
        file="best-belize-shore-excursions.html",
        title="Best Belize Shore Excursions | Compare Cruise Day Options",
        description="Compare Belize shore excursion themes for cruise passengers — cave tubing, Mayan ruins, reef snorkel, wildlife and private touring from Belize City.",
        nav_key="excursions",
        hero_title="Best Belize Shore Excursions for Cruise Guests",
        lead="A comparison hub for cruise-day themes from Belize City's tender port — not a popularity ranking.",
        image=BEST_IMG,
        alt=BEST_ALT,
        crumb="Best excursions",
        body=hub_best_body(TOURS),
        cta_href="/belize-cruise-port-guide.html",
    )
    build_hub(
        file="belize-mayan-ruins-excursions.html",
        title="Belize Mayan Ruins Excursions | Altun Ha, Lamanai & More",
        description="Plan Mayan ruins shore excursions from Belize City — Altun Ha, Lamanai, Cahal Pech and combo days that fit a cruise tender schedule.",
        nav_key="ruins",
        hero_title="Belize Mayan Ruins Excursions",
        lead="Temple days inland from the tender pier — from compact Altun Ha visits to river-access Lamanai.",
        image=RUINS_IMG,
        alt=RUINS_ALT,
        crumb="Mayan ruins",
        body=hub_mayan_body(TOURS),
        cta_href="/best-belize-shore-excursions.html",
    )
    build_hub(
        file="belize-snorkeling-and-beach-excursions.html",
        title="Belize Snorkeling and Beach Excursions | Reef & Island Days",
        description="Plan Belize Barrier Reef snorkel and beach break shore excursions from Belize City — Caye Caulker, Shark Ray Alley and island time for cruise guests.",
        nav_key="snorkel",
        hero_title="Belize Snorkeling and Beach Excursions",
        lead="Boat days toward reef and island shoreline when you want Caribbean water over inland roads.",
        image=SNORKEL_IMG,
        alt=SNORKEL_ALT,
        crumb="Snorkel &amp; beach",
        body=hub_snorkel_body(TOURS),
        cta_href="/best-belize-shore-excursions.html",
    )
    build_hub(
        file="belize-private-tours.html",
        title="Belize Private Tours | Flexible Cruise Shore Excursions",
        description="Explore private Belize shore excursion formats for cruise passengers — private cave tubing and tailored pacing from Belize City's tender port.",
        nav_key="private",
        hero_title="Belize Private Tours for Cruise Guests",
        lead="Editorial guides to private-format days when your group wants more control over pace and stops.",
        image=PRIVATE_IMG,
        alt=PRIVATE_ALT,
        crumb="Private tours",
        body=hub_private_body(TOURS),
        cta_href="/best-belize-shore-excursions.html",
    )
    build_hub(
        file="belize-cruise-port-guide.html",
        title="Belize Cruise Port Guide | Tender Port & Fort Street Village",
        description="Belize City cruise port guide for tender arrivals at Fort Street Tourism Village — timing, transfers and how shore days usually work.",
        nav_key="port",
        hero_title="Belize Cruise Port Guide",
        lead="Ships anchor offshore; passengers tender to Fort Street Tourism Village on a typical six-to-ten-hour call.",
        image=PORT_IMG,
        alt=PORT_ALT,
        crumb="Port guide",
        body=port_guide_body(),
        cta_href="/one-day-in-belize-from-a-cruise-ship.html",
    )
    build_hub(
        file="one-day-in-belize-from-a-cruise-ship.html",
        title="One Day in Belize from a Cruise Ship | Port Day Planning",
        description="Plan one day in Belize from a cruise ship — how to choose between cave tubing, ruins, reef and city options within a tender port window.",
        nav_key="one-day",
        hero_title="One Day in Belize from a Cruise Ship",
        lead="A practical way to choose one coherent theme for a Belize City tender day.",
        image=ONE_DAY_IMG,
        alt=ONE_DAY_ALT,
        crumb="One day in Belize",
        body=one_day_body(),
        cta_href="/best-belize-shore-excursions.html",
    )

    faq_schema = org_graph() + [
        {"@type": "FAQPage", "mainEntity": faq_schema_entities()},
    ]
    html = page_shell(
        title="Belize Shore Excursions FAQ | Tender Port & Cruise Day Answers",
        description="FAQ for Belize cruise shore excursions — tender port logistics, timing, currency, ruins distances and reef days from Belize City.",
        canonical="/belize-shore-excursions-faq.html",
        og_image=FAQ_IMG,
        nav_key="faq",
        hero=hero_page(
            title="Belize Shore Excursions FAQ",
            lead="Straight answers for cruise passengers planning a Belize City tender day.",
            image=FAQ_IMG,
            alt=FAQ_ALT,
            crumb="FAQ",
            cta_href="/belize-cruise-port-guide.html",
            cta_label="Explore the port guide",
        ),
        body=faq_body(),
        schema=faq_schema,
    )
    write(ROOT / "belize-shore-excursions-faq.html", html)


def tour_meta(tour: dict) -> tuple[str, str, str, str]:
    img, alt = SLUG_IMAGES.get(
        tour["slug"],
        CATEGORY_IMAGES.get(tour["category"], (INTRO_IMG, INTRO_ALT)),
    )
    title = f"{tour['title']} | Belize Shore Excursion Guide"
    desc = (
        f"Editorial guide to {tour['title']} for Belize cruise passengers — "
        f"{tour['seg_desc'].rstrip('.')}."
    )
    if len(desc) > 158:
        desc = desc[:155].rstrip() + "…"
    return title, desc, img, alt


def build_products() -> None:
    for tour in TOURS:
        title, desc, img, alt = tour_meta(tour)
        theme_href = {
            "cave": "/best-belize-shore-excursions.html",
            "zip": "/best-belize-shore-excursions.html",
            "combo": "/best-belize-shore-excursions.html",
            "snorkel": "/belize-snorkeling-and-beach-excursions.html",
            "beach": "/belize-snorkeling-and-beach-excursions.html",
            "ruins": "/belize-mayan-ruins-excursions.html",
            "lamanai": "/belize-mayan-ruins-excursions.html",
            "private": "/belize-private-tours.html",
        }.get(tour["category"], "/best-belize-shore-excursions.html")
        html = page_shell(
            title=title,
            description=desc,
            canonical=f"/{tour['slug']}.html",
            og_image=img,
            nav_key="product",
            hero=hero_page(
                title=tour["title"],
                lead=tour["seg_desc"],
                image=img,
                alt=alt,
                crumb=f'<a href="{theme_href}">Guides</a> · {tour["title"]}',
                cta_href=theme_href,
                cta_label="Compare related guides",
            ),
            body=product_body(tour, PRIORITY_BY_SLUG.get(tour["slug"], "B")),
            schema=org_graph(),
        )
        write(ROOT / f"{tour['slug']}.html", html)


def build_trust() -> None:
    pages = [
        (
            "about",
            "About Belize Shore Excursion",
            "About Belize Shore Excursion — an independent cruise passenger planning guide for Belize City shore days.",
            "About",
            trust_about_body(),
        ),
        (
            "contact",
            "Contact Belize Shore Excursion",
            "Contact Belize Shore Excursion at hello@belizeshoreexcursion.com for editorial questions about this cruise planning guide.",
            "Contact",
            trust_contact_body(),
        ),
        (
            "privacy",
            "Privacy Policy | Belize Shore Excursion",
            "Privacy policy for Belize Shore Excursion — how this independent cruise planning website handles information.",
            "Privacy",
            trust_privacy_body(),
        ),
        (
            "terms",
            "Terms of Use | Belize Shore Excursion",
            "Terms of use for Belize Shore Excursion — editorial cruise planning information, not a booking marketplace.",
            "Terms",
            trust_terms_body(),
        ),
        (
            "methodology",
            "Methodology | Belize Shore Excursion",
            "How Belize Shore Excursion researches and organises cruise shore excursion guides for Belize City.",
            "Methodology",
            trust_methodology_body(),
        ),
    ]
    for slug, title, description, crumb, body in pages:
        html = page_shell(
            title=title,
            description=description,
            canonical=f"/{slug}/",
            og_image=HOME_HERO,
            nav_key=slug,
            hero=hero_page(
                title=crumb,
                lead=description,
                image=HOME_HERO,
                alt=HOME_HERO_ALT,
                crumb=crumb,
            ),
            body=body,
            schema=org_graph(),
        )
        # compact hero for trust
        html = html.replace('class="hero hero--page"', 'class="hero hero--page hero--compact"', 1)
        write(ROOT / slug / "index.html", html)


def build_404() -> None:
    html = page_shell(
        title="Page not found | Belize Shore Excursion",
        description="The page you requested was not found on Belize Shore Excursion.",
        canonical="/404.html",
        og_image=HOME_HERO,
        nav_key="404",
        hero="",
        body=not_found_body(),
        schema=org_graph(),
        robots="noindex, follow",
    )
    # 404 should not claim homepage canonical
    html = html.replace(
        f'<link rel="canonical" href="{DOMAIN}/404.html" />',
        f'<link rel="canonical" href="{DOMAIN}/404.html" />\n  <meta name="robots" content="noindex, follow" />',
    )
    write(ROOT / "404.html", html)


def build_sitemap_robots() -> None:
    urls: list[tuple[str, str, str]] = []
    for route in MANIFEST["routes"]:
        if not route.get("sitemap", True):
            continue
        path = route["path"]
        loc = f"{DOMAIN}/" if path == "/" else f"{DOMAIN}{path}"
        priority = "1.0" if path == "/" else ("0.9" if route["kind"] in {"hub", "product"} else "0.8")
        urls.append((loc, priority, "monthly" if path != "/" else "weekly"))
    for route in MANIFEST["trust_routes"]:
        urls.append((f"{DOMAIN}{route['path']}", "0.5", "yearly"))

    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, pri, freq in urls:
        body.append("  <url>")
        body.append(f"    <loc>{loc}</loc>")
        body.append(f"    <changefreq>{freq}</changefreq>")
        body.append(f"    <priority>{pri}</priority>")
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


def verify_protected_count() -> None:
    expected = {r["file"] for r in MANIFEST["routes"]}
    missing = [f for f in expected if not (ROOT / f).exists()]
    if missing:
        raise SystemExit(f"Missing protected files: {missing}")
    if len(expected) != 42:
        raise SystemExit(f"Manifest expected 42, got {len(expected)}")
    print(f"  verified {len(expected)}/42 protected files present")


def main() -> None:
    print("Building Belize Shore Excursion World 2.0…")
    build_home()
    build_planning_pages()
    build_products()
    build_trust()
    build_404()
    build_sitemap_robots()
    verify_protected_count()
    print("Build complete.")


if __name__ == "__main__":
    main()
