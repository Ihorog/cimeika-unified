"""
Calendar module service layer
Business logic goes here
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.calendar.model import CalendarEntry
from app.modules.calendar.schema import CalendarEntryCreate, CalendarEntryUpdate


class CalendarService(ModuleInterface, ServiceInterface):
    """Service for Calendar module operations - implements core interfaces"""
    
    def __init__(self):
        self._initialized = False
        self._name = "calendar"
    
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
        """Initialize the Calendar module"""
        self._initialized = True
        return True
    
    def shutdown(self) -> bool:
        """Shutdown the Calendar module"""
        self._initialized = False
        return True
    
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process data through the Calendar module
        
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
    def create_entry(self, db: Session, entry_data: CalendarEntryCreate) -> CalendarEntry:
        """Create a new calendar entry"""
        db_entry = CalendarEntry(**entry_data.model_dump())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    
    def get_entry(self, db: Session, entry_id: int) -> Optional[CalendarEntry]:
        """Get a calendar entry by ID"""
        return db.query(CalendarEntry).filter(CalendarEntry.id == entry_id).first()
    
    def get_entries(self, db: Session, skip: int = 0, limit: int = 100) -> List[CalendarEntry]:
        """Get all calendar entries with pagination"""
        return db.query(CalendarEntry).offset(skip).limit(limit).all()
    
    def update_entry(self, db: Session, entry_id: int, entry_data: CalendarEntryUpdate) -> Optional[CalendarEntry]:
        """Update a calendar entry"""
        db_entry = self.get_entry(db, entry_id)
        if not db_entry:
            return None
        
        update_data = entry_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_entry, field, value)
        
        db.commit()
        db.refresh(db_entry)
        return db_entry
    
    def delete_entry(self, db: Session, entry_id: int) -> bool:
        """Delete a calendar entry"""
        db_entry = self.get_entry(db, entry_id)
        if not db_entry:
            return False
        
        db.delete(db_entry)
        db.commit()
        return True

