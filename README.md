# Belize Shore Excursion (World 2.0)

Static cruise-port planning site for `belizeshoreexcursion.com`.

## Commands

```bash
npm run build   # Python static HTML generator
npm run qa      # Phase 13B regression gates
npm run deploy  # build + qa + wrangler deploy (Belize only)
npm run preview # local static preview on :8908
```

Canonical URL policy: **apex + `.html`**. Primary content is inline HTML; `js/nav.js` is progressive enhancement only.

Antigua leftover images live under `quarantine/` and are excluded from deploy.
