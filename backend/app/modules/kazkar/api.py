"""
Kazkar module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/kazkar", tags=["kazkar"])


@router.get("/")
async def get_kazkar_status():
    """Get Kazkar module status"""
    return {
        "module": "kazkar",
        "name": "Казкар",
        "description": "Пам'ять, історії, легенди",
        "status": "active"
    }
