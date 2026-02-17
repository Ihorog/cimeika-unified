# Copilot Task Manifests

This directory contains auto-generated task manifests created by the Copilot Task Execution system.

## Structure

- **`auto-{task-id}.yml`** — Auto-generated manifests from `@copilot task:` comments
- Each manifest represents a requested task with its execution plan

## Manifest Lifecycle

1. User comments: `@copilot task: Deploy to production`
2. Workflow generates: `manifests/auto-abc12345.yml`
3. Workflow creates PR with manifest preview
4. Human reviews and approves
5. Workflow executes steps from manifest
6. Manifest remains in repo for audit trail

## Manual Review

Before approving any task, always review the generated manifest to ensure:
- Task type is correct
- Steps are appropriate
- Timeouts are reasonable
- Required approvals are in place
- No sensitive data in the manifest

## Cleanup

Old manifests can be archived or deleted periodically, but keep recent ones for audit purposes.
Consider keeping manifests for at least 90 days for compliance and debugging.
