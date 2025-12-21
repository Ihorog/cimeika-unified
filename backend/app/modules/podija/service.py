"""
Podija module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.podija.model import PodijaEvent
from app.modules.podija.schema import PodijaEventCreate, PodijaEventUpdate


class PodijaService(ModuleInterface, ServiceInterface):
    """Service for Podija module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "podija"
    
    def get_name(self) -> str:
        """Get the module name"""
        return self._name
    
    def get_status(self) -> Dict[str, Any]:
        """Get module status"""
        return {
            "status": "active" if self._initialized else "inactive",
            "name": self._name,
            "initialized": self._initialized
        }
    
    def initialize(self) -> bool:
        """Initialize the Podija module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Podija module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Podija module
        
        Args:
            data: Input data to process
            
        Returns:
            Dict: Processed result
        """
        if not self._initialized:
            return {"error": "Module not initialized"}
        
        return {
            "status": "success",
            "module": self._name,
            "processed": True,
            "data": data
        }
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return isinstance(data, dict)
    
    # CRUD Operations
    def create_event(self, db: Session, event_data: PodijaEventCreate) -> PodijaEvent:
        """Create a new event"""
        db_event = PodijaEvent(**event_data.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    
    def get_event(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """Get an event by ID"""
        return db.query(PodijaEvent).filter(PodijaEvent.id == event_id).first()
    
    def get_events(self, db: Session, skip: int = 0, limit: int = 100) -> List[PodijaEvent]:
        """Get all events with pagination"""
        return db.query(PodijaEvent).offset(skip).limit(limit).all()
    
    def update_event(self, db: Session, event_id: int, event_data: PodijaEventUpdate) -> Optional[PodijaEvent]:
        """Update an event"""
        db_event = self.get_event(db, event_id)
        if not db_event:
            return None
        
        update_data = event_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_event, field, value)
        
        db.commit()
        db.refresh(db_event)
        return db_event
    
    def delete_event(self, db: Session, event_id: int) -> bool:
        """Delete an event"""
        db_event = self.get_event(db, event_id)
        if not db_event:
            return False
        
        db.delete(db_event)
        db.commit()
        return True

