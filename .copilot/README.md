# Copilot Task Execution Scripts

This directory contains Python scripts that power the Copilot task execution integration.

## Scripts

### generate.py

**Purpose:** Generates task manifests from natural language descriptions.

**Usage:**
```bash
python3 generate.py --task "Deploy to production" --id "abc12345" --output "manifests/auto-abc12345.yml"
```

**Features:**
- Detects task type from description (deployment, health-check, rollback)
- Uses predefined templates for each task type
- Generates YAML manifest with constraints and steps
- Safe defaults (health-check if uncertain)

**Task Types:**
- `deployment` - Deploy to Vercel with backup and verification
- `health-check` - Run health checks (no approval needed)
- `rollback` - Rollback deployment with verification

### executor.py

**Purpose:** Executes task steps sequentially with error handling.

**Usage:**
```bash
python3 executor.py --manifest manifest.json
```

**Features:**
- Loads manifest JSON (converted from YAML by workflow)
- Executes each step sequentially
- Captures stdout/stderr for each step
- Halts on first failure (atomic execution)
- Returns detailed execution results
- Exit code 0 = success, 1 = failure

**Safety:**
- Timeout protection per step
- Clear error messages
- Execution logs for debugging

## Dependencies

- Python 3.11+
- PyYAML (for manifest generation)

## Testing

See `TESTING.md` for comprehensive test cases and validation procedures.

## Integration with Workflows

These scripts are called by GitHub Actions workflows:

1. **copilot-task-detect.yml** calls `generate.py`
   - Parses user comment
   - Generates manifest
   - Creates PR with preview

2. **copilot-execute.yml** calls `executor.py`
   - Converts YAML to JSON
   - Executes steps
   - Reports results

## Adding New Task Types

To add a new task type:

1. Edit `generate.py`
2. Add template to `TEMPLATES` dict
3. Add detection keywords to `detect_task_type()`
4. Test with sample task

Example:
```python
TEMPLATES = {
    # ... existing templates ...
    'new-type': {
        'constraints': {
            'timeout_seconds': 300,
            'require_approval': False,
            'require_backup': False
        },
        'steps': [
            {'id': 'step1', 'name': 'Do something', 'script': 'echo "test"'}
        ]
    }
}

def detect_task_type(task: str) -> str:
    # ... existing checks ...
    elif any(kw in task_lower for kw in ['keyword1', 'keyword2']):
        return 'new-type'
```

## Security

- Never commit secrets to manifests
- Use `${{ secrets.NAME }}` for sensitive values
- Secrets are injected at runtime by GitHub Actions
- Logs never expose secret values

## Maintenance

Keep these scripts:
- Simple and focused
- Well-tested
- Well-documented
- Backward compatible

---

**Version:** 1.0.0  
**Last Updated:** 2026-02-17  
**Maintained By:** Cimeika Core Team
