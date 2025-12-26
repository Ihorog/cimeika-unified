"""
Status endpoint for CIMEIKA API
Provides comprehensive system status and metrics
"""
from fastapi import APIRouter, status
from typing import Dict, Any

from app.core.config import settings
from app.core.metrics import get_full_metrics
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["status"])


@router.get("/api/status", status_code=status.HTTP_200_OK)
async def get_status() -> Dict[str, Any]:
    """
    System status endpoint with comprehensive metrics
    
    Returns:
        dict: Complete system status including:
            - Active persona and count
            - Deployment info
            - Version
            - Interaction count
            - Uptime
            - Timezone info
            - Participant API status
            - Request/error rates
    """
    # Get metrics from metrics module
    metrics = get_full_metrics()
    
    # Build comprehensive status response
    response = {
        "active_persona": "ci",
        "активні_персони": 5,  # Ci, Kazkar, Podija, Nastrij, Malya (core active personas)
        "розгортання": "HuggingFace / Docker",
        "статус": "running",
        "версія": settings.API_VERSION,
        **metrics  # Add all metrics (interaction count, uptime, times, participant API, etc.)
    }
    
    logger.debug(f"Status endpoint called: uptime={metrics['uptime']}, interactions={metrics['загальна_кількість_взаємодій']}")
    
    return response
