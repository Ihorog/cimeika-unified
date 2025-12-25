.PHONY: help dev up down logs build clean test lint frontend-lint backend-lint backend-test frontend-build install

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "CIMEIKA Unified - Development Commands"
	@echo "======================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Docker Compose Commands
dev: ## Start all services in development mode
	docker compose up -d
	@echo "\n✅ Services started!"
	@echo "Backend API: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/api/docs"

up: dev ## Alias for dev

down: ## Stop all services
	docker compose down
	@echo "✅ Services stopped"

logs: ## View logs from all services
	docker compose logs -f

logs-backend: ## View backend logs
	docker compose logs -f backend

logs-frontend: ## View frontend logs
	docker compose logs -f frontend

build: ## Rebuild all Docker images
	docker compose build
	@echo "✅ Images rebuilt"

clean: ## Stop services and remove volumes (WARNING: deletes data!)
	docker compose down -v
	@echo "✅ Services stopped and volumes removed"

restart: down dev ## Restart all services

# Testing Commands
test: backend-test ## Run all tests
	@echo "✅ All tests completed"

backend-test: ## Run backend tests
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v

backend-test-cov: ## Run backend tests with coverage
	@echo "Running backend tests with coverage..."
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term

# Linting Commands
lint: backend-lint frontend-lint ## Run all linters
	@echo "✅ All linting completed"

backend-lint: ## Run backend linter (flake8)
	@echo "Running backend linter..."
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

backend-format: ## Format backend code with black
	@echo "Formatting backend code..."
	cd backend && black .

backend-format-check: ## Check backend formatting
	@echo "Checking backend formatting..."
	cd backend && black --check .

frontend-lint: ## Run frontend linter (eslint)
	@echo "Running frontend linter..."
	cd frontend && npm run lint

# Build Commands
frontend-build: ## Build frontend for production
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "✅ Frontend built"

# Installation Commands
install: ## Install dependencies locally (without Docker)
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm ci
	@echo "✅ Dependencies installed"

backend-install: ## Install backend dependencies only
	cd backend && pip install -r requirements.txt

frontend-install: ## Install frontend dependencies only
	cd frontend && npm ci

# Database Commands
db-init: ## Initialize database (run migrations)
	docker compose exec backend python init_db.py

# Development Helpers
shell-backend: ## Open a shell in the backend container
	docker compose exec backend /bin/bash

shell-frontend: ## Open a shell in the frontend container
	docker compose exec frontend /bin/sh

shell-db: ## Open PostgreSQL shell
	docker compose exec postgres psql -U ${POSTGRES_USER:-cimeika_user} -d ${POSTGRES_DB:-cimeika}

# Environment Setup
setup: ## Initial setup (copy .env.example and install dependencies)
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "⚠️  Please edit .env and set your passwords and API keys!"; \
	else \
		echo ".env already exists, skipping..."; \
	fi
	@echo "Installing dependencies..."
	$(MAKE) install
	@echo "✅ Setup complete! Edit .env then run: make dev"

# Health Checks
health: ## Check health of all services
	@echo "Checking backend health..."
	@curl -s http://localhost:8000/health | jq . || echo "Backend not responding"
	@echo "\nChecking backend readiness..."
	@curl -s http://localhost:8000/ready | jq . || echo "Backend not ready"
	@echo "\nChecking frontend..."
	@curl -s -o /dev/null -w "Frontend: %{http_code}\n" http://localhost:3000 || echo "Frontend not responding"

# CI Commands (used by GitHub Actions)
ci-backend: ## Run backend CI checks
	cd backend && python -m pip install --upgrade pip
	cd backend && pip install -r requirements.txt
	cd backend && pip install flake8 black pytest
	cd backend && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	cd backend && pytest tests/ -v

ci-frontend: ## Run frontend CI checks
	cd frontend && npm ci
	cd frontend && npm run lint
	cd frontend && npm run build

ci: ci-backend ci-frontend ## Run all CI checks
	@echo "✅ CI checks passed"
