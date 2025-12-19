"""
Core orchestrator for module coordination
"""
from typing import Dict, Any, Optional, List
from .interfaces import ModuleInterface


class ModuleRegistry:
    """Registry for all Cimeika modules"""
    
    def __init__(self):
        self._modules: Dict[str, ModuleInterface] = {}
    
    def register(self, name: str, module: ModuleInterface) -> None:
        """
        Register a module
        
        Args:
            name: Module name
            module: Module instance implementing ModuleInterface
            
        Raises:
            TypeError: If module doesn't implement ModuleInterface
        """
        if not isinstance(module, ModuleInterface):
            raise TypeError(
                f"Module {name} must implement ModuleInterface"
            )
        self._modules[name] = module
    
    def get(self, name: str) -> Optional[ModuleInterface]:
        """
        Get a registered module
        
        Args:
            name: Module name
            
        Returns:
            Module instance or None if not found
        """
        return self._modules.get(name)
    
    def list_modules(self) -> List[str]:
        """
        List all registered modules
        
        Returns:
            List of module names
        """
        return list(self._modules.keys())
    
    def get_all_statuses(self) -> Dict[str, Dict[str, Any]]:
        """
        Get status of all registered modules
        
        Returns:
            Dict mapping module names to their status
        """
        return {
            name: module.get_status()
            for name, module in self._modules.items()
        }
    
    def initialize_all(self) -> Dict[str, bool]:
        """
        Initialize all registered modules
        
        Returns:
            Dict mapping module names to initialization success
        """
        results = {}
        for name, module in self._modules.items():
            try:
                results[name] = module.initialize()
            except Exception as e:
                results[name] = False
                print(f"Failed to initialize {name}: {e}")
        return results
    
    def shutdown_all(self) -> Dict[str, bool]:
        """
        Shutdown all registered modules
        
        Returns:
            Dict mapping module names to shutdown success
        """
        results = {}
        for name, module in self._modules.items():
            try:
                results[name] = module.shutdown()
            except Exception as e:
                results[name] = False
                print(f"Failed to shutdown {name}: {e}")
        return results
    
    def unregister(self, name: str) -> bool:
        """
        Unregister a module
        
        Args:
            name: Module name
            
        Returns:
            True if module was unregistered, False if not found
        """
        if name in self._modules:
            module = self._modules[name]
            module.shutdown()
            del self._modules[name]
            return True
        return False


# Global registry instance
registry = ModuleRegistry()
