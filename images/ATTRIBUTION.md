# Image attribution — Belize Shore Excursion

Belize photography used on this site is sourced from [Wikimedia Commons](https://commons.wikimedia.org) under applicable Creative Commons or public-domain terms. Filenames are mapped in `scripts/belize_config.py`.

## Active Belize assets (`images/`)

| File | Role |
|------|------|
| `hero-belize.png` | Homepage hero |
| `belize-cruise-port.png` | Port / city context |
| `belize-port-arrival.png` | Tender / arrival context |
| `best-belize-excursions.png` | Excursion hub |
| `one-day-belize.png` | One-day planning |
| `belize-intro.png` | General Belize scenery |
| `belize-cave-tubing.png` | Cave tubing |
| `belize-zip-line.png` | Zip line / canopy |
| `belize-snorkel.png` | Reef snorkel |
| `belize-beach.png` | Beach / island |
| `altun-ha.png` | Altun Ha ruins |
| `lamanai.png` | Lamanai |
| `belize-zoo.png` | Wildlife / zoo |
| `belize-jeep.png` | Jeep adventure |
| `belize-private.png` | Private touring |
| `belize-faq.png` | FAQ / trust |
| `belize-ruins.png` | Mayan ruins hub |

No Shore Excursions Group (SEG) supplier marketing images are used.

## Quarantined Antigua leftovers

Antigua-era clone assets are stored under `quarantine/antigua/` and excluded from deploy via `.assetsignore`. They must not appear under `images/` or in public HTML.

Refresh Wikimedia downloads with `python3 scripts/fetch-belize-images.py` only when intentionally replacing Belize assets — keep filenames stable.
