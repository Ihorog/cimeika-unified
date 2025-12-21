"""
API v1 Main Router
Aggregates all module routes
"""
from fastapi import APIRouter
from app.modules.ci import api as ci_api
from app.modules.kazkar import api as kazkar_api
from app.modules.podija import api as podija_api
from app.modules.nastrij import api as nastrij_api
from app.modules.malya import api as malya_api
from app.modules.gallery import api as gallery_api
from app.modules.calendar import api as calendar_api

# Create main API router
api_router = APIRouter()

# Include module routers
api_router.include_router(ci_api.router, prefix="/ci", tags=["ci"])
api_router.include_router(kazkar_api.router, prefix="/kazkar", tags=["kazkar"])
api_router.include_router(podija_api.router, prefix="/podija", tags=["podija"])
api_router.include_router(nastrij_api.router, prefix="/nastrij", tags=["nastrij"])
api_router.include_router(malya_api.router, prefix="/malya", tags=["malya"])
api_router.include_router(gallery_api.router, prefix="/gallery", tags=["gallery"])
api_router.include_router(calendar_api.router, prefix="/calendar", tags=["calendar"])
