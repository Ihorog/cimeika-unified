# Production Checklist

This checklist defines the criteria for production readiness of CIMEIKA Unified. All items must be verified before deploying to production.

## Table of Contents
- [Security](#security)
- [Monitoring](#monitoring)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Performance](#performance)
- [Backup & Recovery](#backup--recovery)

---

## Security

### Configuration
- [ ] All passwords changed from defaults (`POSTGRES_PASSWORD`, `SECRET_KEY`, `REDIS_PASSWORD`)
- [ ] `ENVIRONMENT` set to `production`
- [ ] `DEBUG` disabled (`DEBUG=false`)
- [ ] CORS configured with specific origins (no wildcard `*`)
- [ ] All secrets stored in secure environment variables (not in code)
- [ ] API keys rotated if they were exposed during development

### SSL/TLS
- [ ] HTTPS enabled for frontend
- [ ] HTTPS enabled for backend API
- [ ] Valid SSL certificates installed
- [ ] HTTP redirects to HTTPS
- [ ] HSTS headers configured

### Rate Limiting
- [ ] Rate limiting enabled (verify 429 responses work)
- [ ] Rate limits appropriate for production load
- [ ] Health check endpoints excluded from rate limiting

### Dependencies
- [ ] All dependencies scanned for vulnerabilities
- [ ] No critical or high severity vulnerabilities
- [ ] Dependencies pinned to specific versions
- [ ] `requirements.txt` / `package-lock.json` committed

### Authentication & Authorization
- [ ] API authentication implemented (if required)
- [ ] Authorization rules enforced
- [ ] Session management secure
- [ ] CSRF protection enabled (if applicable)

---

## Monitoring

### Error Tracking
- [ ] Sentry configured with production DSN
- [ ] Error alerts set up
- [ ] Error grouping configured
- [ ] Release tracking enabled

### Logging
- [ ] Structured logging enabled
- [ ] Log aggregation configured (e.g., CloudWatch, Datadog)
- [ ] Log retention policy set
- [ ] Sensitive data not logged (PII, secrets)

### Health Checks
- [ ] `/health` endpoint responding
- [ ] `/ready` endpoint reporting correct status
- [ ] Load balancer health checks configured
- [ ] Health check alerts set up

### Metrics
- [ ] Application metrics collected
- [ ] Infrastructure metrics monitored
- [ ] Database metrics tracked
- [ ] Alert thresholds configured

---

## Testing

### Automated Tests
- [ ] All unit tests passing (`make test`)
- [ ] Integration tests passing
- [ ] Security tests passing (`tests/test_security.py`)
- [ ] Health check tests passing (`tests/test_health.py`)
- [ ] Module tests passing (`tests/test_modules.py`)
- [ ] Monitoring tests passing (`tests/test_monitoring.py`)
- [ ] Minimum test coverage: 70%

### Manual Testing
- [ ] Smoke tests completed (see [Smoke Test List](#smoke-test-list))
- [ ] All 7 modules accessible
- [ ] API documentation accurate (`/api/docs`)
- [ ] Frontend loads correctly
- [ ] CORS working for production frontend

### Performance Testing
- [ ] Load testing completed
- [ ] API response times acceptable (< 200ms for health checks)
- [ ] Database queries optimized
- [ ] No memory leaks detected

---

## Deployment

### Infrastructure
- [ ] Database deployed and accessible
- [ ] Database backups configured
- [ ] Backend deployed to production environment
- [ ] Frontend deployed to CDN/hosting
- [ ] Load balancer configured
- [ ] Auto-scaling configured (if applicable)

### Database
- [ ] Database migrations run successfully
- [ ] Database connection pooling configured
- [ ] Database credentials secured
- [ ] Database monitoring enabled

### CI/CD
- [ ] CI pipeline green (`.github/workflows/ci.yml`)
- [ ] Deployment pipeline tested
- [ ] Rollback procedure documented
- [ ] Zero-downtime deployment verified

### Environment Variables
- [ ] All required env vars set:
  - `ENVIRONMENT=production`
  - `LOG_LEVEL=WARNING` or `ERROR`
  - `POSTGRES_HOST`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
  - `SECRET_KEY` (unique value)
  - `CORS_ORIGINS` (production URLs only)
- [ ] Optional env vars configured as needed:
  - `SENTRY_DSN`
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`

---

## Documentation

### User Documentation
- [ ] README.md up to date
- [ ] API documentation complete (`/api/docs`)
- [ ] User guides written
- [ ] Troubleshooting guide available

### Technical Documentation
- [ ] Architecture documented (`docs/ARCHITECTURE.md`)
- [ ] Deployment process documented
- [ ] Runbook created (see below)
- [ ] Recovery procedures documented

### Code Documentation
- [ ] Code comments adequate
- [ ] API endpoints documented
- [ ] Environment variables documented

---

## Performance

### Response Times
- [ ] Health checks: < 100ms
- [ ] API endpoints: < 500ms (p95)
- [ ] Frontend load time: < 3s
- [ ] Database queries: < 100ms (p95)

### Resource Usage
- [ ] CPU usage acceptable (< 70% average)
- [ ] Memory usage stable (no leaks)
- [ ] Database connections managed
- [ ] File descriptors within limits

### Caching
- [ ] Static assets cached
- [ ] API responses cached (where appropriate)
- [ ] CDN configured for frontend

---

## Backup & Recovery

### Backups
- [ ] Database backups automated
- [ ] Backup retention policy set (30 days minimum)
- [ ] Backups tested and verified
- [ ] Backup monitoring enabled

### Disaster Recovery
- [ ] Recovery procedures documented
- [ ] Recovery time objective (RTO) defined
- [ ] Recovery point objective (RPO) defined
- [ ] DR drill completed

---

## Smoke Test List

### Backend API
1. **Health Check**
   - URL: `https://api.production-domain.com/health`
   - Expected: HTTP 200, `{"status": "ok"}`

2. **Readiness Check**
   - URL: `https://api.production-domain.com/ready`
   - Expected: HTTP 200, `{"status": "ready"}`, all checks pass

3. **API Root**
   - URL: `https://api.production-domain.com/`
   - Expected: HTTP 200, lists 7 modules

4. **API Docs**
   - URL: `https://api.production-domain.com/api/docs`
   - Expected: Swagger UI loads

5. **Modules List**
   - URL: `https://api.production-domain.com/api/v1/modules/`
   - Expected: HTTP 200, returns 7 modules: ci, kazkar, podija, nastrij, malya, gallery, calendar

6. **Module Status**
   - URL: `https://api.production-domain.com/api/v1/modules/status`
   - Expected: HTTP 200, status for all 7 modules

7. **Individual Module (Ci)**
   - URL: `https://api.production-domain.com/api/v1/ci/`
   - Expected: HTTP 200, Ci module responds

8. **Rate Limiting**
   - Make 65+ requests rapidly to any endpoint
   - Expected: HTTP 429 after exceeding limit

9. **CORS**
   - Request from production frontend origin
   - Expected: CORS headers present, request succeeds
   - Request from unauthorized origin
   - Expected: CORS error

### Frontend
1. **Home Page**
   - URL: `https://production-domain.com/`
   - Expected: Loads without errors, redirects to `/ci`

2. **Ci Module**
   - URL: `https://production-domain.com/ci`
   - Expected: Ci interface loads

3. **All 7 Modules Accessible**
   - Test each: `/ci`, `/kazkar`, `/podija`, `/nastrij`, `/malya`, `/gallery`, `/calendar`
   - Expected: Each module loads correctly

4. **Theme Switching**
   - Navigate to Kazkar
   - Expected: Night theme applied
   - Navigate to any other module
   - Expected: Day theme applied

5. **API Integration**
   - Interact with Ci module
   - Expected: Backend API calls successful

---

## Runbook

### Common Issues

#### Backend Not Responding
```bash
# Check backend health
curl https://api.production-domain.com/health

# Check logs
make logs-backend
# OR
docker compose logs backend

# Restart backend
docker compose restart backend
```

#### Database Connection Issues
```bash
# Check database connectivity
make shell-db

# Check connection pool
# Review logs for connection errors
make logs-backend | grep -i postgres

# Restart database (careful!)
docker compose restart postgres
```

#### High CPU/Memory Usage
```bash
# Check resource usage
docker stats

# Check for slow queries
# Connect to database and run:
# SELECT * FROM pg_stat_activity WHERE state = 'active';

# Restart services if needed
docker compose restart backend
```

#### Rate Limiting Too Aggressive
```bash
# Temporarily adjust rate limits (requires code change)
# Edit backend/main.py:
# RateLimitMiddleware(requests_per_minute=120, requests_per_hour=2000)
# Then deploy
```

### Emergency Contacts
- **Technical Lead:** @Ihorog
- **On-Call:** TBD
- **Escalation:** TBD

### External Dependencies
- **Sentry:** https://sentry.io
- **OpenAI API:** https://platform.openai.com/account/api-keys
- **Anthropic API:** https://console.anthropic.com
- **Database Provider:** TBD
- **Hosting Provider:** TBD

---

## Verification Sign-off

Before deploying to production, the following roles must sign off:

- [ ] **Developer:** Code changes reviewed and tested
- [ ] **DevOps/SRE:** Infrastructure configured and tested
- [ ] **Security:** Security checklist completed
- [ ] **Product Owner:** Features verified
- [ ] **Technical Lead:** Overall approval

**Date:** _______________

**Approved By:** _______________

---

## Post-Deployment

### Immediate (First Hour)
- [ ] Monitor error rates in Sentry
- [ ] Check health endpoints every 5 minutes
- [ ] Monitor response times
- [ ] Verify frontend loads correctly
- [ ] Test key user flows

### Short-term (First Day)
- [ ] Review all error logs
- [ ] Check database performance
- [ ] Monitor resource usage
- [ ] Gather user feedback
- [ ] Address any issues

### Long-term (First Week)
- [ ] Review metrics and trends
- [ ] Optimize based on real traffic
- [ ] Update documentation with learnings
- [ ] Plan next iteration

---

**Last Updated:** 2024-12-25  
**Version:** 1.0.0  
**Owner:** CIMEIKA Team
