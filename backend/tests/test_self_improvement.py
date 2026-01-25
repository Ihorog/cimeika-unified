"""
Tests for Self-Improvement Mechanism
"""
import json
import pytest
from pathlib import Path
from app.core.self_improvement import (
    ToolManifest,
    GitHubIssueGenerator,
    validate_and_report
)


class TestToolManifest:
    """Test ToolManifest class"""
    
    def test_load_manifest(self):
        """Test manifest loading"""
        manifest = ToolManifest()
        assert manifest.manifest is not None
        assert "tools" in manifest.manifest
        assert "required_tools" in manifest.manifest
    
    def test_get_tool_existing(self):
        """Test getting an existing tool"""
        manifest = ToolManifest()
        tool = manifest.get_tool("ci_core")
        assert tool is not None
        assert tool["id"] == "ci_core"
        assert tool["status"] == "active"
    
    def test_get_tool_nonexistent(self):
        """Test getting a non-existent tool"""
        manifest = ToolManifest()
        tool = manifest.get_tool("nonexistent_tool")
        assert tool is None
    
    def test_get_all_tools(self):
        """Test getting all tools"""
        manifest = ToolManifest()
        tools = manifest.get_all_tools()
        assert isinstance(tools, list)
        assert len(tools) > 0
    
    def test_get_required_tools(self):
        """Test getting required tools list"""
        manifest = ToolManifest()
        required = manifest.get_required_tools()
        assert isinstance(required, list)
        assert "ci_core" in required
    
    def test_validate_tools_all_present(self):
        """Test validation when all tools are present"""
        manifest = ToolManifest()
        validation = manifest.validate_tools()
        
        assert "missing" in validation
        assert "inactive" in validation
        assert "all_present" in validation
        
        # With current manifest, all should be present
        assert validation["all_present"] is True
        assert len(validation["missing"]) == 0
        assert len(validation["inactive"]) == 0


class TestGitHubIssueGenerator:
    """Test GitHubIssueGenerator class"""
    
    def test_generate_issue_title_missing(self):
        """Test issue title generation for missing tool"""
        title = GitHubIssueGenerator.generate_issue_title("test_tool", "missing")
        assert "[Tool Missing]" in title
        assert "Test Tool" in title
    
    def test_generate_issue_title_inactive(self):
        """Test issue title generation for inactive tool"""
        title = GitHubIssueGenerator.generate_issue_title("test_tool", "inactive")
        assert "[Tool Inactive]" in title
        assert "Test Tool" in title
    
    def test_generate_issue_body_missing(self):
        """Test issue body generation for missing tool"""
        body = GitHubIssueGenerator.generate_issue_body("test_tool", "missing")
        
        # Check for key sections
        assert "Tool Detection Alert" in body
        assert "test_tool" in body
        assert "Missing Tool" in body
        assert "Acceptance Criteria" in body
        assert "Implementation Guidance" in body
        assert "manifest.json" in body
    
    def test_generate_issue_body_inactive(self):
        """Test issue body generation for inactive tool"""
        body = GitHubIssueGenerator.generate_issue_body("test_tool", "inactive")
        
        # Check for key sections
        assert "Tool Detection Alert" in body
        assert "test_tool" in body
        assert "Inactive Tool" in body
        assert "Acceptance Criteria" in body
    
    def test_generate_issue_body_with_context(self):
        """Test issue body generation with additional context"""
        context = {"reason": "API endpoint not responding", "priority": "high"}
        body = GitHubIssueGenerator.generate_issue_body(
            "test_tool", 
            "missing", 
            context=context
        )
        
        assert "Additional Context" in body
        assert "reason" in body
        assert "priority" in body
    
    def test_generate_batch_issue(self):
        """Test batch issue generation"""
        missing = ["tool1", "tool2"]
        inactive = ["tool3"]
        
        body = GitHubIssueGenerator.generate_batch_issue(missing, inactive)
        
        assert "Multiple Tool Detection Alert" in body
        assert "tool1" in body
        assert "tool2" in body
        assert "tool3" in body
        assert "Missing Tools (2)" in body
        assert "Inactive Tools (1)" in body


class TestValidateAndReport:
    """Test validate_and_report function"""
    
    def test_validate_and_report(self):
        """Test full validation and reporting"""
        result = validate_and_report()
        
        assert "validation" in result
        assert "issues" in result
        
        validation = result["validation"]
        assert "missing" in validation
        assert "inactive" in validation
        assert "all_present" in validation
        
        # Issues list should be present
        assert isinstance(result["issues"], list)


class TestManifestSchema:
    """Test manifest.json schema compliance"""
    
    def test_manifest_file_exists(self):
        """Test that manifest.json exists"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        assert manifest_path.exists()
    
    def test_manifest_valid_json(self):
        """Test that manifest is valid JSON"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        assert isinstance(data, dict)
    
    def test_manifest_required_fields(self):
        """Test that manifest has required fields"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        assert "version" in data
        assert "tools" in data
        assert "required_tools" in data
    
    def test_tools_have_required_fields(self):
        """Test that each tool has required fields"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        required_fields = ["id", "name", "description", "status", "category"]
        
        for tool in data.get("tools", []):
            for field in required_fields:
                assert field in tool, f"Tool {tool.get('id', 'unknown')} missing field: {field}"
    
    def test_tool_status_valid(self):
        """Test that tool status values are valid"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        valid_statuses = ["active", "inactive", "deprecated"]
        
        for tool in data.get("tools", []):
            status = tool.get("status")
            assert status in valid_statuses, f"Tool {tool['id']} has invalid status: {status}"
    
    def test_tool_category_valid(self):
        """Test that tool category values are valid"""
        manifest_path = Path(__file__).parent.parent / "app" / "core" / "manifest.json"
        with open(manifest_path, 'r') as f:
            data = json.load(f)
        
        valid_categories = ["core", "module", "service", "integration"]
        
        for tool in data.get("tools", []):
            category = tool.get("category")
            assert category in valid_categories, f"Tool {tool['id']} has invalid category: {category}"
