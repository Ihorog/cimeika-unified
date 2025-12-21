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

# Include module routers (they already have their own prefixes)
api_router.include_router(ci_api.router, tags=["ci"])
api_router.include_router(kazkar_api.router, tags=["kazkar"])
api_router.include_router(podija_api.router, tags=["podija"])
api_router.include_router(nastrij_api.router, tags=["nastrij"])
api_router.include_router(malya_api.router, tags=["malya"])
api_router.include_router(gallery_api.router, tags=["gallery"])
api_router.include_router(calendar_api.router, tags=["calendar"])
