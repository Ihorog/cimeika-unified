"""
Core interfaces for Cimeika modules
Defines the contract that all modules must implement
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ModuleInterface(ABC):
    """
    Base interface that all Cimeika modules must implement
    
    This ensures consistent behavior across all modules and
    allows the core orchestrator to interact with modules uniformly.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the module name
        
        Returns:
            str: Module name (e.g., 'ci', 'kazkar', 'podija')
        """
        pass
    
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the module
        
        Returns:
            Dict: Status information including at minimum:
                - status: str (e.g., 'active', 'inactive', 'error')
                - Additional module-specific status info
        """
        pass
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the module
        
        Returns:
            bool: True if initialization succeeded, False otherwise
        """
        pass
    
    def shutdown(self) -> bool:
        """
        Gracefully shutdown the module
        
        Returns:
            bool: True if shutdown succeeded, False otherwise
        """
        return True
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get module metadata
        
        Returns:
            Dict: Module metadata including:
                - name: str
                - version: str
                - description: str
        """
        return {
            "name": self.get_name(),
            "version": "0.1.0",
            "description": f"{self.get_name()} module"
        }


class ServiceInterface(ABC):
    """
    Base interface for service layer operations
    
    Services contain business logic and should not depend on
    API layer or directly on other modules.
    """
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data according to service logic
        
        Args:
            data: Input data to process
            
        Returns:
            Dict: Processed result
        """
        pass
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data
        
        Args:
            data: Data to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        return True
