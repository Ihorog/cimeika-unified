"""
Tests for Abilities System
Tests the base Ability class, AbilityRegistry, and individual abilities.
"""
import pytest
import json
from pathlib import Path
import sys

# Add abilities module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "abilities"))

from abilities import registry, Ability, AbilityRegistry
from abilities.notes import NotesAbility
from abilities.scheduler import SchedulerAbility
from abilities.intent_observer import IntentObserverAbility
from abilities.quickstart_ci import QuickstartCiAbility


class TestAbilityBase:
    """Test base Ability interface"""
    
    def test_ability_has_required_properties(self):
        """Test that ability has all required properties"""
        ability = NotesAbility()
        
        # Check properties exist
        assert hasattr(ability, 'name')
        assert hasattr(ability, 'version')
        assert hasattr(ability, 'is_active')
        
        # Check initial state
        assert isinstance(ability.name, str)
        assert isinstance(ability.version, str)
        assert isinstance(ability.is_active, bool)
        assert ability.is_active is False
    
    def test_ability_has_required_methods(self):
        """Test that ability has all required methods"""
        ability = NotesAbility()
        
        # Check methods exist
        assert hasattr(ability, 'activate')
        assert hasattr(ability, 'deactivate')
        assert hasattr(ability, 'execute')
        
        # Check they are callable
        assert callable(ability.activate)
        assert callable(ability.deactivate)
        assert callable(ability.execute)


class TestAbilityRegistry:
    """Test AbilityRegistry class"""
    
    def test_registry_is_singleton(self):
        """Test that registry follows singleton pattern"""
        registry1 = AbilityRegistry()
        registry2 = AbilityRegistry()
        
        assert registry1 is registry2
    
    def test_register_ability(self):
        """Test registering an ability"""
        test_registry = AbilityRegistry()
        ability = NotesAbility()
        
        test_registry.register(ability)
        
        registered = test_registry.get("notes")
        assert registered is not None
        assert registered.name == "notes"
    
    def test_get_nonexistent_ability(self):
        """Test getting a non-existent ability"""
        test_registry = AbilityRegistry()
        
        ability = test_registry.get("nonexistent_ability")
        assert ability is None
    
    def test_list_abilities(self):
        """Test listing all abilities"""
        test_registry = AbilityRegistry()
        
        # Register some abilities
        test_registry.register(NotesAbility())
        test_registry.register(SchedulerAbility())
        
        abilities = test_registry.list_abilities()
        
        assert isinstance(abilities, list)
        assert len(abilities) >= 2
        
        # Check structure
        for ability in abilities:
            assert "name" in ability
            assert "version" in ability
            assert "is_active" in ability
    
    def test_get_manifest(self):
        """Test getting the manifest"""
        test_registry = AbilityRegistry()
        
        manifest = test_registry.get_manifest()
        
        assert isinstance(manifest, dict)
        assert "version" in manifest
        assert "abilities" in manifest


class TestNotesAbility:
    """Test NotesAbility implementation"""
    
    @pytest.mark.asyncio
    async def test_notes_activation(self):
        """Test activating notes ability"""
        ability = NotesAbility()
        
        assert ability.is_active is False
        
        await ability.activate()
        
        assert ability.is_active is True
    
    @pytest.mark.asyncio
    async def test_notes_deactivation(self):
        """Test deactivating notes ability"""
        ability = NotesAbility()
        
        await ability.activate()
        assert ability.is_active is True
        
        await ability.deactivate()
        assert ability.is_active is False
    
    @pytest.mark.asyncio
    async def test_notes_create_operation(self):
        """Test creating a note"""
        ability = NotesAbility()
        await ability.activate()
        
        result = await ability.execute({
            "action": "create",
            "note_id": "test_note",
            "content": "Test content"
        })
        
        assert result["status"] == "created"
        assert result["note_id"] == "test_note"
    
    @pytest.mark.asyncio
    async def test_notes_read_operation(self):
        """Test reading a note"""
        ability = NotesAbility()
        await ability.activate()
        
        # Create a note first
        await ability.execute({
            "action": "create",
            "note_id": "test_note",
            "content": "Test content"
        })
        
        # Read it back
        result = await ability.execute({
            "action": "read",
            "note_id": "test_note"
        })
        
        assert result["status"] == "success"
        assert result["note"]["content"] == "Test content"
    
    @pytest.mark.asyncio
    async def test_notes_update_operation(self):
        """Test updating a note"""
        ability = NotesAbility()
        await ability.activate()
        
        # Create a note
        await ability.execute({
            "action": "create",
            "note_id": "test_note",
            "content": "Original content"
        })
        
        # Update it
        result = await ability.execute({
            "action": "update",
            "note_id": "test_note",
            "content": "Updated content"
        })
        
        assert result["status"] == "updated"
        
        # Verify the update
        read_result = await ability.execute({
            "action": "read",
            "note_id": "test_note"
        })
        assert read_result["note"]["content"] == "Updated content"
    
    @pytest.mark.asyncio
    async def test_notes_delete_operation(self):
        """Test deleting a note"""
        ability = NotesAbility()
        await ability.activate()
        
        # Create a note
        await ability.execute({
            "action": "create",
            "note_id": "test_note",
            "content": "To be deleted"
        })
        
        # Delete it
        result = await ability.execute({
            "action": "delete",
            "note_id": "test_note"
        })
        
        assert result["status"] == "deleted"
        
        # Verify it's gone
        read_result = await ability.execute({
            "action": "read",
            "note_id": "test_note"
        })
        assert "error" in read_result
    
    @pytest.mark.asyncio
    async def test_notes_list_operation(self):
        """Test listing notes"""
        ability = NotesAbility()
        await ability.activate()
        
        # Create some notes
        await ability.execute({
            "action": "create",
            "note_id": "note1",
            "content": "Content 1"
        })
        await ability.execute({
            "action": "create",
            "note_id": "note2",
            "content": "Content 2"
        })
        
        # List them
        result = await ability.execute({
            "action": "list"
        })
        
        assert result["status"] == "success"
        assert result["count"] == 2
        assert "note1" in result["notes"]
        assert "note2" in result["notes"]
    
    @pytest.mark.asyncio
    async def test_notes_inactive_error(self):
        """Test that executing on inactive ability returns error"""
        ability = NotesAbility()
        
        result = await ability.execute({
            "action": "list"
        })
        
        assert "error" in result
        assert "not active" in result["error"]


class TestSchedulerAbility:
    """Test SchedulerAbility implementation"""
    
    @pytest.mark.asyncio
    async def test_scheduler_activation(self):
        """Test activating scheduler ability"""
        ability = SchedulerAbility()
        
        assert ability.is_active is False
        
        await ability.activate()
        
        assert ability.is_active is True
    
    @pytest.mark.asyncio
    async def test_scheduler_schedule_task(self):
        """Test scheduling a task"""
        ability = SchedulerAbility()
        await ability.activate()
        
        result = await ability.execute({
            "action": "schedule",
            "task_id": "test_task",
            "scheduled_time": "2026-02-01T10:00:00",
            "task_data": {"type": "reminder"}
        })
        
        assert result["status"] == "scheduled"
        assert result["task_id"] == "test_task"
    
    @pytest.mark.asyncio
    async def test_scheduler_cancel_task(self):
        """Test canceling a scheduled task"""
        ability = SchedulerAbility()
        await ability.activate()
        
        # Schedule a task
        await ability.execute({
            "action": "schedule",
            "task_id": "test_task",
            "scheduled_time": "2026-02-01T10:00:00"
        })
        
        # Cancel it
        result = await ability.execute({
            "action": "cancel",
            "task_id": "test_task"
        })
        
        assert result["status"] == "cancelled"
    
    @pytest.mark.asyncio
    async def test_scheduler_list_tasks(self):
        """Test listing scheduled tasks"""
        ability = SchedulerAbility()
        await ability.activate()
        
        # Schedule some tasks
        await ability.execute({
            "action": "schedule",
            "task_id": "task1",
            "scheduled_time": "2026-02-01T10:00:00"
        })
        await ability.execute({
            "action": "schedule",
            "task_id": "task2",
            "scheduled_time": "2026-02-01T11:00:00"
        })
        
        # List them
        result = await ability.execute({
            "action": "list"
        })
        
        assert result["status"] == "success"
        assert result["count"] == 2


class TestIntentObserverAbility:
    """Test IntentObserverAbility implementation"""
    
    @pytest.mark.asyncio
    async def test_intent_observer_activation(self):
        """Test activating intent observer ability"""
        ability = IntentObserverAbility()
        
        assert ability.is_active is False
        
        await ability.activate()
        
        assert ability.is_active is True
    
    @pytest.mark.asyncio
    async def test_intent_observer_observe(self):
        """Test observing an intent"""
        ability = IntentObserverAbility()
        await ability.activate()
        
        result = await ability.execute({
            "action": "observe",
            "intent": "create_note",
            "user_id": "user_123"
        })
        
        assert result["status"] == "observed"
        assert result["intent"] == "create_note"
        assert result["total_observations"] == 1
    
    @pytest.mark.asyncio
    async def test_intent_observer_analyze(self):
        """Test analyzing intent patterns"""
        ability = IntentObserverAbility()
        await ability.activate()
        
        # Observe some intents
        await ability.execute({
            "action": "observe",
            "intent": "create_note"
        })
        await ability.execute({
            "action": "observe",
            "intent": "create_note"
        })
        await ability.execute({
            "action": "observe",
            "intent": "schedule_task"
        })
        
        # Analyze patterns
        result = await ability.execute({
            "action": "analyze"
        })
        
        assert result["status"] == "success"
        assert "analysis" in result
        assert result["analysis"]["total_observations"] == 3
        assert result["analysis"]["unique_intents"] == 2
        assert result["analysis"]["most_common_intent"] == "create_note"
    
    @pytest.mark.asyncio
    async def test_intent_observer_patterns(self):
        """Test getting intent patterns"""
        ability = IntentObserverAbility()
        await ability.activate()
        
        # Observe some intents
        await ability.execute({
            "action": "observe",
            "intent": "intent1"
        })
        await ability.execute({
            "action": "observe",
            "intent": "intent1"
        })
        await ability.execute({
            "action": "observe",
            "intent": "intent2"
        })
        
        # Get patterns with threshold
        result = await ability.execute({
            "action": "patterns",
            "threshold": 2
        })
        
        assert result["status"] == "success"
        assert "intent1" in result["patterns"]
        assert result["patterns"]["intent1"] == 2
        # intent2 should be filtered out (count=1, threshold=2)
        assert "intent2" not in result["patterns"]
    
    @pytest.mark.asyncio
    async def test_intent_observer_clear(self):
        """Test clearing observations"""
        ability = IntentObserverAbility()
        await ability.activate()
        
        # Observe some intents
        await ability.execute({
            "action": "observe",
            "intent": "test_intent"
        })
        
        # Clear
        result = await ability.execute({
            "action": "clear"
        })
        
        assert result["status"] == "cleared"
        
        # Verify cleared
        patterns_result = await ability.execute({
            "action": "patterns"
        })
        assert patterns_result["count"] == 0


class TestAbilityRegistryIntegration:
    """Test AbilityRegistry with multiple abilities"""
    
    @pytest.mark.asyncio
    async def test_activate_through_registry(self):
        """Test activating ability through registry"""
        test_registry = AbilityRegistry()
        test_registry.register(NotesAbility())
        
        success = await test_registry.activate("notes")
        
        assert success is True
        
        ability = test_registry.get("notes")
        assert ability.is_active is True
    
    @pytest.mark.asyncio
    async def test_deactivate_through_registry(self):
        """Test deactivating ability through registry"""
        test_registry = AbilityRegistry()
        test_registry.register(NotesAbility())
        
        await test_registry.activate("notes")
        success = await test_registry.deactivate("notes")
        
        assert success is True
        
        ability = test_registry.get("notes")
        assert ability.is_active is False
    
    @pytest.mark.asyncio
    async def test_execute_through_registry(self):
        """Test executing ability through registry"""
        test_registry = AbilityRegistry()
        test_registry.register(NotesAbility())
        
        await test_registry.activate("notes")
        
        result = await test_registry.execute("notes", {
            "action": "create",
            "note_id": "test",
            "content": "Test"
        })
        
        assert result is not None
        assert result["status"] == "created"
    
    @pytest.mark.asyncio
    async def test_execute_inactive_ability(self):
        """Test executing inactive ability returns None"""
        test_registry = AbilityRegistry()
        test_registry.register(NotesAbility())
        
        result = await test_registry.execute("notes", {
            "action": "list"
        })
        
        assert result is None


class TestQuickstartCiAbility:
    """Test QuickstartCiAbility implementation"""

    @pytest.mark.asyncio
    async def test_quickstart_ci_initial_state(self):
        """Ability is dormant by default"""
        ability = QuickstartCiAbility()
        assert ability.name == "quickstart_ci"
        assert ability.version == "0.1.0"
        assert ability.is_active is False

    @pytest.mark.asyncio
    async def test_quickstart_ci_activation(self):
        """Ability transitions to active state"""
        ability = QuickstartCiAbility()
        await ability.activate()
        assert ability.is_active is True

    @pytest.mark.asyncio
    async def test_quickstart_ci_deactivation(self):
        """Ability returns to dormant state"""
        ability = QuickstartCiAbility()
        await ability.activate()
        await ability.deactivate()
        assert ability.is_active is False

    @pytest.mark.asyncio
    async def test_execute_while_inactive_returns_error(self):
        """Executing while dormant returns an error dict"""
        ability = QuickstartCiAbility()
        result = await ability.execute({"action": "get_spec"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_get_spec_returns_widgetspec(self):
        """get_spec returns the full WidgetSpec"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({"action": "get_spec"})
        assert result["status"] == "success"
        spec = result["spec"]
        assert spec["name"] == "quickstart_ci"
        assert spec["template_engine"] == "jinja2"
        assert "jsonSchema" in spec
        assert "template" in spec
        assert "outputJsonPreview" in spec

    @pytest.mark.asyncio
    async def test_list_quick_returns_items(self):
        """list_quick returns buttons from outputJsonPreview"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({"action": "list_quick"})
        assert result["status"] == "success"
        items = result["quick_items"]
        assert isinstance(items, list)
        assert len(items) > 0
        for item in items:
            assert "id" in item
            assert "label" in item

    @pytest.mark.asyncio
    async def test_validate_valid_model(self):
        """validate returns valid=True for a conforming model"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({
            "action": "validate",
            "model": {
                "quick_items": [
                    {"id": "run_ci", "label": "Run CI"}
                ]
            }
        })
        assert result["valid"] is True
        assert result["errors"] == []

    @pytest.mark.asyncio
    async def test_validate_missing_required_field(self):
        """validate returns errors when required field is absent"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({
            "action": "validate",
            "model": {}
        })
        assert result["valid"] is False
        assert any("quick_items" in e for e in result["errors"])

    @pytest.mark.asyncio
    async def test_validate_missing_item_required_field(self):
        """validate returns errors when a quick item is missing required field"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({
            "action": "validate",
            "model": {
                "quick_items": [
                    {"id": "run_ci"}  # missing 'label'
                ]
            }
        })
        assert result["valid"] is False
        assert any("label" in e for e in result["errors"])

    @pytest.mark.asyncio
    async def test_validate_without_model_key_returns_error(self):
        """validate without 'model' key returns an error dict"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({"action": "validate"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_unknown_action_returns_error(self):
        """Unknown action returns an error dict"""
        ability = QuickstartCiAbility()
        await ability.activate()
        result = await ability.execute({"action": "nonexistent"})
        assert "error" in result

    @pytest.mark.asyncio
    async def test_spec_template_is_valid_jinja2(self):
        """Template in the spec is valid Jinja2 syntax"""
        try:
            from jinja2 import Environment
        except ImportError:
            pytest.skip("jinja2 not installed")

        ability = QuickstartCiAbility()
        await ability.activate()
        spec_result = await ability.execute({"action": "get_spec"})
        template_str = spec_result["spec"]["template"]

        env = Environment()
        # Should not raise
        tmpl = env.from_string(template_str)
        output = tmpl.render(quick_items=[{"id": "run_ci", "label": "Run CI"}])
        # Output should be parseable as JSON
        parsed = json.loads(output)
        assert parsed["type"] == "widget"
        children = parsed["children"]
        assert len(children) == 1
        assert children[0]["action"]["type"] == "ci.quick"
        assert children[0]["action"]["payload"]["id"] == "run_ci"
