"""
Ci module API routes
"""
from fastapi import APIRouter

router = APIRouter(prefix="/ci", tags=["ci"])


@router.get("/")
async def get_ci_status():
    """Get Ci module status"""
    return {
        "module": "ci",
        "name": "Ci",
        "description": "Центральне ядро, оркестрація",
        "status": "active"
    }
