"""
Core orchestrator for module coordination
"""
from typing import Dict, Any


class ModuleRegistry:
    """Registry for all Cimeika modules"""
    
    def __init__(self):
        self._modules: Dict[str, Any] = {}
    
    def register(self, name: str, module: Any) -> None:
        """Register a module"""
        self._modules[name] = module
    
    def get(self, name: str) -> Any:
        """Get a registered module"""
        return self._modules.get(name)
    
    def list_modules(self) -> list:
        """List all registered modules"""
        return list(self._modules.keys())


# Global registry instance
registry = ModuleRegistry()
