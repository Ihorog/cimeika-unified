#!/bin/bash

# Script to download original logo files from GitHub comment attachments
# Run this script to fetch and place the original Cimeika logos

set -e

ASSETS_DIR="$(cd "$(dirname "$0")/../frontend/src/assets" && pwd)"

echo "=== Cimeika Logo Download Script ==="
echo "Assets directory: $ASSETS_DIR"
echo ""

# Image URLs from GitHub comment #3677365624
CIMEIKA_LOGO_URL="https://github.com/user-attachments/assets/85cb4090-480a-465e-b2e3-5924996ed602"
CI_ICON_URL="https://github.com/user-attachments/assets/aa61382b-4288-4631-b116-19df35dba9bb"

echo "Downloading Cimeika logo..."
if curl -L -o "$ASSETS_DIR/logo-cimeika.png" "$CIMEIKA_LOGO_URL"; then
    echo "✓ Cimeika logo downloaded successfully"
else
    echo "✗ Failed to download Cimeika logo"
    exit 1
fi

echo "Downloading Ci icon..."
if curl -L -o "$ASSETS_DIR/icon-ci.png" "$CI_ICON_URL"; then
    echo "✓ Ci icon downloaded successfully"
else
    echo "✗ Failed to download Ci icon"
    exit 1
fi

echo ""
echo "=== Download Complete ==="
echo "Logo files have been saved to: $ASSETS_DIR"
echo ""
echo "Files created:"
echo "  - logo-cimeika.png"
echo "  - icon-ci.png"
echo ""
echo "The application code has already been updated to use these PNG files."
echo "You can now remove the old SVG files if desired:"
echo "  git rm $ASSETS_DIR/logo-cimeika.svg $ASSETS_DIR/icon-ci.svg"
echo ""
