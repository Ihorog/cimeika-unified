# Release Process

_(stub)_

## Overview
Versioning and release procedures for the Cimeika ecosystem.

## Versioning
- Follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`.
- Bump `PATCH` for bug fixes, `MINOR` for new features, `MAJOR` for breaking changes.

## Steps
1. Ensure all changes are merged to `main` via approved PRs.
2. Update `CHANGELOG.md` with the new version and release notes.
3. Tag the release commit: `git tag vX.Y.Z`.
4. Push the tag to trigger the release workflow.
5. Verify deployment in staging before production.

## Rules
- No deployment, no production actions without human approval.
- Every release must have a corresponding CHANGELOG entry.
