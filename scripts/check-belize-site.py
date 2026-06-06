#!/usr/bin/env python3
"""QA checks for Belize Shore Excursion site."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "belizeshoreexcursion.com"

FORBIDDEN = [
    "barbados", "antigua", "cozumel", "aruba", "st maarten", "st. maarten",
    "bonaire", "dominica", "flam", "flåm", "st john's", "st johns",
    "philipsburg", "bridgetown", "nelson's dockyard", "cades reef",
    "chankanaab", "mr sanchos", "el cielo", "amber cove", "grand cayman",
    "san juan", "tortola", "gibraltar", "norway", "honningsvag",
]

REQUIRED_PHRASES = [
    "belize",
    "cruise passenger",
    "return to ship",
]

SCAN_EXTENSIONS = {".html", ".py", ".json", ".jsonc", ".txt", ".xml", ".md", ".js", ".css", ".sh"}
SKIP_DIRS = {"node_modules", ".git", "scripts/__pycache__"}


def iter_files() -> list[Path]:
    files = []
    for p in ROOT.rglob("*"):
        if p.is_dir():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SCAN_EXTENSIONS:
            files.append(p)
    return files


def check_forbidden_references() -> list[str]:
    errors = []
    for path in iter_files():
        if path.name == "check-belize-site.py":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in FORBIDDEN:
            if term in text:
                errors.append(f"Forbidden reference '{term}' in {path.relative_to(ROOT)}")
    return errors


def check_domain_config() -> list[str]:
    errors = []
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8") if (ROOT / "robots.txt").exists() else ""
    if DOMAIN not in robots:
        errors.append("robots.txt missing belizeshoreexcursion.com sitemap")
    if "antigua" in robots.lower() or "barbados" in robots.lower():
        errors.append("robots.txt contains wrong destination reference")

    wrangler = (ROOT / "wrangler.jsonc").read_text(encoding="utf-8") if (ROOT / "wrangler.jsonc").exists() else ""
    if DOMAIN not in wrangler:
        errors.append("wrangler.jsonc missing belizeshoreexcursion.com domain")

    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        errors.append("sitemap.xml missing")
    else:
        tree = ET.parse(sitemap)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [el.text for el in tree.findall(".//sm:loc", ns)]
        if not locs:
            locs = [el.text for el in tree.findall(".//loc")]
        bad = [u for u in locs if u and DOMAIN not in u]
        if bad:
            errors.append(f"sitemap.xml has non-Belize URLs: {bad[:3]}")
        if len(locs) < 40:
            errors.append(f"sitemap.xml has only {len(locs)} URLs (expected 42+)")

    index = (ROOT / "index.html").read_text(encoding="utf-8") if (ROOT / "index.html").exists() else ""
    if "Belize Shore Excursion" not in index:
        errors.append("index.html missing Belize site title")
    if "antigua" in index.lower() or "barbados" in index.lower():
        errors.append("index.html contains wrong destination reference")

    return errors


def check_tour_pages() -> list[str]:
    errors = []
    tour_html = list(ROOT.glob("*.html"))
    tour_pages = [p for p in tour_html if p.name not in {
        "index.html", "best-belize-shore-excursions.html", "belize-cruise-port-guide.html",
        "one-day-in-belize-from-a-cruise-ship.html", "belize-private-tours.html",
        "belize-snorkeling-and-beach-excursions.html", "belize-mayan-ruins-excursions.html",
        "belize-shore-excursions-faq.html",
    }]
    if len(tour_pages) < 30:
        errors.append(f"Expected 34 tour pages, found {len(tour_pages)}")

    for path in tour_pages[:5]:
        text = path.read_text(encoding="utf-8")
        if "Cruise Passenger Snapshot" not in text:
            # snapshot is in content partial loaded via JS — check content file
            content_name = path.stem + ".html"
            content_path = ROOT / "content" / content_name
            if content_path.exists():
                content = content_path.read_text(encoding="utf-8")
                if "Cruise Passenger Snapshot" not in content:
                    errors.append(f"{content_name} missing Cruise Passenger Snapshot")
                if "Why Cruise Passengers Choose This Belize Excursion" not in content:
                    errors.append(f"{content_name} missing Why Cruise Passengers Choose section")
                if "Return To Ship On Time" not in content:
                    errors.append(f"{content_name} missing return-to-ship badge")
    return errors


def check_required_content() -> list[str]:
    errors = []
    guides = [
        "best-belize-shore-excursions.html",
        "belize-cruise-port-guide.html",
        "one-day-in-belize-from-a-cruise-ship.html",
        "belize-private-tours.html",
        "belize-snorkeling-and-beach-excursions.html",
        "belize-mayan-ruins-excursions.html",
        "belize-shore-excursions-faq.html",
    ]
    for g in guides:
        if not (ROOT / g).exists():
            errors.append(f"Missing guide page: {g}")
    home_content = ROOT / "content" / "home.html"
    if home_content.exists():
        text = home_content.read_text(encoding="utf-8")
        if "Why Cruise Passengers" not in text:
            errors.append("home.html missing Why Cruise Passengers Choose Belize section")
    return errors


def main() -> None:
    print("Running Belize site QA checks…")
    errors = []
    errors.extend(check_forbidden_references())
    errors.extend(check_domain_config())
    errors.extend(check_tour_pages())
    errors.extend(check_required_content())

    if errors:
        print("FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        raise SystemExit(1)

    print("All checks passed.")
    print(f"  Domain: {DOMAIN}")
    print(f"  Pages in sitemap: {len(ET.parse(ROOT / 'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')) or ET.parse(ROOT / 'sitemap.xml').findall('.//loc')}")
    print("  Ready for GitHub and Cloudflare deploy.")


if __name__ == "__main__":
    main()
