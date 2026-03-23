"""
Self-Improvement Mechanism for Cimeika
Detects missing tools and generates GitHub Issue descriptions
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Default manifest structure constants
DEFAULT_MANIFEST_VERSION = "1.0.0"
DEFAULT_MANIFEST_KEYS = ["version", "tools", "required_tools", "optional_tools"]


class ToolManifest:
    """Manager for tool manifest and validation"""
    
    def __init__(self, manifest_path: Optional[str] = None):
        """Initialize with manifest path"""
        if manifest_path is None:
            # Default to manifest.json in the same directory
            self.manifest_path = Path(__file__).parent / "manifest.json"
        else:
            self.manifest_path = Path(manifest_path)
        
        self.manifest = self._load_manifest()
    
    def _load_manifest(self) -> Dict:
        """Load manifest from JSON file"""
        if not self.manifest_path.exists():
            logger.warning(
                f"Manifest file not found at {self.manifest_path}. "
                "Using empty default manifest. This may indicate a configuration issue."
            )
            return {
                "version": DEFAULT_MANIFEST_VERSION,
                "tools": [],
                "required_tools": [],
                "optional_tools": []
            }
        
        with open(self.manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_tool(self, tool_id: str) -> Optional[Dict]:
        """Get tool by ID from manifest"""
        for tool in self.manifest.get("tools", []):
            if tool.get("id") == tool_id:
                return tool
        return None
    
    def get_all_tools(self) -> List[Dict]:
        """Get all tools from manifest"""
        return self.manifest.get("tools", [])
    
    def get_required_tools(self) -> List[str]:
        """Get list of required tool IDs"""
        return self.manifest.get("required_tools", [])
    
    def get_optional_tools(self) -> List[str]:
        """Get list of optional tool IDs"""
        return self.manifest.get("optional_tools", [])
    
    def validate_tools(self) -> Dict[str, List[str]]:
        """
        Validate that all required tools are present
        Returns dict with 'missing' and 'inactive' lists
        """
        result = {
            "missing": [],
            "inactive": [],
            "all_present": True
        }
        
        tool_ids = {tool.get("id") for tool in self.manifest.get("tools", [])}
        required = set(self.get_required_tools())
        
        # Check for missing required tools
        missing = required - tool_ids
        if missing:
            result["missing"] = list(missing)
            result["all_present"] = False
        
        # Check for inactive required tools
        for tool in self.manifest.get("tools", []):
            if tool.get("id") in required and tool.get("status") != "active":
                result["inactive"].append(tool.get("id"))
                result["all_present"] = False
        
        return result


class GitHubIssueGenerator:
    """Generate GitHub Issue descriptions for missing tools"""
    
    @staticmethod
    def generate_issue_title(tool_id: str, reason: str = "missing") -> str:
        """Generate issue title for a missing tool"""
        tool_name = tool_id.replace("_", " ").title()
        if reason == "missing":
            return f"[Tool Missing] Add {tool_name} to Manifest"
        elif reason == "inactive":
            return f"[Tool Inactive] Reactivate {tool_name} Module"
        else:
            return f"[Tool Issue] {tool_name} - {reason}"
    
    @staticmethod
    def generate_issue_body(
        tool_id: str,
        reason: str = "missing",
        context: Optional[Dict] = None
    ) -> str:
        """
        Generate comprehensive GitHub Issue body for a missing/inactive tool
        
        Args:
            tool_id: The ID of the tool
            reason: Reason for the issue (missing, inactive, etc.)
            context: Additional context information
        
        Returns:
            Formatted markdown issue body
        """
        tool_name = tool_id.replace("_", " ").title()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Base issue template
        issue_body = f"""## 🔧 Tool Detection Alert

**Tool ID:** `{tool_id}`  
**Tool Name:** {tool_name}  
**Status:** {reason.upper()}  
**Detected:** {timestamp}  
**Auto-generated:** Yes (Self-Improvement Mechanism)

---

## 📋 Description

The self-improvement mechanism has detected that the tool **{tool_name}** (`{tool_id}`) is {reason} in the manifest.

"""
        
        # Add reason-specific information
        if reason == "missing":
            issue_body += """### Missing Tool
This tool is marked as required in `manifest.json` but is not present in the tools registry.

**Required Actions:**
1. Define tool specification in `backend/app/core/manifest.json`
2. Implement tool functionality if not yet available
3. Add API endpoints for the tool
4. Update documentation
5. Add tests for the new tool

"""
        
        elif reason == "inactive":
            issue_body += """### Inactive Tool
This tool exists in the manifest but is marked as inactive.

**Required Actions:**
1. Investigate why the tool was deactivated
2. Fix any issues preventing activation
3. Update tool status to "active" in manifest
4. Verify tool functionality
5. Update tests if needed

"""
        
        # Add context if provided
        if context:
            issue_body += "### Additional Context\n\n"
            for key, value in context.items():
                issue_body += f"- **{key}:** {value}\n"
            issue_body += "\n"
        
        # Add standard sections
        issue_body += """---

## 🎯 Acceptance Criteria

- [ ] Tool is registered in `backend/app/core/manifest.json`
- [ ] Tool status is set to "active"
- [ ] Required endpoints are implemented and functional
- [ ] Dependencies are properly declared
- [ ] Documentation is updated
- [ ] Tests are passing
- [ ] Tool is integrated with Ci Core orchestrator

---

## 📚 Resources

- **Manifest Location:** `backend/app/core/manifest.json`
- **Self-Improvement Module:** `backend/app/core/self_improvement.py`
- **Documentation:** `SYSTEM_WILL.md`
- **Architecture:** `docs/ARCHITECTURE.md`

---

## 🏷️ Labels

`tool-missing`, `self-improvement`, `automation`, `enhancement`

---

## 💡 Implementation Guidance

### Step 1: Define Tool in Manifest

Add tool definition to `backend/app/core/manifest.json`:

```json
{
  "id": "your_tool_id",
  "name": "Your Tool Name",
  "description": "What this tool does",
  "status": "active",
  "category": "module|service|integration",
  "endpoints": ["/api/v1/your-tool/endpoint"],
  "dependencies": ["ci_core"]
}
```

### Step 2: Implement Tool

Create module in `backend/app/modules/your_tool/`:
- `__init__.py`
- `routes.py` - API endpoints
- `service.py` - Business logic
- `models.py` - Data models

### Step 3: Register with Main App

Update `backend/main.py` or module router to include new tool endpoints.

### Step 4: Documentation

Update:
- README.md - Add tool to list of modules
- docs/ARCHITECTURE.md - Explain tool's role
- SYSTEM_WILL.md - Add guidance for AI agents

### Step 5: Testing

Create tests in `backend/tests/test_your_tool.py`

---

## 🤖 For AI Agents

This issue was auto-generated by the self-improvement mechanism. When implementing:

1. Follow the ANTI-REPEAT PRINCIPLE from global instructions
2. Make minimal, surgical changes
3. Ensure all changes go through PR workflow
4. Document your decisions in SYSTEM_WILL.md
5. Update manifest.json when tool is ready

**Related Files:**
- `backend/app/core/manifest.json` - Tool registry
- `backend/app/core/self_improvement.py` - This generator
- `SYSTEM_WILL.md` - AI agent documentation

---

**Generated by Cimeika Self-Improvement Mechanism v1.0**
"""
        
        return issue_body
    
    @staticmethod
    def generate_batch_issue(
        missing_tools: List[str],
        inactive_tools: List[str]
    ) -> str:
        """Generate a single issue for multiple missing/inactive tools"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        issue_body = f"""## 🔧 Multiple Tool Detection Alert

**Detected:** {timestamp}  
**Auto-generated:** Yes (Self-Improvement Mechanism)

---

## 📋 Summary

The self-improvement mechanism has detected multiple tools that require attention:

"""
        
        if missing_tools:
            issue_body += f"""### Missing Tools ({len(missing_tools)})
The following tools are marked as required but are not present in the manifest:

"""
            for tool_id in missing_tools:
                tool_name = tool_id.replace("_", " ").title()
                issue_body += f"- [ ] **{tool_name}** (`{tool_id}`)\n"
            issue_body += "\n"
        
        if inactive_tools:
            issue_body += f"""### Inactive Tools ({len(inactive_tools)})
The following tools exist but are marked as inactive:

"""
            for tool_id in inactive_tools:
                tool_name = tool_id.replace("_", " ").title()
                issue_body += f"- [ ] **{tool_name}** (`{tool_id}`)\n"
            issue_body += "\n"
        
        issue_body += """---

## 🎯 Action Required

For each tool listed above:

1. Create individual tracking issues using the command:
   ```bash
   python -m app.core.self_improvement generate-issue <tool_id>
   ```

2. Or implement all at once following the manifest schema

---

## 📚 Resources

- **Manifest:** `backend/app/core/manifest.json`
- **Generator:** `backend/app/core/self_improvement.py`
- **Documentation:** `SYSTEM_WILL.md`

---

**Generated by Cimeika Self-Improvement Mechanism v1.0**
"""
        
        return issue_body


def validate_and_report() -> Dict:
    """
    Validate tools and generate issue descriptions if needed
    Returns dict with validation results and generated issues
    """
    manifest = ToolManifest()
    validation = manifest.validate_tools()
    
    result = {
        "validation": validation,
        "issues": []
    }
    
    # Generate individual issues for missing tools
    for tool_id in validation.get("missing", []):
        issue_title = GitHubIssueGenerator.generate_issue_title(tool_id, "missing")
        issue_body = GitHubIssueGenerator.generate_issue_body(tool_id, "missing")
        result["issues"].append({
            "tool_id": tool_id,
            "title": issue_title,
            "body": issue_body,
            "reason": "missing"
        })
    
    # Generate individual issues for inactive tools
    for tool_id in validation.get("inactive", []):
        tool = manifest.get_tool(tool_id)
        issue_title = GitHubIssueGenerator.generate_issue_title(tool_id, "inactive")
        issue_body = GitHubIssueGenerator.generate_issue_body(
            tool_id, 
            "inactive",
            context={"current_status": tool.get("status")}
        )
        result["issues"].append({
            "tool_id": tool_id,
            "title": issue_title,
            "body": issue_body,
            "reason": "inactive"
        })
    
    return result


# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python -m app.core.self_improvement validate")
        print("  python -m app.core.self_improvement generate-issue <tool_id> [reason]")
        print("  python -m app.core.self_improvement report")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "validate":
        # Validate manifest
        manifest = ToolManifest()
        validation = manifest.validate_tools()
        
        print("=== Tool Manifest Validation ===\n")
        if validation["all_present"]:
            print("✅ All required tools are present and active")
        else:
            if validation["missing"]:
                print(f"❌ Missing tools: {', '.join(validation['missing'])}")
            if validation["inactive"]:
                print(f"⚠️  Inactive tools: {', '.join(validation['inactive'])}")
    
    elif command == "generate-issue":
        if len(sys.argv) < 3:
            print("Error: tool_id required")
            sys.exit(1)
        
        tool_id = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "missing"
        
        title = GitHubIssueGenerator.generate_issue_title(tool_id, reason)
        body = GitHubIssueGenerator.generate_issue_body(tool_id, reason)
        
        print("=== GitHub Issue ===\n")
        print(f"Title: {title}\n")
        print(body)
    
    elif command == "report":
        # Full validation and issue generation
        result = validate_and_report()
        validation = result["validation"]
        
        print("=== Self-Improvement Report ===\n")
        
        if validation["all_present"]:
            print("✅ All required tools are present and active\n")
            print("No issues to generate.")
        else:
            print(f"Found {len(result['issues'])} issue(s) to report:\n")
            
            for i, issue in enumerate(result["issues"], 1):
                print(f"{i}. {issue['title']}")
                print(f"   Tool: {issue['tool_id']}")
                print(f"   Reason: {issue['reason']}\n")
            
            print("\nGenerate individual issues with:")
            for issue in result["issues"]:
                print(f"  python -m app.core.self_improvement generate-issue {issue['tool_id']} {issue['reason']}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
