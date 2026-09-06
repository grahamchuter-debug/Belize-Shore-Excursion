#!/usr/bin/env python3
"""Phase 13B regression harness for Belize Shore Excursion World 2.0."""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = "https://belizeshoreexcursion.com"
APEX = "belizeshoreexcursion.com"
MANIFEST = json.loads((ROOT / "scripts" / "protected_routes.json").read_text(encoding="utf-8"))

failed = 0


def fail(msg: str) -> None:
    global failed
    print(f"FAIL: {msg}")
    failed += 1


def ok(msg: str) -> None:
    print(f"OK: {msg}")


BANNED = [
    re.compile(r"cdn\.tailwindcss\.com", re.I),
    re.compile(r"shoreexcursionsgroup", re.I),
    re.compile(r"fetch\(.*content/", re.I),
    re.compile(r"fetch\(.*partials/", re.I),
    re.compile(r"data-content=", re.I),
    re.compile(r"Book now", re.I),
    re.compile(r"Check availability", re.I),
    re.compile(r"Secure your place", re.I),
    re.compile(r"return[- ]to[- ]ship guarantee", re.I),
    re.compile(r"most[- ]booked", re.I),
    re.compile(r"best[- ]selling", re.I),
    re.compile(r'"@type"\s*:\s*"Product"'),
    re.compile(r'"@type"\s*:\s*"Offer"'),
    re.compile(r"AggregateRating"),
    re.compile(r'"@type"\s*:\s*"LocalBusiness"'),
    re.compile(r"hero-antigua", re.I),
    re.compile(r"nelson.?s dockyard", re.I),
    re.compile(r"cades reef", re.I),
    re.compile(r"sk_live_|sk_test_|resend|stripe\.com", re.I),
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def check_manifest() -> None:
    routes = MANIFEST["routes"]
    if len(routes) != 42:
        fail(f"manifest has {len(routes)} routes, expected 42")
    else:
        ok("manifest 42 routes")
    paths = [r["path"] for r in routes]
    if len(paths) != len(set(paths)):
        fail("duplicate paths in manifest")


def check_protected_files() -> None:
    generated = 0
    for route in MANIFEST["routes"]:
        f = ROOT / route["file"]
        if not f.exists():
            fail(f"missing protected file {route['file']}")
            continue
        generated += 1
        html = f.read_text(encoding="utf-8")
        if "<h1" not in html:
            fail(f"{route['file']} missing H1")
        if 'id="main"' not in html:
            fail(f"{route['file']} missing #main")
        if "skip-link" not in html:
            fail(f"{route['file']} missing skip-link")
        if "menu-toggle" not in html or "mobile-menu" not in html:
            fail(f"{route['file']} missing mobile nav wiring")
        if 'rel="canonical"' not in html:
            fail(f"{route['file']} missing canonical")
        expected_canon = f"{DOMAIN}/" if route["path"] == "/" else f"{DOMAIN}{route['path']}"
        if f'rel="canonical" href="{expected_canon}"' not in html:
            fail(f"{route['file']} canonical should be {expected_canon}")
        title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        if not title_m or len(title_m.group(1).strip()) < 10:
            fail(f"{route['file']} weak/missing title")
        # Soft 404 / empty shell checks
        if 'id="page-content"></main>' in html or 'data-content="' in html:
            fail(f"{route['file']} JS-fetch shell still present")
        if "Could not load content/" in html or "Could not load partials/" in html:
            fail(f"{route['file']} soft-load error markup")
        for ban in BANNED:
            if ban.search(html):
                fail(f"{route['file']} matched banned pattern {ban.pattern}")
        # Primary content should be substantial
        main_m = re.search(r'<main id="main"[^>]*>(.*?)</main>', html, re.S | re.I)
        if not main_m or len(re.sub(r"\s+", " ", main_m.group(1)).strip()) < 400:
            fail(f"{route['file']} main content too thin / missing")
    if generated == 42:
        ok("42/42 protected files generated with static H1")
    else:
        fail(f"only {generated}/42 generated")


def check_titles_unique() -> None:
    titles = []
    h1s = []
    for route in MANIFEST["routes"]:
        html = read(route["file"])
        t = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        h = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        if t:
            titles.append(re.sub(r"\s+", " ", t.group(1)).strip())
        if h:
            h1s.append(re.sub(r"<[^>]+>", "", h.group(1)).strip())
    if len(titles) != len(set(titles)):
        fail("duplicate titles among protected routes")
    else:
        ok("unique titles")
    if len(h1s) != len(set(h1s)):
        # warn-level: some altun ha pages might share similar - fail if exact dup
        from collections import Counter
        dups = [k for k, v in Counter(h1s).items() if v > 1]
        fail(f"duplicate H1s: {dups[:5]}")
    else:
        ok("unique H1s")


def check_trust() -> None:
    for route in MANIFEST["trust_routes"]:
        f = ROOT / route["file"]
        if not f.exists():
            fail(f"missing trust page {route['file']}")
            continue
        html = f.read_text(encoding="utf-8")
        if EMAIL_PLACEHOLDER() not in html and "hello@belizeshoreexcursion.com" not in html:
            fail(f"{route['file']} missing public email")
        if 'rel="canonical"' not in html:
            fail(f"{route['file']} missing canonical")
        ok(f"trust {route['path']}")


def EMAIL_PLACEHOLDER() -> str:
    return "hello@belizeshoreexcursion.com"


def check_404() -> None:
    if not (ROOT / "404.html").exists():
        fail("404.html missing")
        return
    html = read("404.html")
    if "noindex" not in html.lower():
        fail("404.html missing noindex")
    if f'rel="canonical" href="{DOMAIN}/"' in html:
        fail("404.html incorrectly canonicalises homepage")
    if "<h1" not in html:
        fail("404.html missing H1")
    ok("404 page branded + noindex")


def check_sitemap_robots() -> None:
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        fail("sitemap.xml missing")
        return
    tree = ET.parse(sm)
    locs = [el.text for el in tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    if not locs:
        locs = [el.text for el in tree.findall(".//{*}loc")]
    if not locs:
        locs = [el.text for el in tree.findall(".//loc")]
    for route in MANIFEST["routes"]:
        expected = f"{DOMAIN}/" if route["path"] == "/" else f"{DOMAIN}{route['path']}"
        if expected not in locs:
            fail(f"sitemap missing {expected}")
    for route in MANIFEST["trust_routes"]:
        expected = f"{DOMAIN}{route['path']}"
        if expected not in locs:
            fail(f"sitemap missing trust {expected}")
    bad = [u for u in locs if u and ("www." in u or not u.startswith(DOMAIN))]
    if bad:
        fail(f"sitemap has non-apex URLs: {bad[:3]}")
    # no extensionless dupes for equity pages
    for u in locs:
        if u and u.endswith(".html"):
            extless = u[:-5]
            if extless in locs:
                fail(f"sitemap has extensionless dupe of {u}")
    if any("/content/" in (u or "") or "/partials/" in (u or "") for u in locs):
        fail("sitemap includes content/partials")
    ok(f"sitemap valid ({len(locs)} locs)")

    robots = read("robots.txt")
    if f"Sitemap: {DOMAIN}/sitemap.xml" not in robots:
        fail("robots.txt missing apex sitemap")
    if "Allow:" not in robots:
        fail("robots.txt missing Allow")
    ok("robots.txt ok")


def check_worker_assets() -> None:
    w = read("worker.js")
    if "www." not in w or "HTML_EQUITY" not in w:
        fail("worker.js missing www/equity handling")
    if "index.html" not in w:
        fail("worker.js missing index.html → / handling")
    if "404" not in w:
        fail("worker.js missing 404 handling")
    ok("worker.js policy present")

    wr = read("wrangler.jsonc")
    if '"main": "worker.js"' not in wr:
        fail("wrangler missing worker main")
    if "www.belizeshoreexcursion.com" not in wr:
        fail("wrangler missing www custom domain")
    if "not_found_handling" not in wr:
        fail("wrangler missing not_found_handling")
    ok("wrangler World 2.0 assets config")

    if not (ROOT / ".assetsignore").exists():
        fail(".assetsignore missing")
    else:
        ai = read(".assetsignore")
        for req in ("content/", "partials/", "quarantine/", "scripts/"):
            if req not in ai:
                fail(f".assetsignore missing {req}")
        ok(".assetsignore excludes content/partials/quarantine")


def check_antigua_quarantine() -> None:
    q = ROOT / "quarantine" / "antigua"
    if not q.exists():
        fail("quarantine/antigua missing")
        return
    if not (q / "hero-antigua.png").exists():
        fail("hero-antigua not quarantined")
    # Deployed images dir must not contain antigua heroes
    for name in ("hero-antigua.png", "nelsons-dockyard.png", "cades-reef.png"):
        if (ROOT / "images" / name).exists():
            fail(f"Antigua image still in images/: {name}")
    ok("Antigua imagery quarantined")


def check_css_js() -> None:
    css = read("css/site.css")
    if "cdn.tailwind" in css:
        fail("css still references tailwind cdn")
    if ".skip-link" not in css or "clip-path" not in css:
        fail("skip-link not properly hidden in CSS")
    if ".menu-toggle" not in css or ".mobile-menu" not in css:
        fail("mobile nav CSS missing")
    if ".hero__shade" not in css:
        fail("hero scrim CSS missing")
    ok("local CSS World 2.0")
    nav = read("js/nav.js")
    if "menu-toggle" not in nav:
        fail("nav.js incomplete")
    ok("nav.js mobile wiring")


def check_no_antigua_in_deployed_html() -> None:
    for route in MANIFEST["routes"]:
        html = read(route["file"]).lower()
        for term in ("antigua", "nelson", "cades reef", "shirley heights"):
            if term in html:
                fail(f"{route['file']} references {term}")


def main() -> None:
    print("Belize Phase 13B regression…")
    check_manifest()
    check_protected_files()
    check_titles_unique()
    check_trust()
    check_404()
    check_sitemap_robots()
    check_worker_assets()
    check_antigua_quarantine()
    check_css_js()
    check_no_antigua_in_deployed_html()
    if failed:
        print(f"\nREGRESSION RED: {failed} failure(s)")
        sys.exit(1)
    print("\nREGRESSION GREEN: all local gates passed")
    sys.exit(0)


if __name__ == "__main__":
    main()
