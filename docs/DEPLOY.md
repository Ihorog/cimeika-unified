# DEPLOY — Cimeika Deployment Guide

## Prerequisites

- Docker + Docker Compose
- PostgreSQL 15+ with pgvector extension
- Python 3.11+
- Node.js 18+

## Quick Start (Local)

```bash
# 1. Copy environment template
cp .env.example .env
# Edit .env: set POSTGRES_PASSWORD, OPENAI_API_KEY, etc.

# 2. Start all services
make dev
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/api/docs

# 3. Verify health
curl http://localhost:8000/health
curl http://localhost:8000/api/status
```

## Environment Variables

| Variable              | Required | Description                        |
|-----------------------|----------|------------------------------------|
| `POSTGRES_HOST`       | ✅        | PostgreSQL hostname                |
| `POSTGRES_DB`         | ✅        | Database name (default: cimeika)   |
| `POSTGRES_USER`       | ✅        | DB user                            |
| `POSTGRES_PASSWORD`   | ✅        | DB password                        |
| `OPENAI_API_KEY`      | optional | For AI features                    |
| `TELEGRAM_BOT_TOKEN`  | optional | For Telegram Face layer            |
| `SENTRY_DSN`          | optional | Error monitoring                   |
| `ENVIRONMENT`         | optional | development / production           |

## Database Initialisation

```bash
# Auto (on startup): SQLAlchemy creates tables via ORM
make db-init

# Manual seed from SQL file:
make db-seed
```

## Production Checklist

- [ ] All required env vars set in GitHub Secrets
- [ ] `POSTGRES_PASSWORD` is strong (>= 16 chars)
- [ ] `SENTRY_DSN` configured for error monitoring
- [ ] pgvector extension installed on PostgreSQL host
- [ ] CORS origins restricted to production domain
- [ ] Rate limiting active (default: 60 req/min)
- [ ] Health endpoint returning `"status": "healthy"`
- [ ] `/api/status` returning correct version and uptime

## Docker Compose Services

| Service    | Port  | Description          |
|------------|-------|----------------------|
| `backend`  | 8000  | FastAPI application  |
| `frontend` | 3000  | React/Vite SPA       |
| `postgres` | 5432  | PostgreSQL + pgvector|

## Running Tests

```bash
make test          # all tests
make backend-test  # backend only (pytest)
```

## CI/CD

GitHub Actions workflows:
- `ci.yml` — lint + test on every PR
- `vercel-deploy.yml` — frontend deploy to Vercel on merge to main
- `seo-health.yml` — SEO health check

No direct deploys to `main`. All changes go through PR → review → merge.
