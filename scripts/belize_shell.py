"""World 2.0 HTML shell helpers for Belize Shore Excursion."""
from __future__ import annotations

import json
from html import escape

from belize_config import DOMAIN, EMAIL, FONTS, SITE


def nav(current: str) -> str:
    items = [
        ("/", "home", "Home"),
        ("/best-belize-shore-excursions.html", "excursions", "Excursions"),
        ("/belize-mayan-ruins-excursions.html", "ruins", "Mayan Ruins"),
        ("/belize-snorkeling-and-beach-excursions.html", "snorkel", "Snorkel"),
        ("/belize-private-tours.html", "private", "Private"),
        ("/belize-cruise-port-guide.html", "port", "Port Guide"),
        ("/belize-shore-excursions-faq.html", "faq", "FAQ"),
    ]

    def desk(href: str, key: str, label: str) -> str:
        cur = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    desktop = "\n          ".join(desk(*i) for i in items)
    mobile = "\n      ".join(
        f'<a href="{h}"{" aria-current=\"page\"" if current == k else ""}>{lab}</a>'
        for h, k, lab in items
    )
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-nav">
  <div class="wrap site-nav__inner">
    <a class="brand" href="/">
      <span class="brand__name">Belize Shore Excursion</span>
      <span class="brand__tag">Cruise passenger guide</span>
    </a>
    <nav aria-label="Primary">
      <ul class="nav-links">
          {desktop}
      </ul>
    </nav>
    <a class="nav-cta" href="/best-belize-shore-excursions.html">Compare excursions</a>
    <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </div>
  <div class="mobile-menu" id="mobile-menu" hidden>
    <div class="wrap">
      {mobile}
      <a href="/best-belize-shore-excursions.html">Compare excursions</a>
      <a href="/one-day-in-belize-from-a-cruise-ship.html">One day in Belize</a>
      <a href="/contact/">Contact</a>
    </div>
  </div>
</header>"""


def footer() -> str:
    return f"""<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <p class="footer-brand">{SITE}</p>
      <p>{SITE} provides cruise-focused excursion information and independent destination advice for passengers visiting Belize City. Not affiliated with any cruise line.</p>
      <p style="margin-top:0.85rem"><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <h2>Explore</h2>
      <ul>
        <li><a href="/best-belize-shore-excursions.html">Best excursions</a></li>
        <li><a href="/belize-mayan-ruins-excursions.html">Mayan ruins</a></li>
        <li><a href="/belize-snorkeling-and-beach-excursions.html">Snorkel &amp; beach</a></li>
        <li><a href="/belize-private-tours.html">Private tours</a></li>
        <li><a href="/belize-cave-tubing.html">Cave tubing</a></li>
      </ul>
    </div>
    <div>
      <h2>Plan</h2>
      <ul>
        <li><a href="/belize-cruise-port-guide.html">Cruise port guide</a></li>
        <li><a href="/one-day-in-belize-from-a-cruise-ship.html">One day in Belize</a></li>
        <li><a href="/belize-shore-excursions-faq.html">FAQ</a></li>
        <li><a href="/methodology/">Methodology</a></li>
      </ul>
    </div>
    <div>
      <h2>Trust</h2>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy/">Privacy</a></li>
        <li><a href="/terms/">Terms</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>&copy; 2026 {SITE} · <a href="{DOMAIN}/">{DOMAIN.replace("https://", "")}</a> · Not affiliated with any cruise line</p>
  </div>
</footer>"""


def hero_home() -> str:
    return """<section class="hero" aria-label="Homepage hero">
  <div class="hero__media">
    <img src="/images/hero-belize.png" alt="Turquoise Caribbean water and tropical coastline in Belize for cruise passengers planning shore excursions from Belize City cruise port" width="1920" height="1080" fetchpriority="high" />
  </div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__inner">
    <p class="hero__brand">Belize Shore Excursion</p>
    <h1>Belize Shore Excursions from the Cruise Port</h1>
    <p class="hero__lead">Plan a Belize City tender day around cave tubing, Mayan ruins, barrier reef snorkelling and beach breaks — with timing that respects your ship.</p>
    <div class="hero__actions">
      <a class="btn btn--primary" href="/best-belize-shore-excursions.html">Compare excursions</a>
      <a class="btn btn--ghost" href="/belize-cruise-port-guide.html">Explore the port guide</a>
    </div>
  </div>
</section>"""


def hero_page(
    *,
    title: str,
    lead: str,
    image: str,
    alt: str,
    crumb: str,
    cta_href: str | None = None,
    cta_label: str = "Explore related guides",
) -> str:
    cta = ""
    if cta_href:
        cta = f"""
    <div class="hero__actions">
      <a class="btn btn--primary" href="{cta_href}">{escape(cta_label)}</a>
    </div>"""
    return f"""<section class="hero hero--page" aria-label="{escape(title)}">
  <div class="hero__media">
    <img src="{image}" alt="{escape(alt)}" width="1600" height="900" fetchpriority="high" />
  </div>
  <div class="hero__shade" aria-hidden="true"></div>
  <div class="hero__inner">
    <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> · {crumb}</nav>
    <h1>{title}</h1>
    <p class="hero__lead">{lead}</p>{cta}
  </div>
</section>"""


def page_shell(
    *,
    title: str,
    description: str,
    canonical: str,
    og_image: str,
    nav_key: str,
    hero: str,
    body: str,
    schema: dict | list | None = None,
    preload: str | None = None,
    robots: str | None = None,
) -> str:
    canon = canonical if canonical.startswith("http") else f"{DOMAIN}{canonical}"
    preload = preload or og_image
    og_abs = og_image if og_image.startswith("http") else f"{DOMAIN}{og_image}"
    robots_meta = f'  <meta name="robots" content="{robots}" />\n' if robots else ""

    graph: list = []
    if schema is None:
        graph = [
            {
                "@type": "WebSite",
                "name": SITE,
                "url": f"{DOMAIN}/",
                "description": "Cruise-focused Belize shore excursion information and independent destination advice.",
                "inLanguage": "en",
                "publisher": {
                    "@type": "Organization",
                    "name": SITE,
                    "url": f"{DOMAIN}/",
                    "email": EMAIL,
                },
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
    elif isinstance(schema, list):
        graph = schema
    else:
        graph = [schema]

    schema_block = (
        '  <script type="application/ld+json">\n'
        + json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2)
        + "\n  </script>\n"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{escape(description)}" />
{robots_meta}  <link rel="canonical" href="{canon}" />
  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{canon}" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(description)}" />
  <meta property="og:image" content="{og_abs}" />
  <meta property="og:site_name" content="{SITE}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="geo.region" content="BZ" />
  <meta name="geo.placename" content="Belize City, Belize" />
{schema_block}
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{FONTS}" rel="stylesheet" />
  <link rel="stylesheet" href="/css/site.css" />
</head>
<body data-page="{nav_key}">
{nav(nav_key)}
{hero}
<main id="main" tabindex="-1">
{body}
</main>
{footer()}
<script src="/js/nav.js" defer></script>
</body>
</html>
"""


def related_nav(extra: list[tuple[str, str]] | None = None) -> str:
    links = [
        ("/belize-cruise-port-guide.html", "Port guide"),
        ("/best-belize-shore-excursions.html", "Best excursions"),
        ("/one-day-in-belize-from-a-cruise-ship.html", "One day in Belize"),
        ("/belize-snorkeling-and-beach-excursions.html", "Snorkel &amp; beach"),
        ("/belize-mayan-ruins-excursions.html", "Mayan ruins"),
        ("/belize-private-tours.html", "Private tours"),
        ("/belize-shore-excursions-faq.html", "FAQ"),
    ]
    if extra:
        links = extra + links
    items = " · ".join(f'<a href="{h}">{lab}</a>' for h, lab in links)
    return f"""<nav class="related" aria-label="Related Belize guides">
  <p class="related__label">Plan your port day</p>
  <p class="related__links">{items}</p>
</nav>"""


def snapshot(items: list[tuple[str, str]]) -> str:
    rows = "".join(
        f'<div class="snapshot__item"><dt>{escape(k)}</dt><dd>{v}</dd></div>'
        for k, v in items
    )
    return f"""<aside class="snapshot" aria-label="Cruise passenger snapshot">
  <h2>Cruise passenger snapshot</h2>
  <dl class="snapshot__grid">{rows}</dl>
</aside>"""
