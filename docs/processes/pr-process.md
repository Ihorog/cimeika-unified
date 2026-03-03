# PR Process

_(stub)_

## Overview
How to create and handle Pull Requests in the Cimeika ecosystem.

## Requirements
Each PR must include:
- What changed
- Why it changed (root cause)
- How it was verified
- Risk assessment
- Rollback plan

## Flow
1. Create a branch from `main`.
2. Implement changes.
3. Verify (tests / checks / validation).
4. Open a Pull Request against `main`.
5. Await human approval.
6. Merge.

## Rules
- No direct commits to `main`.
- All changes go through branches and Pull Requests.
- PRs without verification or explanation are invalid.
