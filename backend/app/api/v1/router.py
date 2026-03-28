"""
API v1 Main Router
Aggregates all module routes
"""
from fastapi import APIRouter
from typing import Dict, Any
from app.modules.ci import api as ci_api
from app.modules.kazkar import api as kazkar_api
from app.modules.podija import api as podija_api
from app.modules.nastrij import api as nastrij_api
from app.modules.malya import api as malya_api
from app.modules.gallery import api as gallery_api
from app.modules.calendar import api as calendar_api
from app.api import modules as modules_api
from app.api.v1 import abilities
from app.api.v1 import agent as agent_api
from app.core.config import settings
from app.core.metrics import get_full_metrics

# Create main API router
api_router = APIRouter()

# Include core orchestration router
api_router.include_router(modules_api.router, tags=["core"])

# Include module routers (they already have their own prefixes)
api_router.include_router(ci_api.router, tags=["ci"])
api_router.include_router(kazkar_api.router, tags=["kazkar"])
api_router.include_router(podija_api.router, tags=["podiya"])
api_router.include_router(nastrij_api.router, tags=["nastrij"])
api_router.include_router(malya_api.router, tags=["malya"])
api_router.include_router(gallery_api.router, tags=["gallery"])
api_router.include_router(calendar_api.router, tags=["calendar"])

# Include abilities router
api_router.include_router(abilities.router, tags=["abilities"])

# Include agent router
api_router.include_router(agent_api.router, tags=["ci-agent"])


@api_router.get("/health", tags=["system"])
async def v1_health() -> Dict[str, Any]:
    """API v1 health check"""
    return {"status": "ok", "version": settings.API_VERSION}


@api_router.get("/status", tags=["system"])
async def v1_status() -> Dict[str, Any]:
    """API v1 system status"""
    metrics = get_full_metrics()
    return {
        "status": "running",
        "version": settings.API_VERSION,
        **metrics,
    }
