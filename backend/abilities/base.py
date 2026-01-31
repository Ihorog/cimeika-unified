"""
Base Ability Interface for CIT-ORGANISM Plugin System
Defines the abstract base class for all dormant abilities.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class Ability(ABC):
    """Base class for all dormant abilities."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique ability identifier."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Semantic version."""
        pass
    
    @abstractmethod
    async def activate(self) -> None:
        """Transition from dormant to active state."""
        pass
    
    @abstractmethod
    async def deactivate(self) -> None:
        """Return to dormant state."""
        pass
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute ability logic when active."""
        pass
    
    @property
    def is_active(self) -> bool:
        """Current activation state."""
        return getattr(self, '_active', False)
