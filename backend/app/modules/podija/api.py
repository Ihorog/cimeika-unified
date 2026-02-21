"""
Podija module API routes
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.podija.schema import (
    PodijaEventSchema,
    PodijaEventCreate,
    PodijaEventUpdate
)
from app.modules.podija.service import PodijaService

router = APIRouter(prefix="/podija", tags=["podija"])
service = PodijaService()
service.initialize()


@router.get("/")
async def get_podija_status():
    """Get Podija module status"""
    return {
        "module": "podija",
        "name": "Подія",
        "description": "Події, майбутнє, сценарії",
        "status": "active"
    }


@router.post("/events", response_model=PodijaEventSchema)
async def create_event(event: PodijaEventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    return service.create_event(db, event)


@router.get("/events/today", response_model=List[PodijaEventSchema])
async def get_today_events(db: Session = Depends(get_db)):
    """Get events scheduled for today (UTC)"""
    return service.get_today_events(db)


@router.get("/events/week", response_model=List[PodijaEventSchema])
async def get_week_events(db: Session = Depends(get_db)):
    """Get events scheduled within the next 7 days (UTC)"""
    return service.get_week_events(db)


@router.get("/events", response_model=List[PodijaEventSchema])
async def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all events with pagination"""
    return service.get_events(db, skip=skip, limit=limit)


@router.get("/events/{event_id}", response_model=PodijaEventSchema)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get an event by ID"""
    event = service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/events/{event_id}", response_model=PodijaEventSchema)
async def update_event(event_id: int, event: PodijaEventUpdate, db: Session = Depends(get_db)):
    """Update an event"""
    updated_event = service.update_event(db, event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return updated_event


@router.post("/events/{event_id}/done", response_model=PodijaEventSchema)
async def mark_event_done(event_id: int, db: Session = Depends(get_db)):
    """Mark an event as done"""
    event = service.mark_done(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/events/{event_id}/cancel", response_model=PodijaEventSchema)
async def cancel_event(event_id: int, db: Session = Depends(get_db)):
    """Cancel an event"""
    event = service.mark_cancelled(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    success = service.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"message": "Event deleted successfully"}
