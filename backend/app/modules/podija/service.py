"""
Podija module service layer
Business logic goes here
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.interfaces import ModuleInterface, ServiceInterface
from app.modules.podija.model import PodijaEvent
from app.modules.podija.schema import PodijaEventCreate, PodijaEventUpdate

# Valid status transitions
STATUS_TRANSITIONS = {
    "planned": {"done", "cancelled"},
    "done": set(),
    "cancelled": set(),
}


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
        """Create a new PoDiya event and a linked calendar_entry with sync_status=pending"""
        from app.modules.calendar.model import CalendarEntry

        db_event = PodijaEvent(**event_data.model_dump())
        db.add(db_event)
        db.flush()  # Send INSERT to DB so that db_event.id is assigned before we use it below

        # Create linked calendar_entry with sync_status=pending when event has a date
        if db_event.event_date:
            calendar_entry = CalendarEntry(
                title=db_event.title,
                description=db_event.description,
                scheduled_at=db_event.event_date,
                location=db_event.location,
                source_trace=f"podija_event:{db_event.id}",
                sync_status='pending',
            )
            db.add(calendar_entry)

        db.commit()
        db.refresh(db_event)
        return db_event
    
    def get_event(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """Get an event by ID"""
        return db.query(PodijaEvent).filter(PodijaEvent.id == event_id).first()
    
    def get_events(self, db: Session, skip: int = 0, limit: int = 100) -> List[PodijaEvent]:
        """Get all events with pagination"""
        return db.query(PodijaEvent).offset(skip).limit(limit).all()
    
    def get_events_by_range(self, db: Session, range_type: str) -> List[PodijaEvent]:
        """
        Get events filtered by date range.

        Args:
            range_type: 'today' or 'week'

        Returns:
            List of PodijaEvent within the requested range
        """
        now = datetime.utcnow()
        if range_type == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif range_type == "week":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=7)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid range '{range_type}'. Use 'today' or 'week'."
            )
        return (
            db.query(PodijaEvent)
            .filter(PodijaEvent.event_date >= start, PodijaEvent.event_date < end)
            .all()
        )
    
    def update_event(self, db: Session, event_id: int, event_data: PodijaEventUpdate) -> Optional[PodijaEvent]:
        """Partially update an event (PATCH semantics)"""
        db_event = self.get_event(db, event_id)
        if not db_event:
            return None
        
        update_data = event_data.model_dump(exclude_unset=True)

        # Validate status transition if status is being updated
        if "status" in update_data:
            new_status = update_data["status"]
            current_status = db_event.status
            allowed = STATUS_TRANSITIONS.get(current_status, set())
            if new_status != current_status and new_status not in allowed:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Cannot transition from '{current_status}' to '{new_status}'."
                )

        for field, value in update_data.items():
            setattr(db_event, field, value)
        
        db.commit()
        db.refresh(db_event)
        return db_event
    
    def cancel_event(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """
        Cancel a PoDiya event (MVP: also delete linked Google Calendar event).

        Marks the event status='cancelled' and cancels any linked calendar_entry.
        """
        from app.modules.calendar.model import CalendarEntry
        from app.modules.calendar.worker import cancel_entry

        db_event = self.get_event(db, event_id)
        if not db_event:
            return None

        db_event.status = 'cancelled'

        # Cancel linked calendar entry (deletes Google event if synced)
        linked_entry = (
            db.query(CalendarEntry)
            .filter(CalendarEntry.source_trace == f"podija_event:{event_id}")
            .first()
        )
        if linked_entry:
            cancel_entry(db, linked_entry)

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

    def get_events_today(self, db: Session) -> List[PodijaEvent]:
        """Get events scheduled for today"""
        today = datetime.utcnow().date()
        start = datetime(today.year, today.month, today.day)
        end = start + timedelta(days=1)
        return (
            db.query(PodijaEvent)
            .filter(PodijaEvent.event_date >= start, PodijaEvent.event_date < end)
            .all()
        )

    def get_events_week(self, db: Session) -> List[PodijaEvent]:
        """Get events scheduled for the current week (today + 6 days)"""
        today = datetime.utcnow().date()
        start = datetime(today.year, today.month, today.day)
        end = start + timedelta(days=7)
        return (
            db.query(PodijaEvent)
            .filter(PodijaEvent.event_date >= start, PodijaEvent.event_date < end)
            .all()
        )

    def mark_done(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """Mark event as done"""
        db_event = self.get_event(db, event_id)
        if not db_event:
            return None
        allowed = STATUS_TRANSITIONS.get(db_event.status, set())
        if "done" not in allowed:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Cannot transition from '{db_event.status}' to 'done'."
            )
        db_event.status = 'done'
        db_event.is_completed = True
        db.commit()
        db.refresh(db_event)
        return db_event

    def mark_cancel(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """Mark event as cancelled"""
        db_event = self.get_event(db, event_id)
        if not db_event:
            return None
        allowed = STATUS_TRANSITIONS.get(db_event.status, set())
        if "cancelled" not in allowed:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Cannot transition from '{db_event.status}' to 'cancelled'."
            )
        db_event.status = 'cancelled'
        db.commit()
        db.refresh(db_event)
        return db_event

    # Aliases for consistent naming
    def get_today_events(self, db: Session) -> List[PodijaEvent]:
        """Alias for get_events_today"""
        return self.get_events_today(db)

    def get_week_events(self, db: Session) -> List[PodijaEvent]:
        """Alias for get_events_week"""
        return self.get_events_week(db)

    def mark_cancelled(self, db: Session, event_id: int) -> Optional[PodijaEvent]:
        """Alias for mark_cancel"""
        return self.mark_cancel(db, event_id)

