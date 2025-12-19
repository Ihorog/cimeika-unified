"""
Gallery module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/gallery", tags=["gallery"])


@router.get("/")
async def get_gallery_status():
    """Get Gallery module status"""
    return {
        "module": "gallery",
        "name": "Галерея",
        "description": "Візуальний архів, медіа",
        "status": "active"
    }
