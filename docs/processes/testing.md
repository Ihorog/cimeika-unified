# Testing

_(stub)_

## Overview
Testing standards and practices for the Cimeika ecosystem.

## Principles
- All new functionality must be covered by tests.
- Tests must pass before a PR can be merged.
- Do not remove or disable existing tests without explicit justification.

## Test Types
- **Unit tests** — isolate individual functions/modules.
- **Integration tests** — verify interactions between modules.
- **End-to-end tests** — simulate real user flows.

## Running Tests
```bash
# Backend
cd backend && pytest

# Frontend
npm test
```

## CI
All tests run automatically on every PR via GitHub Actions (`ci.yml`).
