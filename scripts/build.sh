#!/usr/bin/env bash
# Regenerates README.md and assets/ from the techhub.cafe/me portfolio data,
# so the profile never claims more than the portfolio does.
#   TECHHUB=~/Documents/dev/techhub scripts/build.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export TECHHUB="${TECHHUB:-$HOME/Documents/dev/techhub}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cd "$TECHHUB"
npx tsx --tsconfig tsconfig.json "$ROOT/scripts/dump.ts" "$TMP/data.json"
# Head-and-shoulders crop of the portfolio portrait, embedded in the hero SVG.
node -e "
require('sharp')('public/me/portrait/qadir.webp')
  .extract({ left: 110, top: 60, width: 300, height: 360 }).resize(356, 428)
  .greyscale().normalise().jpeg({ quality: 72, mozjpeg: true }).toBuffer()
  .then((b) => require('fs').writeFileSync('$TMP/portrait.b64', b.toString('base64')));
"
python3 "$ROOT/scripts/hero.py" "$TMP/portrait.b64" "$ROOT/assets/hero-{theme}.svg" "$TMP/data.json"
python3 "$ROOT/scripts/readme.py" "$TMP/data.json" "$ROOT"
# Social-preview cards for repos (upload by hand: Settings → General → Social preview).
node "$ROOT/scripts/social.cjs" "$TMP/data.json" "$ROOT/assets/social"
