"""
Podija module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/podija", tags=["podija"])


@router.get("/")
async def get_podija_status():
    """Get Podija module status"""
    return {
        "module": "podija",
        "name": "Подія",
        "description": "Події, майбутнє, сценарії",
        "status": "active"
    }
