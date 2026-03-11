"""
Calendar module API routes
Час, ритми, планування

Calendar є модулем для управління часом та плануванням.
Підтримує синхронізацію з Google Calendar та інтеграцію з іншими модулями.

Endpoints:
- GET /calendar/ - Статус модуля
- GET /calendar/entries - Список всіх календарних записів
- GET /calendar/entries/today - Записи на сьогодні
- GET /calendar/entries/week - Записи на тиждень
- POST /calendar/entries - Створити новий запис
- GET /calendar/entries/{id} - Отримати запис за ID
- PUT /calendar/entries/{id} - Оновити запис
- DELETE /calendar/entries/{id} - Видалити запис
- POST /calendar/sync - Синхронізувати з Google Calendar
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.modules.calendar.schema import (
    CalendarEntrySchema,
    CalendarEntryCreate,
    CalendarEntryUpdate
)
from app.modules.calendar.service import CalendarService

router = APIRouter(prefix="/calendar", tags=["calendar"])
service = CalendarService()
service.initialize()


@router.get("/")
async def get_calendar_status():
    """Get Calendar module status"""
    return {
        "module": "calendar",
        "name": "Календар",
        "description": "Час, ритми, планування",
        "status": "active"
    }


@router.post("/sync")
async def trigger_sync(db: Session = Depends(get_db)):
    """Trigger Google Calendar sync for pending calendar_entries"""
    from app.modules.calendar.worker import run_sync
    result = run_sync(db)
    return {"status": "ok", "synced": result["synced"], "failed": result["failed"]}


@router.post("/entries", response_model=CalendarEntrySchema)
async def create_entry(entry: CalendarEntryCreate, db: Session = Depends(get_db)):
    """Create a new calendar entry"""
    return service.create_entry(db, entry)


@router.get("/entries", response_model=List[CalendarEntrySchema])
async def list_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all calendar entries with pagination"""
    return service.get_entries(db, skip=skip, limit=limit)


@router.get("/entries/{entry_id}", response_model=CalendarEntrySchema)
async def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get a calendar entry by ID"""
    entry = service.get_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.put("/entries/{entry_id}", response_model=CalendarEntrySchema)
async def update_entry(entry_id: int, entry: CalendarEntryUpdate, db: Session = Depends(get_db)):
    """Update a calendar entry"""
    updated_entry = service.update_entry(db, entry_id, entry)
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return updated_entry


@router.delete("/entries/{entry_id}")
async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete a calendar entry"""
    success = service.delete_entry(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"message": "Entry deleted successfully"}

