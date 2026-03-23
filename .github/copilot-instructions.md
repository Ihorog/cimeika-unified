# Cimeika — Global GitHub Copilot Instructions

---

## 0. OPERATOR PROTOCOL — AUTHOR ↔ COPILOT DIVISION OF RESPONSIBILITY

**Effective: 2026-03-23. Permanent. Non-negotiable.**

### Role Definitions

| Role | Who | Responsibilities |
|------|-----|------------------|
| **Author** | Ihorog (human) | Ideas, concepts, content, approval, final say |
| **Copilot** | GitHub Copilot | All code, all structure, all repository organization, all GitHub operations |

### Author's Interface: Conversation Only

The Author interacts **exclusively through chat** (this conversation).

The Author does NOT:
- write code
- organize files or directories
- make commits or branches
- manage GitHub settings
- know or need to know GitHub mechanics

The Author DOES:
- describe what the system should do, feel, or contain
- review finished results (PR, deployed UI, screenshots)
- approve or reject via a single button (Merge / Close)
- provide personal materials (texts, images, ideas, stories)

### Copilot's Responsibilities

Copilot owns **everything technical**, including:
- repository structure and file organization
- code architecture and implementation
- branch creation and PR management
- `manifest.json` and `SYSTEM_WILL.md` updates
- identifying and eliminating repeated patterns
- proposing module activations when intent patterns emerge
- cross-repo synchronization (cimeika-unified, cit, ciwiki, cimeika-core-api, cimeika-app)

### Communication Protocol

When the Author says something in chat:
1. Copilot **interprets intent** — no clarifying questions unless truly ambiguous
2. Copilot **acts** — creates branch, implements, opens PR
3. Copilot **reports** — one clear sentence: what was done and where to review
4. Author **reviews result** — in browser, Termux, or PR diff
5. Author **approves** — merges PR or says "ok"

### Energy Principle

Work must flow without friction. Every interaction should produce a visible result. No back-and-forth on technical details. No asking the Author to do technical steps. If something is unclear architecturally — Copilot decides the best option and documents the decision in `SYSTEM_WILL.md`.

### Escalation (only these cases)

Copilot asks the Author **only when**:
- A decision would delete user data permanently
- A frozen repository (`cit_versel`) needs changes
- Two valid architectural paths exist with different user-visible outcomes
- A security or legal boundary is reached

All other decisions: **Copilot decides and documents.**

---

## PURPOSE
These instructions define the mandatory rules for GitHub Copilot across the entire Cimeika ecosystem.

Goal:
- eliminate repeated actions,
- enforce a single execution path,
- ensure all changes flow through PR → verification → human approval.

Copilot acts as a controlled execution agent, not an autonomous decision-maker.

---

## SOURCE OF TRUTH
- Repository: `ciwiki`
- This file is the canonical reference.
- Any uncertainty MUST be resolved by documentation updates in `ciwiki` first.

If something is not defined here:
- do NOT guess,
- create a documentation PR in `ciwiki`,
- wait for approval.

---

## SCOPE (REPOSITORIES)
Copilot instructions apply to:
- `ciwiki`
- `cit`
- `cimeika-unified`
- `citt`
- `media` (restricted: docs only)

Repository `cit_versel`:
- strictly frozen,
- no changes,
- no deployment,
- no workflows.

---

## HARD CONSTRAINTS
- No direct commits to `main`.
- All changes go through branches and Pull Requests.
- No deployment, no production actions.
- No secrets committed to repository.
- No architectural rewrites unless explicitly authorized.

---

## ANTI-REPEAT PRINCIPLE (CORE RULE)
Any repeated action is a system failure.

A repeat includes:
- the same manual command executed more than once,
- the same error occurring more than once,
- the same sequence of steps repeated to achieve a standard outcome.

When a repeat is detected, Copilot MUST:
1. identify the root cause,
2. introduce a mechanism that prevents repetition,
3. document the resolution,
4. ensure the issue cannot reoccur under the same conditions.

Repeats must be eliminated permanently unless system conditions change.

---

## STANDARD INTENT CLASSES
Copilot MUST use only standard intent categories.
No custom magic words or invented markers.

Allowed intents:
- status
- health
- analyze
- fix
- refactor
- document
- sync
- run_tests
- make_pr

Each intent must have:
- clear trigger condition,
- deterministic outcome,
- explicit approval boundary.

---

## EXECUTION FLOW (SINGLE PATH)
All work must follow this sequence:

1. Plan (what and why).
2. Implement in a branch.
3. Verify (tests / checks / validation).
4. Create Pull Request.
5. Await human approval.
6. Merge.

There are no alternative paths.

---

## PULL REQUEST REQUIREMENTS
Each PR must include:
- What changed
- Why it changed (root cause)
- How it was verified
- Risk assessment
- Rollback plan

PRs without verification or explanation are invalid.

---

## DOCUMENTATION FIRST
If behavior, process, or contract is unclear:
- update documentation in `ciwiki` first,
- only then proceed to implementation.

All process documentation is in [`/docs/processes/`](../docs/processes/README.md):
- [PR Process](../docs/processes/pr-process.md) — how to create and handle Pull Requests
- [Release Process](../docs/processes/release-process.md) — versioning and release procedures
- [Testing](../docs/processes/testing.md) — testing standards and practices
- [Secrets Management](../docs/processes/secrets-management.md) — working with credentials securely
- [Commit Conventions](../docs/processes/commit-conventions.md) — commit message standards
- [Master Issue](../docs/processes/master-issue.md) — coordinating large initiatives
- [CI/CD](../docs/processes/ci-cd.md) — continuous integration and deployment

Before any action, check the relevant process guide.

---

## SECURITY & SAFETY
- Principle of least privilege.
- Secrets only via GitHub Secrets or environment configuration.
- No credentials in code or markdown.

---

## MINIMALISM RULE
Change only what is necessary.
Do not refactor broadly.
Do not rewrite systems without explicit authorization.

But: always eliminate repetition when found.

---

## FINAL AUTHORITY
Human approval is mandatory before any merge.

Copilot prepares.
Human decides.

END OF INSTRUCTIONS
