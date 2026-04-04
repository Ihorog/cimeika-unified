# Canonical Decision Record

## Repo roles
- `cimeika-unified-main` = product core
- `ci_gitapi-main` = infra core
- `cimeika-backend-main` = edge runtime
- `cit-main` = local sidecar
- `ci-memory-main` = memory sidecar
- `media-main` = assets

## Canonical paths
### cimeika-unified-main
- frontend root: `app/`
- shared UI: `components/`
- backend: `backend/`

### ci_gitapi-main
- runtime: `app/`
- registry: `registry/`
- content/state: `content/`
- failover: `packages/failover-core/`

## Freeze scope
Inside `cimeika-unified-main`:
- `frontend/`
- `web/`
- `ci/web/`
- `ci/ui/`
- `ci/cit-pwa/`
- `ci/ui_dashboard/`

## Mandatory rules
- one product core
- one infra core
- one registry truth
- one canonical frontend
- no duplicate runtime roles
