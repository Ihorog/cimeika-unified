"""
Notes Ability Module
Provides note-taking and knowledge capture functionality.
"""
from typing import Any, Dict
from ..base import Ability


class NotesAbility(Ability):
    """
    Note-taking and knowledge capture ability.
    
    Activation Triggers:
    - User explicitly requests note-taking functionality
    - System detects need for persistent knowledge storage
    - Integration with Kazkar (memory/legends) module
    
    States:
    - Dormant: No background processes, minimal memory footprint
    - Active: Ready to capture and retrieve notes
    """
    
    def __init__(self):
        """Initialize notes ability in dormant state."""
        self._active = False
        self._notes_storage: Dict[str, Any] = {}
    
    @property
    def name(self) -> str:
        """Unique ability identifier."""
        return "notes"
    
    @property
    def version(self) -> str:
        """Semantic version."""
        return "0.1.0"
    
    async def activate(self) -> None:
        """
        Transition from dormant to active state.
        Initialize note storage and indexing structures.
        """
        if not self._active:
            # Initialize storage structures
            self._notes_storage = {}
            self._active = True
    
    async def deactivate(self) -> None:
        """
        Return to dormant state.
        Persist any pending notes and clean up resources.
        """
        if self._active:
            # Could persist notes to database here
            self._active = False
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute note-taking operations.
        
        Args:
            context: Operation context with keys:
                - action: "create", "read", "update", "delete", "list"
                - note_id: Optional note identifier
                - content: Note content for create/update
                - metadata: Optional metadata dict
        
        Returns:
            Result dict with operation status and data
        """
        if not self._active:
            return {"error": "Notes ability is not active"}
        
        action = context.get("action", "list")
        
        if action == "create":
            note_id = context.get("note_id", f"note_{len(self._notes_storage) + 1}")
            self._notes_storage[note_id] = {
                "content": context.get("content", ""),
                "metadata": context.get("metadata", {})
            }
            return {"status": "created", "note_id": note_id}
        
        elif action == "read":
            note_id = context.get("note_id")
            if note_id in self._notes_storage:
                return {"status": "success", "note": self._notes_storage[note_id]}
            return {"error": "Note not found"}
        
        elif action == "update":
            note_id = context.get("note_id")
            if note_id in self._notes_storage:
                if "content" in context:
                    self._notes_storage[note_id]["content"] = context["content"]
                if "metadata" in context:
                    self._notes_storage[note_id]["metadata"].update(context["metadata"])
                return {"status": "updated", "note_id": note_id}
            return {"error": "Note not found"}
        
        elif action == "delete":
            note_id = context.get("note_id")
            if note_id in self._notes_storage:
                del self._notes_storage[note_id]
                return {"status": "deleted", "note_id": note_id}
            return {"error": "Note not found"}
        
        elif action == "list":
            return {
                "status": "success",
                "notes": list(self._notes_storage.keys()),
                "count": len(self._notes_storage)
            }
        
        return {"error": f"Unknown action: {action}"}
