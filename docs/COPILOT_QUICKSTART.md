# Copilot Task Execution - Quick Start Guide

## Overview

The Copilot Task Execution system allows you to trigger automated workflows directly from GitHub comments. Request tasks, review generated manifests, approve execution, and monitor results—all without leaving GitHub.

## Quick Start

### 1. Request a Task

Comment on any issue or PR with:

```
@copilot task: [your task description]
```

**Examples:**

```
@copilot task: Check system health
@copilot task: Deploy frontend to production
@copilot task: Rollback to previous version
```

### 2. Review the Manifest

Copilot will:
- Generate a task manifest
- Create a feature branch
- Open a PR with manifest preview
- Reply to your comment with the PR link

Review the manifest in the PR to ensure it matches your intent.

### 3. Approve Execution

If the manifest looks good, approve it by commenting:

```
@copilot approve
```

### 4. Monitor Execution

- Execution starts automatically
- View real-time progress in the Actions tab
- Results are posted to the PR
- Execution logs are saved as artifacts

## Available Task Types

### Health Check

**Keywords:** `health`, `check`, `status`

**What it does:**
- Runs system health checks
- Verifies services are running
- Reports status

**Requires approval:** No

**Example:**
```
@copilot task: Check system health
```

### Deployment

**Keywords:** `deploy`, `deployment`, `release`

**What it does:**
- Creates backup before deployment
- Deploys to Vercel production
- Verifies deployment health

**Requires approval:** Yes

**Example:**
```
@copilot task: Deploy to production
```

### Rollback

**Keywords:** `rollback`, `revert`

**What it does:**
- Rolls back to previous Vercel deployment
- Verifies rollback succeeded

**Requires approval:** Yes

**Example:**
```
@copilot task: Rollback deployment
```

## Commands Reference

| Command | Where | Effect |
|---------|-------|--------|
| `@copilot task: <description>` | Issue/PR comment | Generate manifest and create PR |
| `@copilot approve` | PR comment | Approve and execute task |

## Workflow Architecture

```
┌─────────────────────────────────────────────────────┐
│ 1. User Comments: @copilot task: Deploy to prod    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 2. copilot-task-detect.yml                         │
│    - Extract task description                       │
│    - Generate unique task ID                        │
│    - Run generate.py to create manifest             │
│    - Create feature branch                          │
│    - Commit manifest                                │
│    - Open PR with preview                           │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 3. Human Review                                     │
│    - Review manifest in PR                          │
│    - Verify task type and steps                     │
│    - Check constraints and timeouts                 │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 4. User Comments: @copilot approve                  │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 5. copilot-approve.yml                              │
│    - Extract manifest path from PR                  │
│    - Add "copilot-approved" label                   │
│    - Trigger copilot-execute.yml                    │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│ 6. copilot-execute.yml                              │
│    - Convert YAML manifest to JSON                  │
│    - Execute each step sequentially                 │
│    - Capture stdout/stderr                          │
│    - On failure: halt and report                    │
│    - On success: post completion report             │
│    - Upload execution logs as artifacts             │
└─────────────────────────────────────────────────────┘
```

## Task Manifest Structure

Every task has a manifest with this structure:

```yaml
kind: Task
apiVersion: cimeika.io/v1
metadata:
  name: task-abc12345
  namespace: cimeika
  created_at: '2026-02-17T12:00:00Z'
  labels:
    type: health-check
    source: copilot-comment
spec:
  title: Check system health
  description: Auto-generated task
  type: health-check
  constraints:
    timeout_seconds: 300
    require_approval: false
    require_backup: false
  inputs:
    environment:
      VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  steps:
  - id: check
    name: Run health check
    script: make health
status:
  phase: pending
  start_time: null
```

## Safety Features

### Approval Gates

- **Deployment tasks:** Always require human approval
- **Rollback tasks:** Always require human approval
- **Health checks:** No approval needed (safe)

### Timeouts

Each step has a timeout (default 300 seconds):
- Prevents infinite loops
- Ensures workflow doesn't hang
- Configurable per task type

### Backup Requirements

Deployment tasks include automatic backup:
- Backup runs before deployment
- Ensures rollback capability
- Verifies backup succeeded before proceeding

### Atomic Execution

- Steps execute sequentially
- Failure at any step halts execution
- No partial deployments
- Clear error reporting

### Audit Trail

Every execution is logged:
- Full stdout/stderr captured
- Logs uploaded as artifacts (30-day retention)
- Results posted to PR
- Timestamped execution records

## Troubleshooting

### Task not detected

**Problem:** Commented `@copilot task: ...` but nothing happened

**Solutions:**
- Ensure exact format: `@copilot task:` (with colon)
- Check Actions tab for workflow run
- Verify you have write permissions on the repo

### Manifest generation failed

**Problem:** Workflow failed during manifest generation

**Solutions:**
- Check workflow logs in Actions tab
- Ensure `.copilot/generate.py` exists
- Verify PyYAML is installed in the workflow

### Approval not working

**Problem:** Commented `@copilot approve` but execution didn't start

**Solutions:**
- Must comment on the PR (not the original issue)
- Ensure PR was created by the task detection workflow
- Check that manifest path is in PR body
- Verify you have write permissions

### Execution failed

**Problem:** Task execution failed with errors

**Solutions:**
- Download execution logs from artifacts
- Check error messages in PR comment
- Verify required secrets are set (VERCEL_TOKEN, etc.)
- Ensure commands in manifest are valid
- Check timeout constraints

### Missing secrets

**Problem:** Execution failed due to missing environment variables

**Solutions:**
- Add required secrets in repository settings
- Verify secret names match manifest inputs
- Required secrets: `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID`

## Advanced Usage

### Custom Task Types

Want to add a new task type?

1. Edit `.copilot/generate.py`
2. Add new template to `TEMPLATES` dict
3. Add detection keywords to `detect_task_type()`
4. Define steps, constraints, and requirements
5. Test with a sample task

### Viewing Execution Logs

Full logs are always available:

1. Go to Actions tab
2. Find "Copilot Execute" workflow run
3. Download "execution-logs-{PR}" artifact
4. Unzip and view `execution.log`

### Modifying Step Timeouts

Edit manifest before approval:

1. Review manifest in PR
2. Adjust `timeout_seconds` value
3. Commit changes to the feature branch
4. Approve with `@copilot approve`

## Best Practices

### ✅ Do

- Always review the manifest before approving
- Use descriptive task descriptions
- Monitor execution in Actions tab
- Download logs for failed executions
- Test new task types with health checks first

### ❌ Don't

- Approve tasks without reviewing the manifest
- Use production deployments for testing
- Skip verification steps
- Ignore timeout warnings
- Rush through approval process

## Security Considerations

### Secrets Management

- Never commit secrets to manifests
- Use GitHub Secrets for sensitive data
- Secrets are automatically injected at runtime
- Logs never expose secret values

### Approval Requirements

- Destructive operations require human approval
- Read-only operations can run without approval
- Approval gate prevents accidental execution
- Only authorized users can approve

### Execution Isolation

- Tasks run in isolated GitHub Actions runners
- No persistent state between runs
- Fresh environment for each execution
- Automatic cleanup after completion

## Examples

### Example 1: Simple Health Check

**Request:**
```
@copilot task: Check if backend is healthy
```

**Generated Manifest:**
```yaml
spec:
  type: health-check
  steps:
  - id: check
    name: Run health check
    script: make health
```

**Approval:**
```
@copilot approve
```

### Example 2: Production Deployment

**Request:**
```
@copilot task: Deploy latest changes to production
```

**Generated Manifest:**
```yaml
spec:
  type: deployment
  constraints:
    require_approval: true
    require_backup: true
  steps:
  - id: backup
    name: Create backup
    script: make backup
  - id: deploy
    name: Deploy to Vercel
    script: vercel deploy --prod
  - id: verify
    name: Verify deployment
    script: curl -f https://cimeika.com.ua/api/health
```

**Approval:**
```
@copilot approve
```

### Example 3: Emergency Rollback

**Request:**
```
@copilot task: Rollback to previous version immediately
```

**Generated Manifest:**
```yaml
spec:
  type: rollback
  constraints:
    require_approval: true
  steps:
  - id: rollback
    name: Rollback deployment
    script: vercel rollback
  - id: verify
    name: Verify rollback
    script: curl -f https://cimeika.com.ua/api/health
```

**Approval:**
```
@copilot approve
```

## Getting Help

### Documentation

- **Architecture:** See `SYSTEM_WILL.md` for integration details
- **Workflows:** Check `.github/workflows/copilot-*.yml`
- **Scripts:** Review `.copilot/generate.py` and `.copilot/executor.py`

### Support

- **Issues:** Open a GitHub issue with `copilot` label
- **Logs:** Always attach execution logs when reporting issues
- **Questions:** Tag maintainers in your issue

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-17  
**Maintained By:** Cimeika Core Team

*Copilot prepares. Human decides.*
