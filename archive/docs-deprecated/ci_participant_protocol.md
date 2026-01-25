# CI Participant Protocol v1

## Overview

The CI Participant Protocol enables automated CI/CD systems to interact with CIMEIKA API for intelligent failure analysis and guidance. The API uses rule-based pattern matching to identify common CI failures and provide actionable remediation steps.

## Endpoint

**POST** `/api/participant/message`

## Authentication

All requests require an `X-API-KEY` header with a valid API key.

```bash
curl -X POST https://api.cimeika.com/api/participant/message \
  -H "X-API-KEY: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Rate Limiting

- **30 requests per minute** per API key
- Exceeding the limit returns `429 Too Many Requests`
- Rate limit counters reset every 60 seconds

## Request Schema

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
      "pr": 0
    }
  }
}
```

### Fields

- **conversation_id** (required): Unique identifier for conversation context
- **mode** (required): Operation mode
  - `analysis`: Analyze failure patterns and suggest actions
  - `autofix`: Attempt to generate patch (returns patch_unified_diff if possible)
  - `logger`: Log-only mode for passive monitoring
- **topic** (required): Brief description or context
- **input.text** (required): Text to analyze (logs, error messages, stack traces)
- **input.artifacts** (optional): Additional files as base64-encoded content
- **input.metadata** (optional): Context about the source

## Response Schema

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

### Fields

- **participant**: Always "cimeika-api"
- **message**: Human-readable analysis result
- **severity**: Issue severity level
- **outputs.patch_unified_diff**: Unified diff patch (null if not available)
- **outputs.actions**: List of suggested actions

## Recognized CI Failure Patterns

The rule engine recognizes the following patterns:

1. **Node.js Version Mismatch**
   - Detects: Version errors in npm/node
   - Suggests: Checking .nvmrc or package.json engines

2. **npm Lockfile Issues**
   - Detects: package-lock.json conflicts or outdated lockfiles
   - Suggests: Regenerating lockfile with npm install

3. **Python Dependency Installation Failures**
   - Detects: pip install errors, missing packages
   - Suggests: Verifying requirements.txt

4. **Ruff Linting Errors**
   - Detects: Ruff check failures
   - Suggests: Running `ruff check --fix .`

5. **Flake8 Errors**
   - Detects: Flake8 linting failures
   - Suggests: Running flake8 locally

6. **Pytest Import Errors**
   - Detects: Module not found during test collection
   - Suggests: Checking dependencies and PYTHONPATH

7. **Cancelled Workflow Runs**
   - Detects: Workflow cancellation
   - Suggests: Checking cancellation reason

8. **Test Failures**
   - Detects: Pytest or other test failures
   - Suggests: Running tests locally

9. **Build Timeouts**
   - Detects: Timeout errors
   - Suggests: Optimizing or increasing timeout

10. **Docker Build Failures**
    - Detects: Docker image build errors
    - Suggests: Testing build locally

## Example Usage

### Basic Analysis Request

```json
{
  "conversation_id": "ci-run-12345",
  "mode": "analysis",
  "topic": "npm ci failure on PR #42",
  "input": {
    "text": "npm ci failed with error: npm ERR! lockfile version mismatch. Expected 3, got 2",
    "metadata": {
      "source": "ci",
      "repo": "myorg/myrepo",
      "run_id": "12345",
      "pr": 42
    }
  }
}
```

### Response

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

## Security & Privacy

- **No secrets in responses**: API never returns sensitive data
- **Audit logging**: All requests logged with timestamp, path, status, and latency only
- **No payload logging**: Request/response bodies are not stored in audit logs
- **API key required**: All endpoints require valid X-API-KEY header

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded. Maximum 30 requests per minute."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Metrics Impact

Each successful `/api/participant/message` call:
- Increments the global interaction counter
- Updates `participant_api.last_call_at` timestamp
- Records request/error in rolling 5-minute window

These metrics are visible in `/api/status` endpoint.

## Future Enhancements

Future versions may include:
- LLM-powered analysis (beyond rule-based patterns)
- Actual patch generation with artifacts
- Multi-language support
- Custom pattern registration
- Webhook support for async analysis
