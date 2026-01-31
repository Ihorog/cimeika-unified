"""
Test integration between abilities system and self_improvement mechanism
"""
import pytest
from pathlib import Path
from app.core.self_improvement import ToolManifest


class TestAbilitiesSelfImprovementIntegration:
    """Test that abilities system integrates with self_improvement validation"""
    
    def test_abilities_in_manifest(self):
        """Test that abilities_system is present in the manifest"""
        manifest = ToolManifest()
        
        abilities_tool = manifest.get_tool("abilities_system")
        
        assert abilities_tool is not None
        assert abilities_tool["id"] == "abilities_system"
        assert abilities_tool["name"] == "Abilities System"
        assert abilities_tool["status"] == "active"
    
    def test_abilities_in_required_tools(self):
        """Test that abilities_system is in required tools list"""
        manifest = ToolManifest()
        
        required_tools = manifest.get_required_tools()
        
        assert "abilities_system" in required_tools
    
    def test_abilities_endpoints_defined(self):
        """Test that abilities endpoints are defined in manifest"""
        manifest = ToolManifest()
        
        abilities_tool = manifest.get_tool("abilities_system")
        
        assert "endpoints" in abilities_tool
        endpoints = abilities_tool["endpoints"]
        
        # Check that key endpoints are present
        assert "/api/v1/abilities" in endpoints
        assert "/api/v1/abilities/manifest" in endpoints
        assert any("activate" in ep for ep in endpoints)
        assert any("deactivate" in ep for ep in endpoints)
        assert any("execute" in ep for ep in endpoints)
    
    def test_abilities_has_sub_components(self):
        """Test that abilities_system lists its sub-components"""
        manifest = ToolManifest()
        
        abilities_tool = manifest.get_tool("abilities_system")
        
        assert "sub_components" in abilities_tool
        sub_components = abilities_tool["sub_components"]
        
        # Check the three dormant abilities are listed
        assert "notes" in sub_components
        assert "scheduler" in sub_components
        assert "intent_observer" in sub_components
    
    def test_manifest_validation_passes(self):
        """Test that manifest validation passes with abilities system"""
        manifest = ToolManifest()
        
        validation_result = manifest.validate_tools()
        
        # abilities_system should not be in missing or inactive
        assert "abilities_system" not in validation_result.get("missing", [])
        assert "abilities_system" not in validation_result.get("inactive", [])
