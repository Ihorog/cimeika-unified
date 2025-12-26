"""
Rule Engine for CI Failure Detection
Recognizes common CI failures and provides actionable guidance
"""
import re
from typing import Dict, List, Any, Optional


class CIFailurePattern:
    """Represents a CI failure pattern with detection logic and remediation"""
    
    def __init__(
        self,
        name: str,
        patterns: List[str],
        message: str,
        actions: List[Dict[str, str]],
        severity: str = "error"
    ):
        self.name = name
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.message = message
        self.actions = actions
        self.severity = severity
    
    def matches(self, text: str) -> bool:
        """Check if any pattern matches the text"""
        return any(pattern.search(text) for pattern in self.patterns)


# Define common CI failure patterns
CI_PATTERNS = [
    CIFailurePattern(
        name="node_version_mismatch",
        patterns=[
            r"error.*?node.*?version",
            r"expected node.*?but got",
            r"required node.*?version",
            r"unsupported engine.*?node"
        ],
        message="Node.js version mismatch detected. Check your .nvmrc or package.json engines field.",
        actions=[
            {
                "type": "check",
                "title": "Verify Node.js version",
                "details": "Check .nvmrc file or package.json engines.node field matches CI environment"
            },
            {
                "type": "suggest",
                "title": "Update CI workflow",
                "details": "Update .github/workflows to use correct Node.js version via actions/setup-node"
            }
        ],
        severity="error"
    ),
    
    CIFailurePattern(
        name="npm_lockfile_mismatch",
        patterns=[
            r"npm.*?lockfile.*?version",
            r"package-lock\.json.*?conflict",
            r"npm ci.*?failed",
            r"lockfile.*?out of date",
            r"package-lock\.json is outdated"
        ],
        message="npm lockfile is out of sync. Run 'npm install' locally and commit the updated package-lock.json.",
        actions=[
            {
                "type": "patch",
                "title": "Regenerate package-lock.json",
                "details": "Run: rm -rf node_modules package-lock.json && npm install"
            },
            {
                "type": "check",
                "title": "Verify npm version",
                "details": "Ensure CI and local npm versions match"
            }
        ],
        severity="error"
    ),
    
    CIFailurePattern(
        name="python_deps_install_failed",
        patterns=[
            r"error.*?installing.*?requirements",
            r"pip install.*?failed",
            r"could not find.*?version.*?pypi",
            r"no matching distribution found"
        ],
        message="Python dependency installation failed. Check requirements.txt for invalid versions or unavailable packages.",
        actions=[
            {
                "type": "check",
                "title": "Verify requirements.txt",
                "details": "Check for typos, version constraints, and package availability on PyPI"
            },
            {
                "type": "suggest",
                "title": "Pin exact versions",
                "details": "Use pip freeze to generate exact versions if using loose constraints"
            }
        ],
        severity="error"
    ),
    
    CIFailurePattern(
        name="ruff_linting_errors",
        patterns=[
            r"ruff.*?found.*?error",
            r"ruff check.*?failed",
            r"ruff.*?\d+\s+error"
        ],
        message="Ruff linting errors detected. Run 'ruff check --fix .' locally to auto-fix most issues.",
        actions=[
            {
                "type": "patch",
                "title": "Auto-fix with Ruff",
                "details": "Run: ruff check --fix ."
            },
            {
                "type": "check",
                "title": "Review remaining errors",
                "details": "Run: ruff check . to see unfixable errors"
            }
        ],
        severity="warn"
    ),
    
    CIFailurePattern(
        name="flake8_errors",
        patterns=[
            r"flake8.*?error",
            r"flake8.*?failed"
        ],
        message="Flake8 linting errors found. Run 'flake8' locally and fix reported issues.",
        actions=[
            {
                "type": "check",
                "title": "Run flake8 locally",
                "details": "Run: flake8 . to see all errors"
            },
            {
                "type": "suggest",
                "title": "Consider using Ruff",
                "details": "Ruff is a faster alternative to flake8 with auto-fix capabilities"
            }
        ],
        severity="warn"
    ),
    
    CIFailurePattern(
        name="pytest_import_errors",
        patterns=[
            r"import.*?error.*?pytest",
            r"modulenotfounderror",
            r"no module named",
            r"pytest.*?collection.*?error"
        ],
        message="Python import errors during test collection. Check missing dependencies or PYTHONPATH issues.",
        actions=[
            {
                "type": "check",
                "title": "Verify all dependencies installed",
                "details": "Ensure all packages in requirements.txt are installed: pip install -r requirements.txt"
            },
            {
                "type": "check",
                "title": "Check PYTHONPATH",
                "details": "Verify test files can import application modules correctly"
            }
        ],
        severity="error"
    ),
    
    CIFailurePattern(
        name="cancelled_run",
        patterns=[
            r"workflow.*?cancelled",
            r"run.*?cancelled",
            r"cancelled by"
        ],
        message="Workflow run was cancelled. This is typically a manual action or superseded by newer run.",
        actions=[
            {
                "type": "check",
                "title": "Check cancellation reason",
                "details": "Review GitHub Actions UI for cancellation details"
            },
            {
                "type": "suggest",
                "title": "Re-run if needed",
                "details": "Manually trigger a new run if this was cancelled in error"
            }
        ],
        severity="info"
    ),
    
    CIFailurePattern(
        name="test_failures",
        patterns=[
            r"\d+\s+failed.*?test",
            r"test.*?failed",
            r"assertion.*?error",
            r"pytest.*?\d+\s+failed"
        ],
        message="Test failures detected. Review test output for specific assertion errors.",
        actions=[
            {
                "type": "check",
                "title": "Run tests locally",
                "details": "Run the same test suite locally to reproduce failures"
            },
            {
                "type": "check",
                "title": "Review test logs",
                "details": "Check CI logs for detailed assertion errors and stack traces"
            }
        ],
        severity="error"
    ),
    
    CIFailurePattern(
        name="build_timeout",
        patterns=[
            r"timeout.*?exceeded",
            r"build.*?timeout",
            r"execution.*?timeout"
        ],
        message="Build or test execution timed out. Optimize slow tests or increase timeout limits.",
        actions=[
            {
                "type": "check",
                "title": "Identify slow tests",
                "details": "Run tests with timing info: pytest --durations=10"
            },
            {
                "type": "suggest",
                "title": "Increase timeout",
                "details": "Update workflow timeout-minutes if jobs legitimately need more time"
            }
        ],
        severity="warn"
    ),
    
    CIFailurePattern(
        name="docker_build_failed",
        patterns=[
            r"docker.*?build.*?failed",
            r"error.*?building.*?image",
            r"dockerfile.*?error"
        ],
        message="Docker image build failed. Check Dockerfile syntax and base image availability.",
        actions=[
            {
                "type": "check",
                "title": "Test Docker build locally",
                "details": "Run: docker build -t test-image ."
            },
            {
                "type": "check",
                "title": "Verify base image",
                "details": "Ensure base image in FROM statement is accessible"
            }
        ],
        severity="error"
    ),
]


class RuleEngine:
    """Rule engine for analyzing CI failures and providing guidance"""
    
    def __init__(self):
        self.patterns = CI_PATTERNS
    
    def analyze(
        self,
        text: str,
        mode: str = "analysis",
        artifacts: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze text for CI failure patterns
        
        Args:
            text: Input text to analyze (logs, error messages, etc.)
            mode: Operation mode (analysis, autofix, logger)
            artifacts: Optional list of artifacts with base64 content
            
        Returns:
            dict: Analysis result with message, severity, and actions
        """
        # Find matching patterns
        matches = [pattern for pattern in self.patterns if pattern.matches(text)]
        
        if not matches:
            return {
                "message": "No recognized CI failure patterns detected. Please review logs manually.",
                "severity": "info",
                "outputs": {
                    "patch_unified_diff": None,
                    "actions": [
                        {
                            "type": "check",
                            "title": "Review full logs",
                            "details": "Check complete CI output for error details"
                        }
                    ]
                }
            }
        
        # Use the first match (most specific)
        match = matches[0]
        
        # For autofix mode, attempt to generate patch
        patch = None
        if mode == "autofix":
            patch = self._generate_patch(match, text, artifacts)
        
        return {
            "message": match.message,
            "severity": match.severity,
            "outputs": {
                "patch_unified_diff": patch,
                "actions": match.actions
            }
        }
    
    def _generate_patch(
        self,
        pattern: CIFailurePattern,
        text: str,
        artifacts: Optional[List[Dict[str, Any]]]
    ) -> Optional[str]:
        """
        Generate a unified diff patch for autofix mode
        
        Args:
            pattern: Matched failure pattern
            text: Input text
            artifacts: Optional artifacts
            
        Returns:
            str | None: Unified diff or None if can't generate
        """
        # For MVP, return None and request artifacts
        # In future, implement specific fixes based on pattern type
        
        if not artifacts:
            # Can't generate patch without relevant files
            return None
        
        # Pattern-specific patch generation would go here
        # For now, just return None (actions will guide user)
        return None
    
    def get_pattern_names(self) -> List[str]:
        """Get list of recognized pattern names"""
        return [p.name for p in self.patterns]
