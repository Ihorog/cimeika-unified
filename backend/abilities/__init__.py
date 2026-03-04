"""
Ability Registry for CIT-ORGANISM Plugin System
Manages discovery, registration, and lifecycle of dormant abilities.
"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Type
from .base import Ability

logger = logging.getLogger(__name__)


class AbilityRegistry:
    """Singleton registry for managing abilities."""
    
    _instance: Optional['AbilityRegistry'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize registry (only once)."""
        if not self._initialized:
            self._abilities: Dict[str, Ability] = {}
            self._manifest_path = Path(__file__).parent / "manifest.json"
            self._manifest = self._load_manifest()
            AbilityRegistry._initialized = True
            logger.info("AbilityRegistry initialized")
    
    def _load_manifest(self) -> Dict:
        """Load manifest from JSON file."""
        if not self._manifest_path.exists():
            logger.warning(f"Manifest not found at {self._manifest_path}, using empty manifest")
            return {"version": "1.0.0", "abilities": {}}
        
        try:
            with open(self._manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading manifest: {e}")
            return {"version": "1.0.0", "abilities": {}}
    
    def _save_manifest(self) -> None:
        """Save current manifest state to JSON file."""
        try:
            with open(self._manifest_path, 'w', encoding='utf-8') as f:
                json.dump(self._manifest, f, indent=2)
            logger.info("Manifest saved successfully")
        except Exception as e:
            logger.error(f"Error saving manifest: {e}")
    
    def register(self, ability: Ability) -> None:
        """Register an ability instance."""
        ability_name = ability.name
        if ability_name in self._abilities:
            logger.warning(f"Ability '{ability_name}' is already registered, replacing")
        
        self._abilities[ability_name] = ability
        logger.info(f"Registered ability: {ability_name} (v{ability.version})")
    
    def get(self, name: str) -> Optional[Ability]:
        """Get ability by name."""
        return self._abilities.get(name)
    
    def list_abilities(self) -> List[Dict]:
        """List all registered abilities with their metadata."""
        abilities_list = []
        for name, ability in self._abilities.items():
            manifest_data = self._manifest.get("abilities", {}).get(name, {})
            abilities_list.append({
                "name": name,
                "version": ability.version,
                "is_active": ability.is_active,
                "enabled": manifest_data.get("enabled", False),
                "description": manifest_data.get("description", ""),
                "dependencies": manifest_data.get("dependencies", [])
            })
        return abilities_list
    
    async def activate(self, name: str) -> bool:
        """Activate an ability."""
        ability = self.get(name)
        if not ability:
            logger.error(f"Ability '{name}' not found")
            return False
        
        if ability.is_active:
            logger.warning(f"Ability '{name}' is already active")
            return True
        
        try:
            await ability.activate()
            
            # Update manifest
            if name in self._manifest.get("abilities", {}):
                self._manifest["abilities"][name]["enabled"] = True
                self._save_manifest()
            
            logger.info(f"Activated ability: {name}")
            return True
        except Exception as e:
            logger.error(f"Error activating ability '{name}': {e}")
            return False
    
    async def deactivate(self, name: str) -> bool:
        """Deactivate an ability."""
        ability = self.get(name)
        if not ability:
            logger.error(f"Ability '{name}' not found")
            return False
        
        if not ability.is_active:
            logger.warning(f"Ability '{name}' is already inactive")
            return True
        
        try:
            await ability.deactivate()
            
            # Update manifest
            if name in self._manifest.get("abilities", {}):
                self._manifest["abilities"][name]["enabled"] = False
                self._save_manifest()
            
            logger.info(f"Deactivated ability: {name}")
            return True
        except Exception as e:
            logger.error(f"Error deactivating ability '{name}': {e}")
            return False
    
    async def execute(self, name: str, context: Dict) -> Optional[Dict]:
        """Execute an ability with given context."""
        ability = self.get(name)
        if not ability:
            logger.error(f"Ability '{name}' not found")
            return None
        
        if not ability.is_active:
            logger.error(f"Ability '{name}' is not active")
            return None
        
        try:
            result = await ability.execute(context)
            logger.info(f"Executed ability: {name}")
            return result
        except Exception as e:
            logger.error(f"Error executing ability '{name}': {e}")
            return None
    
    def get_manifest(self) -> Dict:
        """Get current manifest."""
        return self._manifest.copy()


# Global registry instance
registry = AbilityRegistry()

# Import ability implementations
from .notes import NotesAbility
from .scheduler import SchedulerAbility
from .intent_observer import IntentObserverAbility
from .quickstart_ci import QuickstartCiAbility

__all__ = [
    'Ability', 
    'AbilityRegistry', 
    'registry',
    'NotesAbility',
    'SchedulerAbility',
    'IntentObserverAbility',
    'QuickstartCiAbility'
]
