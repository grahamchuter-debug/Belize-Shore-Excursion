/**
 * Belize Shore Excursion — Workers Assets entry (World 2.0 / Phase 13B).
 * Canonical = apex + .html
 * - www → apex 301 (path + query preserved)
 * - extensionless equity → matching .html 301
 * - /index.html → /
 * - genuine 404 (no soft homepage fallback)
 */
const APEX_HOST = 'belizeshoreexcursion.com';

const HTML_EQUITY = new Set([
  'best-belize-shore-excursions',
  'belize-cruise-port-guide',
  'one-day-in-belize-from-a-cruise-ship',
  'belize-private-tours',
  'belize-snorkeling-and-beach-excursions',
  'belize-mayan-ruins-excursions',
  'belize-shore-excursions-faq',
  'cave-tubing-and-zip-line-combo',
  'belize-cave-tubing',
  'turtle-snorkel-and-island-time',
  'altun-ha-and-belize-city-overview',
  'shark-ray-alley-and-caye-caulker-beach-break',
  'lamanai-eco-adventure',
  'kukumba-beach-and-city',
  'barrier-reef-snorkel',
  'xunantunich-and-cave-tubing',
  'private-tubing-expedition',
  'cave-tubing-and-jungle-trek-with-lunch',
  'jungle-zip-line',
  'belize-city-and-zoo-combo',
  'belize-zoo-and-jeep-adventure',
  'zip-line-and-belize-zoo-with-lunch',
  'howler-monkey-sanctuary',
  'baboon-sanctuary-and-jeep-adventure',
  'expedition-to-crooked-tree-wildlife-sanctuary',
  'jungle-jeep-adventure',
  'jungle-jeep-adventure-and-beach-break',
  'jungle-jeep-adventure-and-sibun-wildlife-river-cruise',
  'belize-jungle-jeep-rum-factory-and-museum-tour',
  'belize-city-and-rum-factory-tour',
  'city-sightseeing-and-highlights',
  'river-wallace-and-burrell-boom',
  'beach-and-city',
  'journey-to-cahal-pech',
  'altun-ha-and-jeep-adventure',
  'altun-ha-and-river-wallace',
  'altun-ha-mayan-ruins-and-tropical-jungle-monkey-reserve',
  'altun-ha-mayan-ruins-and-wildlife-of-the-belize-zoo',
  'adventure-to-altun-ha',
  'adventure-to-altun-ha-and-belize-zoo',
  'belize-party-bus',
]);

const DIR_PAGES = new Set([
  'about',
  'contact',
  'privacy',
  'terms',
  'methodology',
]);

function assetRequest(request, url, pathname) {
  const assetUrl = new URL(url.toString());
  assetUrl.pathname = pathname;
  return new Request(assetUrl.toString(), request);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname.toLowerCase();
    const path = url.pathname || '/';

    if (host === `www.${APEX_HOST}`) {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      return Response.redirect(dest.toString(), 301);
    }

    if (path === '/index.html' || path === '/index.HTML') {
      const dest = new URL(url.toString());
      dest.hostname = APEX_HOST;
      dest.protocol = 'https:';
      dest.pathname = '/';
      return Response.redirect(dest.toString(), 301);
    }

    if (!path.includes('.') && !path.endsWith('/')) {
      const slug = path.replace(/^\//, '');
      if (HTML_EQUITY.has(slug)) {
        const dest = new URL(url.toString());
        dest.hostname = APEX_HOST;
        dest.protocol = 'https:';
        dest.pathname = `/${slug}.html`;
        return Response.redirect(dest.toString(), 301);
      }
      if (DIR_PAGES.has(slug)) {
        const dest = new URL(url.toString());
        dest.hostname = APEX_HOST;
        dest.protocol = 'https:';
        dest.pathname = `/${slug}/`;
        return Response.redirect(dest.toString(), 301);
      }
    }

    let assetPath = path;
    if (path === '/' || path === '') {
      assetPath = '/index.html';
    } else if (path.endsWith('/')) {
      const slug = path.slice(1, -1);
      if (DIR_PAGES.has(slug)) {
        assetPath = `/${slug}/index.html`;
      }
    }

    const assetResponse = await env.ASSETS.fetch(assetRequest(request, url, assetPath));

    if (assetResponse.status === 404) {
      const notFound = await env.ASSETS.fetch(assetRequest(request, url, '/404.html'));
      return new Response(notFound.body, {
        status: 404,
        headers: {
          'content-type': 'text/html; charset=utf-8',
          'cache-control': 'no-store',
          'x-robots-tag': 'noindex',
        },
      });
    }

    return assetResponse;
  },
};
