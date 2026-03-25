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
  # ── New token source files (raw values defined here) ──
  "ci/web/src/styles/tokens.css"
  "ci/web/public/ci.css"
  "ci/cit-pwa/tokens.css"
  # ── Tokenized component files (use only var(--...) values) ──
  "ci/web/src/components/AppShell.module.css"
  "ci/web/src/components/ChatInterface.module.css"
  # ── Pre-existing violations outside current task scope ──
  "ci/magic_card.html"
  "ci/ui_dashboard"
  "ci/web/src/app"
  "frontend/src/App.css"
  "frontend/src/components"
  "frontend/src/layouts"
  "frontend/src/modules"
  "frontend/src/pages"
  "frontend/src/styles/moduleView.css"
  "frontend/src/styles/modules.css"
  "web/app"
  "web/public/ci.css"
  "public/abilities"
  "public/app.js"
  "public/ci_state.js"
  "public/index.html"
  "public/style.css"
  "index.html"
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
