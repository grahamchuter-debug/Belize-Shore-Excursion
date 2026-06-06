#!/usr/bin/env python3
"""Generate Belize Shore Excursion static site files."""
from pathlib import Path

from belize_config import (
    ACCENT,
    ALL_IMAGES,
    BEST_ALT,
    BEST_IMG,
    CATEGORY_IMAGES,
    DATE,
    DOMAIN,
    FAQ_ALT,
    FAQ_IMG,
    HERO_GRADIENT,
    HOME_HERO,
    HOME_HERO_ALT,
    INTRO_ALT,
    INTRO_IMG,
    ONE_DAY_ALT,
    ONE_DAY_IMG,
    PLACEHOLDER_PNG,
    PORT_ALT,
    PORT_IMG,
    PORT_ARRIVAL_ALT,
    PORT_ARRIVAL_IMG,
    PRIVATE_ALT,
    PRIVATE_IMG,
    ROOT,
    RUINS_ALT,
    RUINS_IMG,
    SITE,
    SNORKEL_ALT,
    SNORKEL_IMG,
)
from belize_guides import all_guide_content, home_faq_data
from belize_helpers import hero_inner, hero_wave, home_schema, page_shell, tourist_trip_schema
from belize_tours import all_tour_content
from belize_tours_data import SITEMAP_PAGES, TOURS


def write(path: str, content: str) -> None:
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"  wrote {path}")


def hero_home() -> str:
    return f"""  <section class="site-hero">
    <div class="absolute inset-0 hero-bg" style="background-image: {HERO_GRADIENT}, url('{HOME_HERO}');" role="img" aria-label="{HOME_HERO_ALT}"></div>
    <div class="site-hero__inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="max-w-3xl">
        <div class="site-hero__eyebrow inline-flex items-center gap-2 bg-white/15 backdrop-blur-sm border border-white/30 rounded-full px-4 py-1.5 mb-3">
          <span class="w-2 h-2 rounded-full bg-pr-400 animate-pulse"></span>
          <span class="text-white/90 text-xs font-semibold tracking-widest uppercase">Belize City · Tender Port</span>
        </div>
        <h1 class="site-hero__title text-4xl sm:text-5xl lg:text-[3.25rem] font-display font-bold text-white leading-tight mb-3">
          Belize Shore<br/><span class="{ACCENT}">Excursions</span><br/>from the Cruise Port
        </h1>
        <p class="site-hero__lead text-base sm:text-lg text-white/85 font-light leading-relaxed mb-5 max-w-2xl">
          Cave tubing, Mayan ruins, barrier reef snorkelling and beach breaks — the shore excursions cruise passengers book most from Belize City, Belize.
        </p>
        <div class="site-hero__actions flex flex-col sm:flex-row gap-3">
          <a href="best-belize-shore-excursions.html" class="btn-primary inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm shadow-xl">Compare Excursions</a>
          <a href="belize-cave-tubing.html" class="btn-outline inline-flex items-center justify-center gap-2 text-white font-semibold px-7 py-3 rounded-full text-sm">Cave Tubing</a>
        </div>
        <div class="site-hero__tags flex flex-wrap gap-2 mt-5 pt-4 border-t border-white/20">
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Cave Tubing</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Altun Ha</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Barrier Reef</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">Cruise Passengers</span>
          <span class="inline-flex items-center bg-white/10 border border-white/25 rounded-full px-3.5 py-1.5 text-xs font-semibold text-white">BZD &amp; USD</span>
        </div>
      </div>
    </div>
    {hero_wave()}
  </section>"""


def tour_hero(tour: dict) -> str:
    img, alt = CATEGORY_IMAGES.get(tour["category"], (INTRO_IMG, INTRO_ALT))
    title_parts = tour["title"].replace(" and ", " &amp; ").split(" ", 2)
    if len(title_parts) >= 2:
        h1 = f"{title_parts[0]}<br/><span class=\"{ACCENT}\">{title_parts[1]}</span>"
        if len(title_parts) > 2:
            h1 += f"<br/>{title_parts[2]}"
    else:
        h1 = tour["title"]
    return hero_inner(
        f"{tour['duration']} · {tour['activity']}",
        h1,
        f"{tour['seg_desc']} Shore excursion for Belize cruise passengers with port pickup and return-to-ship timing.",
        img,
        f"{tour['title']} Belize shore excursion hero image for cruise passengers from Belize City port",
        breadcrumb=tour["title"],
    )


def nav_html() -> str:
    return f"""<nav class="fixed top-0 left-0 right-0 z-50 bg-white/90 border-b border-pr-100 shadow-sm">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-12">
      <a href="index.html" class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full btn-ocean flex items-center justify-center">
          <svg class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
          </svg>
        </div>
        <span class="font-display font-semibold text-ocean-800 text-base leading-tight">Belize Shore<br/><span class="text-[10px] font-body font-normal text-pr-600 tracking-widest uppercase">Excursion</span></span>
      </a>
      <div class="hidden lg:flex items-center gap-5 text-sm font-medium">
        <a href="index.html" data-nav="home" class="text-gray-600 hover:text-ocean-600 transition-colors">Home</a>
        <a href="best-belize-shore-excursions.html" data-nav="excursions" class="text-gray-600 hover:text-ocean-600 transition-colors">Excursions</a>
        <a href="belize-mayan-ruins-excursions.html" data-nav="ruins" class="text-gray-600 hover:text-ocean-600 transition-colors">Ruins</a>
        <a href="belize-snorkeling-and-beach-excursions.html" data-nav="snorkel" class="text-gray-600 hover:text-ocean-600 transition-colors">Snorkel</a>
        <a href="belize-private-tours.html" data-nav="private" class="text-gray-600 hover:text-ocean-600 transition-colors">Private</a>
        <a href="belize-cruise-port-guide.html" data-nav="port" class="text-gray-600 hover:text-ocean-600 transition-colors">Port Guide</a>
      </div>
      <a href="best-belize-shore-excursions.html" class="hidden md:inline-flex items-center gap-2 btn-ocean text-white text-sm font-semibold px-4 py-2 rounded-full shadow-md">
        Compare Tours
      </a>
      <button type="button" class="lg:hidden p-2 rounded-lg text-gray-600 hover:bg-sand-50" aria-label="Open menu">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
      </button>
    </div>
  </div>
</nav>
"""


def footer_html() -> str:
    featured = [t for t in TOURS if t.get("featured")][:6]
    tour_links = "".join(
        f'<li><a href="{t["slug"]}.html" class="hover:text-white transition-colors">{t["title"]}</a></li>'
        for t in featured
    )
    return f"""  <footer class="bg-gray-900 text-gray-400 py-14">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        <div class="sm:col-span-2 lg:col-span-1">
          <a href="index.html" class="font-display font-semibold text-white text-lg">{SITE}</a>
          <p class="mt-3 text-sm leading-relaxed">Planning guide for cruise visitors to Belize City, Belize. Not affiliated with any cruise line.</p>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Excursions</h3>
          <ul class="space-y-2 text-sm">
            {tour_links}
          </ul>
        </div>
        <div>
          <h3 class="text-white text-sm font-semibold uppercase tracking-wider mb-4">Guides</h3>
          <ul class="space-y-2 text-sm">
            <li><a href="best-belize-shore-excursions.html" class="hover:text-white transition-colors">Belize Shore Excursions</a></li>
            <li><a href="belize-cruise-port-guide.html" class="hover:text-white transition-colors">Cruise Port Guide</a></li>
            <li><a href="one-day-in-belize-from-a-cruise-ship.html" class="hover:text-white transition-colors">One Day in Belize</a></li>
            <li><a href="belize-snorkeling-and-beach-excursions.html" class="hover:text-white transition-colors">Snorkel &amp; Beach</a></li>
            <li><a href="belize-mayan-ruins-excursions.html" class="hover:text-white transition-colors">Mayan Ruins</a></li>
            <li><a href="belize-private-tours.html" class="hover:text-white transition-colors">Private Tours</a></li>
            <li><a href="belize-shore-excursions-faq.html" class="hover:text-white transition-colors">FAQ</a></li>
          </ul>
        </div>
      </div>
      <div class="border-t border-gray-800 pt-8 text-xs text-center sm:text-left">
        <p>&copy; 2026 {SITE}. Verify times and prices with operators before booking.</p>
      </div>
    </div>
  </footer>
"""


def trust_strip_html() -> str:
    return """<section class="trust-strip" aria-label="Belize shore excursion highlights">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <ul class="trust-strip__list">
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Cave Tubing</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Mayan Ruins</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Barrier Reef Snorkel</li>
      <li class="trust-strip__item"><span class="trust-strip__check" aria-hidden="true">✔</span> Return To Ship On Time</li>
    </ul>
  </div>
</section>
"""


def tour_data_page(tour: dict) -> str:
    cat = tour["category"]
    if cat in ("snorkel", "beach"):
        data_page = "snorkel"
    elif cat in ("ruins", "lamanai"):
        data_page = "ruins"
    elif cat == "private":
        data_page = "private"
    elif cat in ("cave", "zip", "jeep", "combo"):
        data_page = "adventure"
    else:
        data_page = "tours"
    return data_page


def build_page_meta() -> list[dict]:
    pages = [
        dict(
            file="index.html",
            title=f"{SITE} | Cave Tubing, Ruins &amp; Reef Tours from Belize City",
            description="Plan Belize shore excursions for cruise passengers — cave tubing, Altun Ha Mayan ruins, barrier reef snorkelling and beach breaks from Belize City tender port.",
            keywords="Belize shore excursions, Belize City cruise excursions, cave tubing Belize, Altun Ha cruise tour, Belize snorkel excursion",
            path="",
            data_page="home",
            hero="partials/hero-home.html",
            content="home.html",
            schema=home_schema(home_faq_data()),
        ),
        dict(
            file="best-belize-shore-excursions.html",
            title="Belize Shore Excursions | Compare Belize City Cruise Tours",
            description="Compare the best Belize shore excursions — cave tubing, Mayan ruins, reef snorkelling and beach breaks with cruise timing from Belize City tender port.",
            keywords="Belize shore excursions, Belize City cruise port tours, compare Belize excursions, Belize cruise trips",
            path="best-belize-shore-excursions.html",
            data_page="excursions",
            hero="partials/hero-excursions.html",
            content="best-belize-shore-excursions.html",
            preload=BEST_IMG,
            schema={"@context": "https://schema.org", "@type": "WebPage", "name": "Belize Shore Excursions", "url": f"{DOMAIN}/best-belize-shore-excursions.html"},
        ),
        dict(
            file="belize-cruise-port-guide.html",
            title="Belize Cruise Port Guide | Belize City for Cruise Passengers",
            description="Belize cruise port guide — tender port logistics, Fort Street Tourism Village, distances to ruins and reef, currency and shore excursion planning.",
            keywords="Belize cruise port guide, Belize City port day, cruise passenger guide Belize, tender port Belize",
            path="belize-cruise-port-guide.html",
            data_page="port",
            hero="partials/hero-port-guide.html",
            content="belize-cruise-port-guide.html",
            preload=PORT_IMG,
            schema={"@context": "https://schema.org", "@type": "Article", "headline": "Belize Cruise Port Guide", "url": f"{DOMAIN}/belize-cruise-port-guide.html"},
        ),
        dict(
            file="one-day-in-belize-from-a-cruise-ship.html",
            title="One Day in Belize from a Cruise Ship | Port Itinerary",
            description="How to spend one day in Belize on a cruise stop — cave tubing, Mayan ruins or reef snorkel with return-to-ship buffer for Belize City tender port calls.",
            keywords="one day in Belize cruise, Belize City port day itinerary, cruise stop Belize planning",
            path="one-day-in-belize-from-a-cruise-ship.html",
            data_page="port",
            hero="partials/hero-one-day.html",
            content="one-day-in-belize-from-a-cruise-ship.html",
            preload=ONE_DAY_IMG,
            schema={"@context": "https://schema.org", "@type": "Article", "headline": "One Day in Belize from a Cruise Ship", "url": f"{DOMAIN}/one-day-in-belize-from-a-cruise-ship.html"},
        ),
        dict(
            file="belize-private-tours.html",
            title="Belize Private Tours | Private Shore Excursions for Cruise Passengers",
            description="Private and small-group Belize shore excursions for cruise passengers — dedicated guides, custom pacing and return-to-ship timing from Belize City port.",
            keywords="Belize private tours cruise, private shore excursions Belize, small group Belize tours",
            path="belize-private-tours.html",
            data_page="private",
            hero="partials/hero-private.html",
            content="belize-private-tours.html",
            preload=PRIVATE_IMG,
            schema={"@context": "https://schema.org", "@type": "Article", "headline": "Belize Private Tours", "url": f"{DOMAIN}/belize-private-tours.html"},
        ),
        dict(
            file="belize-snorkeling-and-beach-excursions.html",
            title="Belize Snorkeling &amp; Beach Excursions | Reef Tours for Cruise Passengers",
            description="Belize snorkelling and beach excursions for cruise passengers — Caye Caulker, Shark Ray Alley, barrier reef and island beach breaks from Belize City.",
            keywords="Belize snorkel excursion cruise, Caye Caulker shore excursion, Shark Ray Alley Belize, beach break cruise",
            path="belize-snorkeling-and-beach-excursions.html",
            data_page="snorkel",
            hero="partials/hero-snorkel.html",
            content="belize-snorkeling-and-beach-excursions.html",
            preload=SNORKEL_IMG,
            schema={"@context": "https://schema.org", "@type": "Article", "headline": "Belize Snorkeling and Beach Excursions", "url": f"{DOMAIN}/belize-snorkeling-and-beach-excursions.html"},
        ),
        dict(
            file="belize-mayan-ruins-excursions.html",
            title="Belize Mayan Ruins Excursions | Altun Ha &amp; Lamanai for Cruise Passengers",
            description="Belize Mayan ruins excursions for cruise passengers — Altun Ha, Lamanai, Cahal Pech and cultural tours from Belize City tender port.",
            keywords="Belize Mayan ruins cruise, Altun Ha shore excursion, Lamanai Belize tour, Mayan ruins Belize City",
            path="belize-mayan-ruins-excursions.html",
            data_page="ruins",
            hero="partials/hero-ruins.html",
            content="belize-mayan-ruins-excursions.html",
            preload=RUINS_IMG,
            schema={"@context": "https://schema.org", "@type": "Article", "headline": "Belize Mayan Ruins Excursions", "url": f"{DOMAIN}/belize-mayan-ruins-excursions.html"},
        ),
        dict(
            file="belize-shore-excursions-faq.html",
            title="Belize Shore Excursions FAQ | Cruise Passenger Questions",
            description="Frequently asked questions about Belize shore excursions — tender port logistics, safety, currency, best tours and what to bring on a Belize cruise port day.",
            keywords="Belize shore excursions FAQ, Belize cruise port questions, is Belize safe cruise, Belize tender port",
            path="belize-shore-excursions-faq.html",
            data_page="port",
            hero="partials/hero-faq.html",
            content="belize-shore-excursions-faq.html",
            preload=FAQ_IMG,
            schema={"@context": "https://schema.org", "@type": "FAQPage", "name": "Belize Shore Excursions FAQ", "url": f"{DOMAIN}/belize-shore-excursions-faq.html"},
        ),
    ]
    for tour in TOURS:
        img, _ = CATEGORY_IMAGES.get(tour["category"], (INTRO_IMG, INTRO_ALT))
        pages.append(dict(
            file=f"{tour['slug']}.html",
            title=f"{tour['title']} | Belize Cruise Shore Excursion",
            description=f"{tour['title']} shore excursion for Belize cruise passengers — {tour['seg_desc']} {tour['duration']} from Belize City tender port with return-to-ship timing.",
            keywords=f"{tour['title']} Belize, Belize shore excursion cruise, {tour['category']} Belize City tour",
            path=f"{tour['slug']}.html",
            data_page=tour_data_page(tour),
            hero=f"partials/hero-{tour['slug']}.html",
            content=f"{tour['slug']}.html",
            preload=img,
            schema=tourist_trip_schema(tour["title"], f"{tour['seg_desc']} Shore excursion from Belize City cruise port for cruise passengers."),
        ))
    return pages


def build_hero_defs() -> dict[str, str]:
    heroes = {
        "hero-home.html": hero_home(),
        "hero-excursions.html": hero_inner(
            "Belize City · Tender Port",
            f"Belize<br/><span class=\"{ACCENT}\">Shore Excursions</span>",
            "Compare cave tubing, Mayan ruins, reef snorkelling and beach breaks for your Belize cruise ship schedule.",
            BEST_IMG, BEST_ALT, breadcrumb="Shore Excursions",
        ),
        "hero-port-guide.html": hero_inner(
            "Cruise Passenger Guide",
            f"Belize<br/><span class=\"{ACCENT}\">Cruise Port Guide</span>",
            "Tender port logistics, Fort Street Tourism Village, distances to ruins and reef, currency and return-to-ship timing.",
            PORT_IMG, PORT_ALT, breadcrumb="Port Guide",
            cta=("best-belize-shore-excursions.html", "View Shore Excursions →"),
            tags=["🚢 Tender Port", "🏛️ Mayan Ruins", "🐠 Barrier Reef", "💵 BZD & USD"],
        ),
        "hero-one-day.html": hero_inner(
            "Port Day Timeline",
            f"One Day in<br/><span class=\"{ACCENT}\">Belize</span>",
            "Hour-by-hour plan from tender to departure — ruins, cave tubing or reef snorkel with return-to-ship buffer.",
            ONE_DAY_IMG, ONE_DAY_ALT, breadcrumb="One Day in Belize",
        ),
        "hero-private.html": hero_inner(
            "Private &amp; Small Group",
            f"Belize<br/><span class=\"{ACCENT}\">Private Tours</span>",
            "Dedicated guides, custom pacing and private cave tubing for cruise passenger groups at Belize City port.",
            PRIVATE_IMG, PRIVATE_ALT, breadcrumb="Private Tours",
        ),
        "hero-snorkel.html": hero_inner(
            "Barrier Reef",
            f"Snorkeling &amp;<br/><span class=\"{ACCENT}\">Beach Excursions</span>",
            "Caye Caulker, Shark Ray Alley and Belize Barrier Reef snorkelling timed for cruise port schedules.",
            SNORKEL_IMG, SNORKEL_ALT, breadcrumb="Snorkel &amp; Beach",
        ),
        "hero-ruins.html": hero_inner(
            "Mayan Heritage",
            f"Mayan Ruins<br/><span class=\"{ACCENT}\">Excursions</span>",
            "Altun Ha, Lamanai and Cahal Pech — ancient temples and cultural tours from Belize City cruise port.",
            RUINS_IMG, RUINS_ALT, breadcrumb="Mayan Ruins",
        ),
        "hero-faq.html": hero_inner(
            "Cruise Passenger FAQ",
            f"Belize Shore<br/><span class=\"{ACCENT}\">Excursions FAQ</span>",
            "Tender port logistics, safety, currency, best tours and packing tips for your Belize cruise port day.",
            FAQ_IMG, FAQ_ALT, breadcrumb="FAQ",
        ),
    }
    for tour in TOURS:
        heroes[f"hero-{tour['slug']}.html"] = tour_hero(tour)
    return heroes


def main() -> None:
    print("Building Belize Shore Excursion site…")

    write("partials/nav.html", nav_html())
    write("partials/footer.html", footer_html())
    write("partials/trust-strip.html", trust_strip_html())

    for name, html in build_hero_defs().items():
        write(f"partials/{name}", html)

    for name, html in all_guide_content().items():
        write(f"content/{name}", html)

    for name, html in all_tour_content().items():
        write(f"content/{name}", html)

    for p in build_page_meta():
        write(
            p["file"],
            page_shell(
                title=p["title"],
                description=p["description"],
                keywords=p["keywords"],
                canonical_path=p["path"],
                data_page=p["data_page"],
                hero=p["hero"],
                content=p["content"],
                preload=p.get("preload", HOME_HERO),
                schema=p.get("schema"),
            ),
        )

    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, freq in SITEMAP_PAGES:
        url = f"{DOMAIN}/{loc}" if loc else f"{DOMAIN}/"
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{DATE}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    write("sitemap.xml", "\n".join(lines) + "\n")

    write("package.json", """{
  "name": "belize-shore-excursion",
  "private": true,
  "scripts": {
    "build": "python3 scripts/build-belize-site.py",
    "images": "python3 scripts/fetch-belize-images.py",
    "check": "python3 scripts/check-belize-site.py",
    "deploy": "wrangler deploy",
    "preview": "python3 -m http.server 8908"
  },
  "devDependencies": {
    "wrangler": "^4.94.0"
  }
}
""")

    write("wrangler.jsonc", """{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "belize-shore-excursion",
  "compatibility_date": "2026-06-06",
  "observability": { "enabled": true },
  "assets": { "directory": "." },
  "routes": [
    {
      "pattern": "belizeshoreexcursion.com",
      "custom_domain": true
    }
  ]
}
""")

    write("deploy.sh", f"""#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

if [[ ! -f node_modules/.bin/wrangler ]]; then
  npm install
fi

echo "Deploying {SITE} to Cloudflare..."
npx wrangler deploy

echo "Done. Check {DOMAIN}/ shortly."
""")

    (ROOT / "deploy.sh").chmod(0o755)

    images_dir = ROOT / "images"
    images_dir.mkdir(exist_ok=True)
    for img in ALL_IMAGES:
        p = ROOT / img
        if p.exists() and p.stat().st_size > 5000:
            continue
        p.write_bytes(PLACEHOLDER_PNG)

    write("images/ATTRIBUTION.md", """# Image attribution

Hero and content images are sourced from [Wikimedia Commons](https://commons.wikimedia.org) under Creative Commons licences where applicable.

Run `npm run images` to download location-accurate photos. Replace any image with your own assets — keep filenames consistent with `scripts/belize_config.py`.
""")

    write("README.md", """# Belize Shore Excursion

Cruise-passenger planning guide for Belize City, Belize shore excursions.

## Development

```bash
npm install
npm run build
npm run images
npm run check
npm run preview
```

Open http://localhost:8908 (requires local server for partial loading).

## Deploy to Cloudflare

```bash
npm run build && npm run images && npm run check && ./deploy.sh
```

Domain: https://belizeshoreexcursion.com
""")

    print("Done.")


if __name__ == "__main__":
    main()
