"""
Podija module API routes
URL prefix: /podiya  (code name: podiya / podija)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.podija.schema import (
    PodijaEventSchema,
    PodijaEventCreate,
    PodijaEventUpdate
)
from app.modules.podija.service import PodijaService

router = APIRouter(prefix="/podiya", tags=["podiya"])
service = PodijaService()
service.initialize()


@router.get("/")
async def get_podija_status():
    """Get ПоДія module status"""
    return {
        "module": "podiya",
        "name": "ПоДія",
        "description": "Події, майбутнє, сценарії",
        "status": "active"
    }


@router.post("/events", response_model=PodijaEventSchema, status_code=201)
async def create_event(event: PodijaEventCreate, db: Session = Depends(get_db)):
    """Create a new ПоДія event"""
    return service.create_event(db, event)


@router.get("/events", response_model=List[PodijaEventSchema])
async def list_events(
    range: Optional[str] = Query(
        default=None,
        description="Date range filter: 'today' or 'week'"
    ),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get ПоДія events. Use ?range=today or ?range=week to filter by date."""
    if range is not None:
        return service.get_events_by_range(db, range)
    return service.get_events(db, skip=skip, limit=limit)


@router.get("/events/{event_id}", response_model=PodijaEventSchema)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a ПоДія event by ID"""
    event = service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ПоДія not found")
    return event


@router.patch("/events/{event_id}", response_model=PodijaEventSchema)
async def update_event(event_id: int, event: PodijaEventUpdate, db: Session = Depends(get_db)):
    """Partially update a ПоДія event"""
    updated_event = service.update_event(db, event_id, event)
    if not updated_event:
        raise HTTPException(status_code=404, detail="ПоДія not found")
    return updated_event


@router.post("/events/{event_id}/done", response_model=PodijaEventSchema)
async def mark_event_done(event_id: int, db: Session = Depends(get_db)):
    """Mark a ПоДія event as done"""
    event = service.mark_done(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ПоДія not found")
    return event


@router.post("/events/{event_id}/cancel", response_model=PodijaEventSchema)
async def cancel_event(event_id: int, db: Session = Depends(get_db)):
    """Cancel a ПоДія event"""
    event = service.mark_cancelled(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="ПоДія not found")
    return event


@router.delete("/events/{event_id}")
async def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete a ПоДія event"""
    success = service.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="ПоДія not found")
    return {"message": "ПоДія deleted successfully"}

