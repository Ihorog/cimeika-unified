# Copilot Integration Tests

This directory contains test scripts for validating the Copilot task execution integration.

## Test Scripts

### Test 1: Manifest Generation

Tests all three task types to ensure correct manifest generation.

```bash
# Test health-check detection
python3 .copilot/generate.py \
  --task "Check system health and status" \
  --id "test-health" \
  --output "/tmp/health-manifest.yml"

# Expected: type=health-check, require_approval=false, 1 step

# Test deployment detection
python3 .copilot/generate.py \
  --task "Deploy frontend to production" \
  --id "test-deploy" \
  --output "/tmp/deploy-manifest.yml"

# Expected: type=deployment, require_approval=true, require_backup=true, 3 steps

# Test rollback detection
python3 .copilot/generate.py \
  --task "Rollback to previous version" \
  --id "test-rollback" \
  --output "/tmp/rollback-manifest.yml"

# Expected: type=rollback, require_approval=true, 2 steps
```

### Test 2: Executor Success Path

Tests successful execution of all steps.

```bash
# Create test manifest
cat > /tmp/test-success.json << 'EOF'
{
  "metadata": {"name": "test-success"},
  "spec": {
    "type": "test",
    "steps": [
      {"id": "step1", "name": "Echo 1", "script": "echo 'Step 1'"},
      {"id": "step2", "name": "Echo 2", "script": "echo 'Step 2'"}
    ]
  }
}
EOF

# Execute
python3 .copilot/executor.py --manifest /tmp/test-success.json

# Expected: Exit code 0, both steps succeed
```

### Test 3: Executor Failure Handling

Tests that execution stops at first failure.

```bash
# Create test manifest with failure
cat > /tmp/test-failure.json << 'EOF'
{
  "metadata": {"name": "test-failure"},
  "spec": {
    "type": "test",
    "steps": [
      {"id": "step1", "name": "Success", "script": "echo 'OK'"},
      {"id": "step2", "name": "Failure", "script": "exit 1"},
      {"id": "step3", "name": "Should not run", "script": "echo 'BAD'"}
    ]
  }
}
EOF

# Execute
python3 .copilot/executor.py --manifest /tmp/test-failure.json

# Expected: Exit code 1, step1 succeeds, step2 fails, step3 not executed
```

### Test 4: Workflow YAML Validation

Validates workflow syntax.

```bash
# Validate all workflows
for workflow in .github/workflows/copilot-*.yml; do
  echo "Validating $workflow..."
  python3 -c "import yaml; yaml.safe_load(open('$workflow'))"
  echo "✅ Valid"
done
```

## Integration Testing

### Manual Integration Test

1. **Create test issue** in GitHub
2. **Comment**: `@copilot task: Check system health`
3. **Verify**: 
   - Workflow runs (copilot-task-detect)
   - Manifest generated in new branch
   - PR created with manifest preview
   - Reply comment posted
4. **Review PR** and manifest
5. **Comment on PR**: `@copilot approve`
6. **Verify**:
   - Workflow runs (copilot-approve)
   - Label added to PR
   - Execution workflow triggered (copilot-execute)
   - Results posted to PR
   - Logs uploaded as artifacts

### Expected Workflow Behavior

**copilot-task-detect.yml:**
- Triggers on: issue_comment.created, pull_request_review_comment.created
- Condition: Comment contains "@copilot task:"
- Actions:
  1. Extract task description with regex
  2. Generate 8-char hash as task ID
  3. Run generate.py to create manifest
  4. Create branch copilot/{task-id}
  5. Commit manifest to manifests/auto-{task-id}.yml
  6. Open PR with manifest preview
  7. Reply to original comment

**copilot-approve.yml:**
- Triggers on: issue_comment.created (on PRs only)
- Condition: Comment contains "@copilot approve"
- Actions:
  1. Get PR details
  2. Extract manifest path from PR body
  3. Add "copilot-approved" label
  4. Trigger copilot-execute.yml via workflow_dispatch
  5. Reply to comment

**copilot-execute.yml:**
- Triggers on: workflow_dispatch
- Inputs: manifest (path), pr (number)
- Actions:
  1. Convert YAML manifest to JSON
  2. Execute executor.py with manifest
  3. Capture exit code
  4. Upload execution.log as artifact
  5. Post success/failure report to PR
  6. Fail workflow if execution failed

## Automated Test Suite

Future enhancement: Create automated test suite using pytest.

```python
# tests/test_copilot_integration.py
def test_detect_health_check():
    """Test health-check task type detection"""
    assert detect_task_type("Check system health") == "health-check"

def test_detect_deployment():
    """Test deployment task type detection"""
    assert detect_task_type("Deploy to production") == "deployment"

def test_detect_rollback():
    """Test rollback task type detection"""
    assert detect_task_type("Rollback deployment") == "rollback"

def test_executor_success():
    """Test executor with successful steps"""
    # Create test manifest, run executor, verify exit code 0

def test_executor_failure():
    """Test executor failure handling"""
    # Create manifest with failing step, verify execution stops
```

## CI/CD Integration

The Copilot workflows are designed to:
- Run alongside existing CI/CD (ci.yml, vercel-deploy.yml, etc.)
- Not interfere with existing workflows
- Use the same secrets and infrastructure
- Follow the same code quality standards

## Security Considerations

All tests should verify:
- No secrets in manifests
- Proper use of GitHub Secrets for sensitive data
- Workflow permissions are minimal and necessary
- Execution isolation in GitHub Actions runners
- Audit trail maintained (logs, artifacts, PR comments)

## Next Steps

1. Run all tests locally before first production use
2. Test with real GitHub issue/PR in staging environment
3. Monitor first executions closely
4. Create automated test suite
5. Set up monitoring for workflow failures
6. Document any edge cases discovered

---

**Last Updated:** 2026-02-17  
**Status:** Ready for testing
