# GitHub Dev Contour

## Goal
One delegated automation process for all Cimeika repositories.

## Environments
- development
- staging
- production

## Mandatory GitHub features
- protected branches
- required status checks
- reusable workflows
- environment secrets
- dependabot
- scheduled health checks
- development auto deploy

## Flow
Issue -> branch -> PR -> required checks -> development deploy -> review -> merge

## Repo mapping
- core: `cimeika-unified-main`
- infra: `ci_gitapi-main`
- edge: `cimeika-backend-main`
- sidecars: `cit-main`, `ci-memory-main`
- assets: `media-main`
