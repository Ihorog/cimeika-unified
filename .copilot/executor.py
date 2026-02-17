#!/usr/bin/env python3
"""
Manifest Executor
Executes task steps sequentially with error handling and logging
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime

class TaskExecutor:
    def __init__(self, manifest_path: str):
        with open(manifest_path) as f:
            self.manifest = json.load(f)
        self.results = []
    
    def execute_step(self, step: dict) -> bool:
        """Execute a single step"""
        step_id = step['id']
        step_name = step.get('name', step_id)
        script = step['script']
        
        print(f"\n▶ [{step_id}] {step_name}")
        print(f"  Script: {script}")
        
        try:
            result = subprocess.run(
                script,
                shell=True,
                capture_output=True,
                text=True,
                timeout=step.get('timeout', 300)
            )
            
            if result.returncode == 0:
                print(f"✅ [{step_id}] SUCCESS")
                if result.stdout:
                    print(f"   Output: {result.stdout[:200]}")
                self.results.append({
                    'step': step_id,
                    'status': 'success',
                    'output': result.stdout
                })
                return True
            else:
                print(f"❌ [{step_id}] FAILED (exit code {result.returncode})")
                print(f"   Error: {result.stderr}")
                self.results.append({
                    'step': step_id,
                    'status': 'failed',
                    'error': result.stderr
                })
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  [{step_id}] TIMEOUT")
            self.results.append({
                'step': step_id,
                'status': 'timeout'
            })
            return False
        except Exception as e:
            print(f"❌ [{step_id}] ERROR: {e}")
            self.results.append({
                'step': step_id,
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def execute(self) -> int:
        """Execute all steps"""
        steps = self.manifest['spec']['steps']
        
        print(f"🤖 Executing task: {self.manifest['metadata']['name']}")
        print(f"   Total steps: {len(steps)}")
        print(f"   Type: {self.manifest['spec']['type']}")
        print("=" * 60)
        
        for i, step in enumerate(steps, 1):
            print(f"\n[{i}/{len(steps)}] Executing step...")
            success = self.execute_step(step)
            
            if not success:
                print(f"\n❌ Task FAILED at step {i}/{len(steps)}")
                return 1
        
        print("\n" + "=" * 60)
        print(f"✅ Task COMPLETED successfully")
        print(f"   Steps executed: {len(self.results)}/{len(steps)}")
        return 0

def main():
    parser = argparse.ArgumentParser(description='Execute CIMEIKA task manifest')
    parser.add_argument('--manifest', required=True, help='Path to manifest JSON')
    
    args = parser.parse_args()
    
    executor = TaskExecutor(args.manifest)
    exit_code = executor.execute()
    
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
