# Changelog

All notable changes to CIMEIKA Unified will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- MVP Production Backbone implementation (PR-01 to PR-06)
- CI/CD pipeline with GitHub Actions
- Comprehensive test suite (47 passing tests)
- Production readiness checklist
- Development tooling (Makefile, docker-compose)

## [0.1.0] - 2024-12-25

### Added - PR-01: Governance + CI Skeleton
- GitHub Actions CI workflow (`.github/workflows/ci.yml`)
  - Frontend pipeline: install → lint → build
  - Backend pipeline: install → lint → tests
- CODEOWNERS file with @Ihorog as repository owner
- CONTRIBUTING.md with PR requirements and development workflow
- .editorconfig for consistent code style across editors

### Added - PR-02: Backend Bootstrap
- Dedicated health check endpoints (`/health`, `/ready`)
  - Health endpoint for basic status checks
  - Readiness endpoint with environment validation
- Centralized configuration management (`app/core/config.py`)
  - Environment variable handling
  - Configuration validation
  - Production safety checks
- Structured logging system (`app/core/logging.py`)
  - JSON logging for production
  - Human-readable logs for development
  - Context-aware logging functions
- Comprehensive test suite
  - 6 health endpoint tests
  - 11 module endpoint tests
- Updated backend README with complete development guide

### Added - PR-03: Basic Security Layer
- Rate limiting middleware (`app/core/rate_limit.py`)
  - Per-IP rate limiting (60 requests/min, 1000/hour)
  - Automatic cleanup of old entries
  - Configurable exclusion paths (health checks, docs)
  - HTTP 429 responses with Retry-After header
- CORS security validation
  - No wildcard allowed in production
  - Specific origin allowlist
  - Configuration validation at startup
- Security test suite (10 tests)
  - Rate limiting behavior
  - CORS configuration validation
  - Pydantic input validation

### Added - PR-04: Monitoring-ready
- Optional Sentry integration (`app/core/monitoring.py`)
  - Initializes only if SENTRY_DSN configured
  - FastAPI and Starlette integrations
  - Automatic error capture
  - Health check request filtering
  - Graceful degradation when unavailable
- Enhanced readiness endpoint
  - Reports monitoring status
  - Environment sanity checks
- Monitoring test suite (10 tests)
  - Works with and without Sentry
  - Verifies graceful degradation
  - Tests endpoint stability

### Added - PR-05: Docker/Compose for dev
- Comprehensive `.env.example` template
  - Organized configuration sections
  - Security notes and best practices
  - Quick start instructions
- Makefile with 30+ development commands
  - Docker Compose wrappers (dev, down, logs, restart)
  - Testing commands (test, lint, coverage)
  - CI commands matching GitHub Actions
  - Setup and helper utilities
- Updated README.md
  - Three setup options documented
  - Docker Compose (recommended)
  - Makefile commands (convenience)
  - Local development (no Docker)
- Verified docker-compose.yml configuration

### Added - PR-06: Production Checklist + Release Discipline
- Production readiness checklist (`docs/production-checklist.md`)
  - Security verification steps
  - Monitoring configuration
  - Testing requirements
  - Deployment procedures
  - Smoke test list
  - Runbook with common issues
- CHANGELOG.md (this file)
- Semantic versioning policy (see below)
- Deployment documentation
  - Production URLs documented
  - Manual smoke test procedures
  - External access verification

### Changed
- Upgraded main.py to use new config and logging systems
- Enhanced /ready endpoint with comprehensive checks
- Updated backend README with architecture details

### Security
- Rate limiting prevents abuse (429 on limit exceed)
- CORS restricted to specific origins (no wildcard)
- Configuration validation prevents insecure production deploys
- All secrets managed via environment variables

### Testing
- 47 total tests passing:
  - 6 health endpoint tests
  - 11 module endpoint tests
  - 10 security tests
  - 10 monitoring tests
  - 5 Kazkar legend tests
  - 5 SEO matrix tests (passing subset)
- All critical paths covered
- CI runs automatically on PRs

### Documentation
- Complete API documentation at `/api/docs`
- Backend README with setup instructions
- Production checklist with verification steps
- CONTRIBUTING.md with PR guidelines
- Architecture preserved in existing docs

## Semantic Versioning Policy

CIMEIKA Unified follows [Semantic Versioning 2.0.0](https://semver.org/):

### Version Format: MAJOR.MINOR.PATCH

**MAJOR version** (X.0.0) - Incompatible API changes:
- Breaking changes to public APIs
- Removal of deprecated features
- Database schema changes requiring migration
- Major architecture changes

**MINOR version** (0.X.0) - New features, backwards compatible:
- New modules or endpoints
- New configuration options
- Enhanced functionality
- Performance improvements
- Non-breaking API additions

**PATCH version** (0.0.X) - Backwards compatible bug fixes:
- Bug fixes
- Security patches
- Documentation updates
- Dependency updates (non-breaking)
- Minor refactoring

### Pre-release versions
- Alpha: `X.Y.Z-alpha.N` - Early development, unstable
- Beta: `X.Y.Z-beta.N` - Feature complete, testing phase
- RC: `X.Y.Z-rc.N` - Release candidate, final testing

### Examples
- `0.1.0` - Initial MVP release
- `0.2.0` - New Gallery module features
- `0.2.1` - Fix rate limiting bug
- `1.0.0` - First production-ready release
- `1.0.0-beta.1` - Beta version before 1.0.0

### Release Process

1. **Version Bump**
   - Update version in relevant files:
     - `backend/app/core/config.py` (`API_VERSION`)
     - `frontend/package.json` (`version`)
   - Commit: `chore: bump version to X.Y.Z`

2. **Update Changelog**
   - Move unreleased changes to new version section
   - Add release date
   - Commit: `docs: update CHANGELOG for X.Y.Z`

3. **Create Git Tag**
   ```bash
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push origin vX.Y.Z
   ```

4. **GitHub Release**
   - Create release from tag
   - Copy changelog entry to release notes
   - Attach build artifacts if applicable

5. **Deploy**
   - Follow production checklist
   - Verify smoke tests pass
   - Monitor for first hour

### Deprecation Policy

- Features marked deprecated in version X.Y will be removed in version (X+1).0
- Deprecation warnings logged for 1 major version before removal
- Alternatives documented before deprecation

## External Access & Deployed URLs

### Production (TBD)
- **Frontend:** TBD
- **Backend API:** TBD
- **API Docs:** TBD

### Staging (TBD)
- **Frontend:** TBD
- **Backend API:** TBD

### Development
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs
- **Database:** localhost:5432

### Manual Smoke Test Checklist

See `docs/production-checklist.md` for complete smoke test procedures.

Quick smoke test URLs (update with production domains):
```bash
# Health checks
curl https://api.DOMAIN/health
curl https://api.DOMAIN/ready

# API
curl https://api.DOMAIN/api/v1/modules/

# Frontend
open https://DOMAIN/ci
```

---

## Migration Guide

### Upgrading from Pre-MVP to 0.1.0

1. **Environment Variables**
   - Copy `.env.example` to `.env`
   - Set `ENVIRONMENT=development`
   - Set `LOG_LEVEL=INFO`
   - Update all passwords (no defaults!)
   - Configure CORS with specific origins

2. **Database**
   - Run migrations: `make db-init`
   - Verify database connectivity

3. **Dependencies**
   - Backend: `pip install -r requirements.txt`
   - Frontend: `npm ci`

4. **Configuration**
   - Optional: Add `SENTRY_DSN` for monitoring
   - Optional: Add AI API keys

5. **Verification**
   - Run tests: `make test`
   - Start services: `make dev`
   - Check health: `make health`

---

**Maintained by:** CIMEIKA Team  
**Repository:** https://github.com/Ihorog/cimeika-unified
