"""
Calendar module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/")
async def get_calendar_status():
    """Get Calendar module status"""
    return {
        "module": "calendar",
        "name": "Календар",
        "description": "Час, ритми, планування",
        "status": "active"
    }
