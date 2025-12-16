#!/bin/bash

# CIMEIKA Stop Script
# Stops all CIMEIKA services

set -e

echo "========================================="
echo "  Stopping CIMEIKA"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    exit 1
fi

# Stop services
echo "🛑 Stopping services..."
docker compose down

echo ""
echo "✅ CIMEIKA stopped successfully"
echo ""
echo "To remove volumes as well, run:"
echo "  docker compose down -v"
echo ""
