#!/bin/bash

# CIMEIKA Quick Start Script
# This script helps you set up and run the CIMEIKA ecosystem

set -e

echo "========================================="
echo "  CIMEIKA Quick Start"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed"

# Check if .env file exists
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.template .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file and set your configuration:"
    echo "   - Database credentials"
    echo "   - Redis password"
    echo "   - API keys (OpenAI, Anthropic)"
    echo "   - Secret key for Flask"
    echo ""
    read -p "Press Enter after you've edited .env to continue..."
else
    echo "✅ .env file exists"
fi

echo ""
echo "🚀 Starting CIMEIKA ecosystem..."
echo ""

# Start services
docker compose up -d

echo ""
echo "========================================="
echo "  CIMEIKA is starting!"
echo "========================================="
echo ""
echo "Services:"
echo "  • Frontend:  http://localhost:3000"
echo "  • Backend:   http://localhost:5000"
echo "  • Health:    http://localhost:5000/health"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop:      docker compose down"
echo ""
