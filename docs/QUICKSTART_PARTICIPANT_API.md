# Quick Start Guide - CIMEIKA Participant API

## Environment Setup

Add to your `.env` file:
```bash
# For HuggingFace Space deployment
BACKEND_PORT=7860
BACKEND_HOST=0.0.0.0

# Required database configuration
POSTGRES_HOST=your_db_host
POSTGRES_DB=cimeika
POSTGRES_USER=cimeika_user
POSTGRES_PASSWORD=your_secure_password

# Participant API Key (keep secret!)
CIMEIKA_PARTICIPANT_KEY=your_secure_api_key_here
```

## Docker Deployment

```bash
# Build the image
docker build -t cimeika-api ./backend

# Run with port 7860 (HuggingFace standard)
docker run -p 7860:7860 \
  -e BACKEND_PORT=7860 \
  -e POSTGRES_HOST=your_db \
  -e POSTGRES_DB=cimeika \
  -e POSTGRES_USER=cimeika_user \
  -e POSTGRES_PASSWORD=your_password \
  -e CIMEIKA_PARTICIPANT_KEY=your_api_key \
  cimeika-api
```

## API Usage Examples

### 1. Health Check
```bash
curl http://localhost:7860/health
# Response: {"status":"ok"}
```

### 2. Readiness Check
```bash
curl http://localhost:7860/ready
# Response: {"status":"ok","deps":{"env":"ok"}}
```

### 3. System Status
```bash
curl http://localhost:7860/api/status | jq
```

Response example:
```json
{
  "active_persona": "ci",
  "активні_персони": 5,
  "розгортання": "HuggingFace / Docker",
  "статус": "running",
  "версія": "2.2.1",
  "загальна_кількість_взаємодій": 42,
  "uptime": "02:15:33",
  "timezone": "Europe/Kyiv",
  "utc_time": "2025-12-26T04:28:18.948770+00:00",
  "local_time": "2025-12-26T06:28:18.948766+02:00",
  "participant_api": {
    "enabled": true,
    "last_call_at": "2025-12-26T04:15:22.123456+00:00"
  },
  "requests_last_5m": 15,
  "errors_last_5m": 0
}
```

### 4. Analyze CI Failure

```bash
curl -X POST http://localhost:7860/api/participant/message \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_api_key_here" \
  -d '{
    "conversation_id": "ci-run-12345",
    "mode": "analysis",
    "topic": "npm ci failure on PR #42",
    "input": {
      "text": "npm ci failed with error: npm ERR! lockfile version mismatch. Expected 3, got 2",
      "artifacts": [],
      "metadata": {
        "source": "ci",
        "repo": "myorg/myrepo",
        "run_id": "12345",
        "pr": 42
      }
    }
  }' | jq
```

Response:
```json
{
  "participant": "cimeika-api",
  "message": "npm lockfile is out of sync. Run 'npm install' locally and commit the updated package-lock.json.",
  "severity": "error",
  "outputs": {
    "patch_unified_diff": null,
    "actions": [
      {
        "type": "patch",
        "title": "Regenerate package-lock.json",
        "details": "Run: rm -rf node_modules package-lock.json && npm install"
      },
      {
        "type": "check",
        "title": "Verify npm version",
        "details": "Ensure CI and local npm versions match"
      }
    ]
  }
}
```

## GitHub Actions Integration Example

```yaml
name: CI Analysis

on: [push, pull_request]

jobs:
  analyze-failures:
    runs-on: ubuntu-latest
    if: failure()
    steps:
      - name: Analyze CI Failure
        run: |
          curl -X POST ${{ secrets.CIMEIKA_API_URL }}/api/participant/message \
            -H "Content-Type: application/json" \
            -H "X-API-KEY: ${{ secrets.CIMEIKA_API_KEY }}" \
            -d "{
              \"conversation_id\": \"${{ github.run_id }}\",
              \"mode\": \"analysis\",
              \"topic\": \"CI failure on ${{ github.ref }}\",
              \"input\": {
                \"text\": \"${{ github.event.head_commit.message }}\",
                \"metadata\": {
                  \"source\": \"ci-cd\",
                  \"repo\": \"${{ github.repository }}\",
                  \"run_id\": \"${{ github.run_id }}\",
                  \"pr\": ${{ github.event.pull_request.number || 0 }}
                }
              }
            }"
```

## Testing the API

```bash
# Run all tests
cd backend
pytest tests/ -v

# Run specific test suites
pytest tests/test_participant.py -v  # Participant API tests
pytest tests/test_status.py -v       # Status endpoint tests
pytest tests/test_health.py -v       # Health check tests
```

## Recognized CI Failure Patterns

The API currently recognizes these common CI issues:

1. **Node.js version mismatches**
2. **npm lockfile conflicts**
3. **Python dependency installation failures**
4. **Ruff linting errors**
5. **Flake8 errors**
6. **Pytest import errors**
7. **Cancelled workflow runs**
8. **Test failures**
9. **Build timeouts**
10. **Docker build failures**

See `docs/ci_participant_protocol.md` for complete details.

## Security Notes

- **Never commit** `CIMEIKA_PARTICIPANT_KEY` to version control
- Use environment variables or secrets management (GitHub Secrets, HF Secrets, etc.)
- API key is validated on every request to `/api/participant/message`
- Rate limit: 30 requests per minute per key
- All requests are audited (timestamp, path, status, latency only - no payloads)

## HuggingFace Space Configuration

When deploying to HuggingFace Spaces:

1. Set secrets in Space settings:
   - `POSTGRES_HOST`
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `CIMEIKA_PARTICIPANT_KEY`

2. The app will automatically bind to port 7860 when `BACKEND_PORT=7860` is set

3. Health and readiness checks are available at standard paths

## Troubleshooting

### 401 Unauthorized
- Check that `X-API-KEY` header is present
- Verify the API key matches `CIMEIKA_PARTICIPANT_KEY` env var

### 429 Too Many Requests
- Rate limit is 30 requests per minute per API key
- Wait 60 seconds and retry

### 422 Unprocessable Entity
- Check request JSON structure matches schema
- Ensure required fields are present

### Connection Refused
- Verify `BACKEND_PORT` is set correctly
- Check that database connection details are correct in `/ready` endpoint
