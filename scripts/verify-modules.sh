#!/bin/bash
# Verification script for Cimeika 7-module structure

echo "==================================="
echo "Cimeika Modules Verification Script"
echo "==================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 - MISSING"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1 - MISSING"
        ERRORS=$((ERRORS + 1))
        return 1
    fi
}

echo "1. Checking Frontend Module Structure..."
echo "----------------------------------------"

MODULES=("Ci" "Calendar" "Gallery" "Kazkar" "Malya" "Nastrij" "Podija")

for module in "${MODULES[@]}"; do
    echo ""
    echo "Checking $module module..."
    check_dir "frontend/src/modules/$module"
    check_file "frontend/src/modules/$module/index.ts"
    check_file "frontend/src/modules/$module/page.tsx"
    check_file "frontend/src/modules/$module/types.ts"
    check_file "frontend/src/modules/$module/api.ts"
    check_file "frontend/src/modules/$module/ui.tsx"
    check_file "frontend/src/modules/$module/service.ts"
    check_file "frontend/src/modules/$module/store.ts"
done

echo ""
echo "2. Checking Backend API Structure..."
echo "-------------------------------------"

BACKEND_MODULES=("ci" "calendar" "gallery" "kazkar" "malya" "nastrij" "podija")

for module in "${BACKEND_MODULES[@]}"; do
    echo ""
    echo "Checking $module backend..."
    check_file "backend/api/$module.py"
    check_file "backend/models/${module}_models.py"
    check_file "backend/services/${module}_service.py"
done

echo ""
echo "3. Checking Documentation..."
echo "----------------------------"

check_dir "docs/modules"
for module in "${BACKEND_MODULES[@]}"; do
    check_file "docs/modules/$module.md"
done
check_file "docs/modules/README.md"

echo ""
echo "4. Checking Build..."
echo "--------------------"

cd frontend
if npm run build > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Frontend builds successfully"
else
    echo -e "${RED}✗${NC} Frontend build failed"
    ERRORS=$((ERRORS + 1))
fi
cd ..

echo ""
echo "==================================="
echo "Verification Summary"
echo "==================================="

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "All 7 modules are properly structured:"
    echo "  ✓ Frontend modules (types, api, page, ui)"
    echo "  ✓ Backend API routers"
    echo "  ✓ Backend models (DTOs)"
    echo "  ✓ Backend services"
    echo "  ✓ Documentation"
    echo "  ✓ Build succeeds"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) found${NC}"
    exit 1
fi
