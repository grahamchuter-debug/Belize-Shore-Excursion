#!/usr/bin/env node
/**
 * Phase 13B regression harness — Belize Shore Excursion World 2.0
 * Must be GREEN before commit / push / deploy.
 */
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
let failed = 0;
let passed = 0;

function fail(msg) {
  console.error("FAIL:", msg);
  failed += 1;
}
function ok(msg) {
  console.log("OK:", msg);
  passed += 1;
}

const manifest = JSON.parse(readFileSync(join(ROOT, "scripts/protected_routes.json"), "utf8"));
const expected = manifest.routes.map((r) => r.file);
if (expected.length !== 42) fail(`manifest expected 42 routes, got ${expected.length}`);
else ok("manifest 42 protected routes");

const banned = [
  /shoreexcursionsgroup/i,
  /\bSEG\b/,
  /CABZTUBE|CABZTURTLE|CABZALTUN|SEG_MANUAL/i,
  /viator/i,
  /getyourguide/i,
  /cdn\.tailwindcss\.com/i,
  /fetch\(\s*['"]\/?content\//i,
  /fetch\(\s*['"]\/?partials\//i,
  /data-content=/i,
  /id="page-content"/i,
  /Check availability/i,
  /Secure your place/i,
  /Reserve your/i,
  /Secure a reservation/i,
  /most[- ]booked/i,
  /best[- ]selling/i,
  /return-to-ship guarantee/i,
  /easy booking/i,
  /live availability/i,
  /AggregateRating/,
  /"@type":\s*"Product"/,
  /"@type":\s*"Offer"/,
  /"@type":\s*"LocalBusiness"/,
  /hero-antigua/i,
  /nelsons-dockyard/i,
  /cades-reef/i,
  /antigua-/i,
  /sk_live_/i,
  /sk_test_/i,
];

const COMMERCIAL = new Set([
  "belize-cave-tubing.html",
  "turtle-snorkel-and-island-time.html",
  "altun-ha-and-belize-city-overview.html",
]);

const soft404Signals = [
  /Sorry, this page could not load/i,
  /python3 -m http\.server/i,
];

for (const file of expected) {
  const p = join(ROOT, file);
  if (!existsSync(p)) {
    fail(`missing protected ${file}`);
    continue;
  }
  const html = readFileSync(p, "utf8");
  if (!html.includes("<h1")) fail(`${file} missing static H1`);
  else ok(`${file} H1`);
  if (!/<title>[^<]+<\/title>/.test(html)) fail(`${file} missing title`);
  if (!html.includes('rel="canonical"')) fail(`${file} missing canonical`);
  const expectedCanon =
    file === "index.html"
      ? 'rel="canonical" href="https://belizeshoreexcursion.com/"'
      : `rel="canonical" href="https://belizeshoreexcursion.com/${file}"`;
  if (!html.includes(expectedCanon)) fail(`${file} bad canonical (want apex .html policy)`);
  if (!html.includes("hello@belizeshoreexcursion.com")) fail(`${file} missing contact email`);
  if (!html.includes('id="main"')) fail(`${file} missing #main`);
  if (!html.includes("skip-link")) fail(`${file} missing skip-link`);
  if (!html.includes("menu-toggle") || !html.includes("mobile-menu")) fail(`${file} mobile nav wiring`);
  if (!html.includes("/css/site.css")) fail(`${file} missing local CSS`);
  if (!html.includes("/js/nav.js")) fail(`${file} missing nav.js`);
  for (const re of banned) {
    if (re.test(html)) fail(`${file} banned pattern ${re}`);
  }
  if (!COMMERCIAL.has(file) && /Book now/i.test(html)) {
    fail(`${file} must remain editorial (no Book now)`);
  }
  for (const re of soft404Signals) {
    if (re.test(html)) fail(`${file} soft-404 signal ${re}`);
  }
}

const trust = ["about", "contact", "privacy", "terms", "methodology"];
for (const slug of trust) {
  const file = `${slug}/index.html`;
  if (!existsSync(join(ROOT, file))) fail(`missing trust ${file}`);
  else {
    const html = readFileSync(join(ROOT, file), "utf8");
    const canon = `rel="canonical" href="https://belizeshoreexcursion.com/${slug}/"`;
    if (!html.includes(canon)) fail(`${file} bad trust canonical`);
    else ok(`trust ${slug}`);
    if (!html.includes("<h1")) fail(`${file} missing H1`);
  }
}

if (!existsSync(join(ROOT, "404.html"))) fail("missing 404.html");
else {
  const html = readFileSync(join(ROOT, "404.html"), "utf8");
  if (!html.includes('content="noindex')) fail("404 missing noindex");
  if (html.includes('rel="canonical" href="https://belizeshoreexcursion.com/"')) {
    fail("404 must not use homepage canonical");
  }
  if (!html.includes("<h1")) fail("404 missing H1");
  else ok("404 branded noindex");
}

const sitemap = readFileSync(join(ROOT, "sitemap.xml"), "utf8");
if (sitemap.includes("www.belizeshoreexcursion.com")) fail("sitemap contains www host");
if (sitemap.includes("/content/") || sitemap.includes("/partials/")) fail("sitemap includes content/partials");
for (const r of manifest.routes) {
  const loc =
    r.path === "/"
      ? "https://belizeshoreexcursion.com/"
      : `https://belizeshoreexcursion.com${r.path}`;
  if (!sitemap.includes(`<loc>${loc}</loc>`)) fail(`sitemap missing ${loc}`);
}
for (const t of trust) {
  const loc = `https://belizeshoreexcursion.com/${t}/`;
  if (!sitemap.includes(`<loc>${loc}</loc>`)) fail(`sitemap missing ${loc}`);
  else ok(`sitemap ${t}`);
}
// extensionless dupes should not appear for equity pages
if (/belizeshoreexcursion\.com\/[a-z0-9-]+<\/loc>/.test(sitemap.replaceAll("belizeshoreexcursion.com/", ""))) {
  // crude check: every non-root/non-dir loc should end with .html or /
}
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
for (const loc of locs) {
  if (loc.includes("www.")) fail(`www in sitemap loc ${loc}`);
  const path = loc.replace("https://belizeshoreexcursion.com", "");
  if (path !== "/" && !path.endsWith(".html") && !path.endsWith("/")) {
    fail(`extensionless sitemap loc ${loc}`);
  }
}
ok(`sitemap locs ${locs.length}`);

const robots = readFileSync(join(ROOT, "robots.txt"), "utf8");
if (!robots.includes("Sitemap: https://belizeshoreexcursion.com/sitemap.xml")) fail("robots sitemap");
else ok("robots");

if (!existsSync(join(ROOT, "worker.js"))) fail("missing worker.js");
else {
  const w = readFileSync(join(ROOT, "worker.js"), "utf8");
  if (!w.includes("www.") || !w.includes("HTML_EQUITY")) fail("worker missing www/equity policy");
  if (!w.includes("/index.html")) fail("worker missing index.html handling");
  ok("worker.js");
}
if (!existsSync(join(ROOT, "js/nav.js"))) fail("missing js/nav.js");
else ok("js/nav.js");
if (!existsSync(join(ROOT, "css/site.css"))) fail("missing css");
else {
  const css = readFileSync(join(ROOT, "css/site.css"), "utf8");
  if (!css.includes(".skip-link") || !css.includes("clip-path")) fail("skip-link CSS incomplete");
  if (!css.includes(".hero__shade")) fail("hero scrim missing");
  ok("css/site.css");
}
if (!existsSync(join(ROOT, "images/ATTRIBUTION.md"))) fail("ATTRIBUTION");
else ok("ATTRIBUTION");
if (!existsSync(join(ROOT, ".assetsignore"))) fail(".assetsignore");
else {
  const ai = readFileSync(join(ROOT, ".assetsignore"), "utf8");
  if (!ai.includes("quarantine/") || !ai.includes("content/") || !ai.includes("partials/")) {
    fail(".assetsignore must exclude quarantine/content/partials");
  } else ok(".assetsignore quarantine");
}

const antigua = [
  "hero-antigua.png",
  "nelsons-dockyard.png",
  "cades-reef.png",
];
for (const name of antigua) {
  if (existsSync(join(ROOT, "images", name))) fail(`Antigua still in images/: ${name}`);
  if (!existsSync(join(ROOT, "quarantine/antigua", name))) fail(`Antigua not quarantined: ${name}`);
}
ok("Antigua quarantined");

// unique titles / h1 across protected routes
const titles = new Map();
const h1s = new Map();
for (const file of expected) {
  const html = readFileSync(join(ROOT, file), "utf8");
  const t = (html.match(/<title>([^<]+)<\/title>/) || [])[1];
  const h = (html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1]?.replace(/<[^>]+>/g, "").trim();
  if (!t) fail(`${file} empty title`);
  if (!h) fail(`${file} empty h1`);
  if (titles.has(t)) fail(`duplicate title: ${t} (${file} vs ${titles.get(t)})`);
  else titles.set(t, file);
  if (h1s.has(h)) fail(`duplicate H1: ${h} (${file} vs ${h1s.get(h)})`);
  else h1s.set(h, file);
}
ok("unique titles and H1s");

// no-JS primary content: sample homepage has substantial inline body
const home = readFileSync(join(ROOT, "index.html"), "utf8");
if (home.length < 8000) fail("homepage too thin — likely shell");
if (!home.includes("<main")) fail("homepage missing main");
ok("homepage inline content");

// Phase 13D commercial checks
for (const rel of COMMERCIAL) {
  const html = readFileSync(join(ROOT, rel), "utf8");
  const count = (html.match(/Book now/gi) || []).length;
  if (count < 3) fail(`${rel} expected >=3 Book now CTAs, found ${count}`);
  else ok(`${rel} Book now CTAs (${count})`);
  if (!existsSync(join(ROOT, "book", rel.replace(".html", ""), "index.html"))) {
    fail(`missing book route for ${rel}`);
  } else ok(`book route ${rel}`);
}

const privateHtml = readFileSync(join(ROOT, "belize-private-tours.html"), "utf8");
if (/Book now/i.test(privateHtml)) fail("private tours must remain editorial (no Book now)");
else ok("private tours editorial only");

const zipHtml = readFileSync(join(ROOT, "cave-tubing-and-zip-line-combo.html"), "utf8");
if (/Book now/i.test(zipHtml)) fail("non-commercial cave+zip must remain editorial");
else ok("cave+zip editorial only");

const terms = readFileSync(join(ROOT, "terms/index.html"), "utf8");
if (!/14 days/.test(terms)) fail("terms missing 14-day cancellation");
else ok("terms 14-day cancellation");
if (!/Payment is not confirmation/i.test(terms)) fail("terms missing payment≠confirmation");
else ok("terms payment≠confirmation");

const commercialCfg = readFileSync(join(ROOT, "js/commercial-config.js"), "utf8");
if (!/PRODUCTION_READY_LOCKED/.test(commercialCfg)) fail("commercial-config missing PRODUCTION_READY_LOCKED");
else ok("public lock PRODUCTION_READY_LOCKED");
if (/CABZTUBE|CABZTURTLE|CABZALTUN|SEG_MANUAL|\bSEG\b/.test(commercialCfg)) {
  fail("commercial-config leaked internal supply refs");
} else ok("commercial-config no SEG leak");

console.log(`\nRegression: ${passed} checks noted, ${failed} failures`);
if (failed > 0) {
  console.error("NOT GREEN");
  process.exit(1);
}
console.log("GREEN — 42/42 protected routes ready");
