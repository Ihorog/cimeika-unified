# Delegated Execution

## Principle
One task enters the system once and is routed by repo role.

## Flow
1. classify intent
2. assign owner repo
3. compute dependent repos
4. execute repo-local changes
5. run repo-local checks
6. sync registry
7. run cross-repo checks
8. deploy development
9. run health checks
10. approve or iterate

## Repo roles
- product: `cimeika-unified-main`
- infra: `ci_gitapi-main`
- edge: `cimeika-backend-main`
- memory: `ci-memory-main`
- media: `media-main`
- local_sidecar: `cit-main`

## Hard rules
- one product core
- one infra core
- one registry truth
- one canonical frontend
- no duplicate runtime roles
