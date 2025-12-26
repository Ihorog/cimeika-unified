# API Endpoints Quick Reference - v2.2.1

## Health & Readiness

### GET /health
**Purpose:** Basic health check for load balancers
**Auth:** None required
**Response:**
```json
{"status": "ok"}
```

### GET /ready
**Purpose:** Validate environment configuration
**Auth:** None required
**Response:**
```json
{
  "status": "ok",
  "deps": {"env": "ok"}
}
```
Returns `"not_ready"` if required env vars missing.

## System Status

### GET /api/status
**Purpose:** Comprehensive system metrics
**Auth:** None required
**Response:**
```json
{
  "active_persona": "ci",
  "активні_персони": 5,
  "розгортання": "HuggingFace / Docker",
  "статус": "running",
  "версія": "2.2.1",
  "загальна_кількість_взаємодій": <int>,
  "uptime": "HH:MM:SS",
  "timezone": "Europe/Kyiv",
  "utc_time": "<ISO8601+00:00>",
  "local_time": "<ISO8601+02:00|+03:00>",
  "participant_api": {
    "enabled": true,
    "last_call_at": "<ISO8601|null>"
  },
  "requests_last_5m": <int>,
  "errors_last_5m": <int>
}
```

**Notes:**
- `local_time` offset changes with DST (winter: +02:00, summer: +03:00)
- `uptime` resets on app restart
- `загальна_кількість_взаємодій` increments with each participant API call

## Participant API

### POST /api/participant/message
**Purpose:** Analyze CI failures and provide guidance
**Auth:** Required - `X-API-KEY` header
**Rate Limit:** 30 requests/minute per key
**Content-Type:** application/json

**Request:**
```json
{
  "conversation_id": "string",
  "mode": "analysis|autofix|logger",
  "topic": "string",
  "input": {
    "text": "string",
    "artifacts": [
      {
        "name": "string",
        "content_base64": "string"
      }
    ],
    "metadata": {
      "source": "ci|ci-cd|user",
      "repo": "string",
      "run_id": "string",
      "pr": <int>
    }
  }
}
```

**Response:**
```json
{
  "participant": "cimeika-api",
  "message": "string",
  "severity": "info|warn|error",
  "outputs": {
    "patch_unified_diff": "string|null",
    "actions": [
      {
        "type": "suggest|check|patch",
        "title": "string",
        "details": "string"
      }
    ]
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid X-API-KEY
- `422 Unprocessable Entity` - Invalid request schema
- `429 Too Many Requests` - Rate limit exceeded (wait 60s)

## Recognized CI Patterns

The rule engine detects these failure patterns:

1. **node_version_mismatch** - Node.js engine compatibility issues
2. **npm_lockfile_mismatch** - package-lock.json out of sync
3. **python_deps_install_failed** - pip install errors
4. **ruff_linting_errors** - Ruff check failures
5. **flake8_errors** - Flake8 linting issues
6. **pytest_import_errors** - Module import failures
7. **cancelled_run** - Workflow cancellations
8. **test_failures** - Assertion errors in tests
9. **build_timeout** - Long-running processes
10. **docker_build_failed** - Container build errors

## Quick Examples

### Health Check
```bash
curl http://localhost:7860/health
```

### Check Status
```bash
curl http://localhost:7860/api/status | jq
```

### Analyze CI Failure
```bash
curl -X POST http://localhost:7860/api/participant/message \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_key_here" \
  -d '{
    "conversation_id": "ci-123",
    "mode": "analysis",
    "topic": "npm error",
    "input": {
      "text": "npm ci failed with lockfile version mismatch",
      "metadata": {"source": "ci"}
    }
  }'
```

## Environment Variables

### Required
```bash
POSTGRES_HOST=host
POSTGRES_DB=cimeika
POSTGRES_USER=user
POSTGRES_PASSWORD=password
CIMEIKA_PARTICIPANT_KEY=key
```

### Optional
```bash
BACKEND_PORT=7860           # Default: 8000
BACKEND_HOST=0.0.0.0        # Default: 0.0.0.0
ENVIRONMENT=production      # Default: development
LOG_LEVEL=INFO              # Default: INFO
SENTRY_DSN=dsn              # Optional monitoring
OPENAI_API_KEY=key          # Optional AI features
```

## Deployment Ports

- **Development:** 8000
- **HuggingFace Spaces:** 7860
- **Custom:** Set via `BACKEND_PORT`

## API Documentation

Interactive docs available at:
- Swagger UI: `http://localhost:7860/api/docs`
- ReDoc: `http://localhost:7860/api/redoc`
- OpenAPI JSON: `http://localhost:7860/api/openapi.json`

## Monitoring & Metrics

All endpoints except `/health` and `/ready` are rate limited (60/min, 1000/hour).

Metrics tracked:
- Total interactions (via participant API)
- Application uptime
- Requests in last 5 minutes
- Errors in last 5 minutes
- Participant API last call timestamp

## Security Notes

- Never commit `CIMEIKA_PARTICIPANT_KEY` to version control
- Use secrets management (GitHub Secrets, HF Secrets, env vars)
- Rotate API keys periodically
- Monitor rate limit violations
- Audit logs stored in memory (last 1000 entries)

## Version

Current: **v2.2.1**

## Support

- Protocol Spec: `docs/ci_participant_protocol.md`
- Quickstart: `docs/QUICKSTART_PARTICIPANT_API.md`
- Implementation: `IMPLEMENTATION_PARTICIPANT_API.md`
- Tests: `backend/tests/test_*.py`
