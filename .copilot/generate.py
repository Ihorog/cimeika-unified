#!/usr/bin/env python3
"""
Manifest Generator
Detects task type from description and generates executable YAML manifest
"""

import argparse
import yaml
from datetime import datetime, timezone
import hashlib

TEMPLATES = {
    'deployment': {
        'constraints': {
            'timeout_seconds': 600,
            'require_approval': True,
            'require_backup': True
        },
        'steps': [
            {'id': 'backup', 'name': 'Create backup', 'script': 'make backup'},
            {'id': 'deploy', 'name': 'Deploy to Vercel', 'script': 'vercel deploy --prod --token=$VERCEL_TOKEN'},
            {'id': 'verify', 'name': 'Verify deployment', 'script': 'curl -f https://cimeika.com.ua/api/health'}
        ]
    },
    'health-check': {
        'constraints': {
            'timeout_seconds': 300,
            'require_approval': False,
            'require_backup': False
        },
        'steps': [
            {'id': 'check', 'name': 'Run health check', 'script': 'make health'}
        ]
    },
    'rollback': {
        'constraints': {
            'timeout_seconds': 300,
            'require_approval': True,
            'require_backup': False
        },
        'steps': [
            {'id': 'rollback', 'name': 'Rollback deployment', 'script': 'vercel rollback --token=$VERCEL_TOKEN'},
            {'id': 'verify', 'name': 'Verify rollback', 'script': 'curl -f https://cimeika.com.ua/api/health'}
        ]
    }
}

def detect_task_type(task: str) -> str:
    """Detect task type from description"""
    task_lower = task.lower()
    
    # Check rollback first (more specific)
    if any(kw in task_lower for kw in ['rollback', 'revert']):
        return 'rollback'
    elif any(kw in task_lower for kw in ['deploy', 'deployment', 'release']):
        return 'deployment'
    elif any(kw in task_lower for kw in ['health', 'check', 'status']):
        return 'health-check'
    else:
        # Default to health-check for safety
        return 'health-check'

def generate_manifest(task: str, task_id: str, output: str):
    """Generate manifest YAML from task description"""
    
    task_type = detect_task_type(task)
    template = TEMPLATES[task_type]
    
    manifest = {
        'kind': 'Task',
        'apiVersion': 'cimeika.io/v1',
        'metadata': {
            'name': f'task-{task_id}',
            'namespace': 'cimeika',
            'created_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            'labels': {
                'type': task_type,
                'source': 'copilot-comment'
            }
        },
        'spec': {
            'title': task,
            'description': f'Auto-generated task: {task}',
            'type': task_type,
            'constraints': template['constraints'],
            'inputs': {
                'environment': {
                    'VERCEL_TOKEN': '${{ secrets.VERCEL_TOKEN }}',
                    'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}'
                }
            },
            'steps': template['steps']
        },
        'status': {
            'phase': 'pending',
            'start_time': None
        }
    }
    
    with open(output, 'w') as f:
        yaml.dump(manifest, f, default_flow_style=False, sort_keys=False)
    
    print(f"✅ Manifest generated: {output}")
    print(f"   Task type: {task_type}")
    print(f"   Steps: {len(template['steps'])}")

def main():
    parser = argparse.ArgumentParser(description='Generate CIMEIKA task manifest')
    parser.add_argument('--task', required=True, help='Task description')
    parser.add_argument('--id', required=True, help='Task ID')
    parser.add_argument('--output', required=True, help='Output manifest path')
    
    args = parser.parse_args()
    
    generate_manifest(args.task, args.id, args.output)

if __name__ == '__main__':
    main()
