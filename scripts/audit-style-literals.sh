#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Allowed literal zones: token adapter and generated artifacts only.
ALLOWLIST=(
  "frontend/src/tokens"
  "frontend/src/theme"
  "frontend/src/styles/design-system.css"
  "frontend/src/styles/themes.css"
  "src/tokens"
  "src/theme"
  "src/design-system/tokens"
  "tokens"
  ".github"
  "node_modules"
  "dist"
  "build"
  "*/_bak_*"
  "ci/ui/_bak_*"
  "ci/ui"
)

EXCLUDES=()
for path in "${ALLOWLIST[@]}"; do
  EXCLUDES+=("--glob=!${path}")
done

PATTERN='#([0-9A-Fa-f]{3,8})\b|rgba?\(|\b[0-9]+px\b|\b[0-9]+rem\b|box-shadow|border-radius|cubic-bezier|transition\s*:'

echo "Running style literal audit..."

MATCHES=$(rg -n -S "$PATTERN" \
  --glob='*.{ts,tsx,js,jsx,css,scss,sass,less,vue,html}' \
  "${EXCLUDES[@]}" \
  . || true)

if [[ -n "$MATCHES" ]]; then
  echo "Forbidden styling literals found outside token adapter zones:"
  echo "$MATCHES"
  exit 1
fi

echo "Style literal audit passed."
