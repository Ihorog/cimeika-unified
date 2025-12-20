#!/bin/bash

# CIMEIKA Deployment Verification Script
# Перевіряє стан розгортання локально та на production

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
LOCAL_BACKEND_URL="http://localhost:5000"
LOCAL_FRONTEND_URL="http://localhost:3000"
TIMEOUT=10

echo ""
echo "========================================="
echo "  CIMEIKA Deployment Verification"
echo "========================================="
echo ""

# Function to check URL accessibility
check_url() {
    local url=$1
    local name=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $name... "
    
    if response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout $TIMEOUT "$url" 2>/dev/null); then
        if [ "$response" -eq "$expected_status" ]; then
            echo -e "${GREEN}✅ OK${NC} (HTTP $response)"
            return 0
        else
            echo -e "${YELLOW}⚠️  WARNING${NC} (HTTP $response, expected $expected_status)"
            return 1
        fi
    else
        echo -e "${RED}❌ FAILED${NC} (Cannot connect)"
        return 1
    fi
}

# Function to check JSON response
check_json_endpoint() {
    local url=$1
    local name=$2
    local field=$3
    
    echo -n "Checking $name... "
    
    if response=$(curl -s --connect-timeout $TIMEOUT "$url" 2>/dev/null); then
        if echo "$response" | jq -e ".$field" > /dev/null 2>&1; then
            value=$(echo "$response" | jq -r ".$field")
            echo -e "${GREEN}✅ OK${NC} ($field: $value)"
            return 0
        else
            echo -e "${YELLOW}⚠️  WARNING${NC} (Field '$field' not found)"
            return 1
        fi
    else
        echo -e "${RED}❌ FAILED${NC} (Cannot connect or parse JSON)"
        return 1
    fi
}

# Function to check Docker container status
check_docker_container() {
    local container_name=$1
    
    echo -n "Checking Docker container $container_name... "
    
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        status=$(docker inspect --format='{{.State.Status}}' "$container_name" 2>/dev/null)
        health=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "none")
        
        if [ "$status" = "running" ]; then
            if [ "$health" = "healthy" ] || [ "$health" = "none" ]; then
                echo -e "${GREEN}✅ Running${NC}"
                return 0
            else
                echo -e "${YELLOW}⚠️  Running but health: $health${NC}"
                return 1
            fi
        else
            echo -e "${RED}❌ Status: $status${NC}"
            return 1
        fi
    else
        echo -e "${RED}❌ Not found${NC}"
        return 1
    fi
}

# Check if required commands exist
echo -e "${BLUE}[1/6] Checking prerequisites...${NC}"
echo ""

command -v curl >/dev/null 2>&1 || { echo -e "${RED}❌ curl is not installed${NC}"; exit 1; }
echo -e "${GREEN}✅ curl is installed${NC}"

command -v jq >/dev/null 2>&1 || { echo -e "${YELLOW}⚠️  jq is not installed (optional, for JSON parsing)${NC}"; }
command -v docker >/dev/null 2>&1 || { echo -e "${YELLOW}⚠️  Docker is not installed (needed for local deployment)${NC}"; }

echo ""
echo -e "${BLUE}[2/6] Checking Docker Compose services...${NC}"
echo ""

if command -v docker >/dev/null 2>&1; then
    check_docker_container "cimeika-postgres"
    check_docker_container "cimeika-redis"
    check_docker_container "cimeika-backend"
    check_docker_container "cimeika-frontend"
    check_docker_container "cimeika-celery-worker"
else
    echo -e "${YELLOW}⚠️  Docker not available, skipping container checks${NC}"
fi

echo ""
echo -e "${BLUE}[3/6] Checking Backend API...${NC}"
echo ""

BACKEND_SUCCESS=0
if check_url "$LOCAL_BACKEND_URL" "Backend root endpoint"; then
    ((BACKEND_SUCCESS++))
fi

if check_url "$LOCAL_BACKEND_URL/health" "Backend health endpoint"; then
    ((BACKEND_SUCCESS++))
fi

if command -v jq >/dev/null 2>&1; then
    if check_json_endpoint "$LOCAL_BACKEND_URL/api/v1/modules" "Modules API" "modules"; then
        ((BACKEND_SUCCESS++))
    fi
else
    if check_url "$LOCAL_BACKEND_URL/api/v1/modules" "Modules API"; then
        ((BACKEND_SUCCESS++))
    fi
fi

echo ""
echo -e "${BLUE}[4/6] Checking Frontend...${NC}"
echo ""

FRONTEND_SUCCESS=0
if check_url "$LOCAL_FRONTEND_URL" "Frontend homepage" 200; then
    ((FRONTEND_SUCCESS++))
fi

if check_url "$LOCAL_FRONTEND_URL/health" "Frontend health page" 200; then
    ((FRONTEND_SUCCESS++))
fi

echo ""
echo -e "${BLUE}[5/6] Checking configuration files...${NC}"
echo ""

echo -n "Checking docker-compose.yml... "
if [ -f "docker-compose.yml" ]; then
    echo -e "${GREEN}✅ Found${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
fi

echo -n "Checking vercel.json... "
if [ -f "vercel.json" ]; then
    echo -e "${GREEN}✅ Found${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
fi

echo -n "Checking .env file... "
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Found${NC}"
else
    echo -e "${YELLOW}⚠️  Not found (copy from .env.template)${NC}"
fi

echo -n "Checking GitHub Actions workflow... "
if [ -f ".github/workflows/vercel-deploy.yml" ]; then
    echo -e "${GREEN}✅ Found${NC}"
else
    echo -e "${RED}❌ Not found${NC}"
fi

echo ""
echo -e "${BLUE}[6/6] Deployment Summary${NC}"
echo ""
echo "==========================================="
echo -e "Backend Health:    $([ $BACKEND_SUCCESS -ge 2 ] && echo "${GREEN}✅ HEALTHY${NC}" || echo "${RED}❌ UNHEALTHY${NC}") ($BACKEND_SUCCESS/3 checks passed)"
echo -e "Frontend Health:   $([ $FRONTEND_SUCCESS -ge 1 ] && echo "${GREEN}✅ HEALTHY${NC}" || echo "${RED}❌ UNHEALTHY${NC}") ($FRONTEND_SUCCESS/2 checks passed)"
echo "==========================================="
echo ""

# Overall status
TOTAL_SUCCESS=$((BACKEND_SUCCESS + FRONTEND_SUCCESS))
TOTAL_CHECKS=5
if [ $TOTAL_SUCCESS -ge 4 ]; then
    echo -e "${GREEN}✅ Deployment verification PASSED${NC}"
    echo ""
    echo "Your CIMEIKA ecosystem is running correctly!"
    echo ""
    echo "Access points:"
    echo "  • Frontend:  $LOCAL_FRONTEND_URL"
    echo "  • Backend:   $LOCAL_BACKEND_URL"
    echo "  • Health UI: $LOCAL_FRONTEND_URL/health"
    echo "  • API Docs:  $LOCAL_BACKEND_URL/api/v1/modules"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Deployment verification FAILED${NC}"
    echo ""
    echo "Some services are not responding correctly."
    echo ""
    echo "Troubleshooting steps:"
    echo "  1. Check if Docker containers are running: docker compose ps"
    echo "  2. View logs: docker compose logs"
    echo "  3. Restart services: docker compose restart"
    echo "  4. Check .env configuration"
    echo ""
    exit 1
fi
