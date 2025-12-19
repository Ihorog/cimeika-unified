"""
Nastrij module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/nastrij", tags=["nastrij"])


@router.get("/")
async def get_nastrij_status():
    """Get Nastrij module status"""
    return {
        "module": "nastrij",
        "name": "Настрій",
        "description": "Емоційні стани, контекст",
        "status": "active"
    }
