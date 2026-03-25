"""
Health check endpoints for CIMEIKA API
Provides health and readiness checks for monitoring and orchestration
"""
import os
from fastapi import APIRouter, status
from typing import Dict, Any
from app.core.config import settings
from app.core.monitoring import get_monitoring_status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> Dict[str, Any]:
    """
    Basic health check endpoint.

    Returns:
        dict: Health status with version
    """
    return {
        "status": "ok",
        "version": settings.API_VERSION,
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def ready() -> Dict[str, Any]:
    """
    Readiness check endpoint.
    Verifies that the service is ready to accept traffic.
    Validates required environment variables exist (does not print values).

    Returns:
        dict: Readiness status with dependency and monitoring checks
    """
    deps = {}
    checks = {}
    all_ready = True

    # Check required environment variables (MUST exist)
    required_env_vars = [
        'POSTGRES_HOST',
        'POSTGRES_DB',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
    ]

    env_status = "ok"
    for var in required_env_vars:
        if not os.getenv(var):
            env_status = "missing_required"
            all_ready = False
            break

    deps["env"] = env_status

    return {
        "status": "ready" if all_ready else "not_ready",
        "deps": deps,
        "checks": {
            "monitoring": get_monitoring_status(),
        },
    }
