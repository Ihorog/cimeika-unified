"""
Malya module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/malya", tags=["malya"])


@router.get("/")
async def get_malya_status():
    """Get Malya module status"""
    return {
        "module": "malya",
        "name": "Маля",
        "description": "Ідеї, творчість, інновації",
        "status": "active"
    }
