#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
npm run build
npm run qa
npx wrangler deploy
echo "Deployed https://belizeshoreexcursion.com"
