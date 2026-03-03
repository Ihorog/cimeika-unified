# CI/CD

_(stub)_

## Overview
Continuous integration and deployment for the Cimeika ecosystem.

## Workflows
All workflows are defined in `.github/workflows/`:

| Workflow                   | Trigger              | Purpose                          |
|----------------------------|----------------------|----------------------------------|
| `ci.yml`                   | Push / PR to `main`  | Lint, test, build                |
| `vercel-deploy.yml`        | Merge to `main`      | Deploy frontend to Vercel        |
| `seo-health.yml`           | Schedule / manual    | SEO health checks                |
| `copilot-task-detect.yml`  | Issue comment        | Detect and dispatch Copilot tasks|
| `copilot-approve.yml`      | Issue comment        | Approve Copilot task execution   |
| `copilot-execute.yml`      | Workflow dispatch    | Execute approved Copilot tasks   |

## Permissions
- Workflows use minimal permissions: `contents: read` by default.
- Write permissions are added only where explicitly required.

## Rules
- No production deployments without a passing CI run.
- All secrets must be stored in GitHub Secrets — never hard-coded.
- See [Secrets Management](secrets-management.md) for credential handling.

## References
- See `.github/workflows/README.md` for workflow documentation.
