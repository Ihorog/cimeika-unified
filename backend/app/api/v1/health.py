"""
Health check endpoints for CIMEIKA API
Provides health and readiness checks for monitoring and orchestration
"""
import os
from fastapi import APIRouter, status
from typing import Dict, Any
from app.config.canon import CANON_BUNDLE_ID
from app.core.monitoring import get_monitoring_status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> Dict[str, Any]:
    """
    Basic health check endpoint
    
    Returns:
        dict: Simple health status
    """
    return {
        "status": "ok"
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def ready() -> Dict[str, Any]:
    """
    Readiness check endpoint
    Verifies that the service is ready to accept traffic
    Validates required environment variables exist (does not print values)
    
    Returns:
        dict: Readiness status with dependency checks
    """
    deps = {}
    all_ready = True
    
    # Check required environment variables (MUST exist)
    required_env_vars = [
        'POSTGRES_HOST',
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
    ]
    
    # Check all required vars exist
    env_status = "ok"
    for var in required_env_vars:
        value = os.getenv(var)
        if not value:
            env_status = "missing_required"
            all_ready = False
            break
    
    deps["env"] = env_status
    
    return {
        "status": "ok" if all_ready else "not_ready",
        "deps": deps
    }
