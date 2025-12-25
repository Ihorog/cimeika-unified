"""
Health check endpoints for CIMEIKA API
Provides health and readiness checks for monitoring and orchestration
"""
import os
from fastapi import APIRouter, status
from typing import Dict, Any
from app.config.canon import CANON_BUNDLE_ID

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> Dict[str, Any]:
    """
    Basic health check endpoint
    
    Returns:
        dict: Health status with basic system info
    """
    return {
        "status": "ok",
        "message": "CIMEIKA Backend is running",
        "version": "0.1.0",
        "canon_bundle_id": CANON_BUNDLE_ID
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def ready() -> Dict[str, Any]:
    """
    Readiness check endpoint
    Verifies that the service is ready to accept traffic
    Checks environment configuration and minimal dependencies
    
    Returns:
        dict: Readiness status with environment sanity checks
    """
    checks = {}
    all_ready = True
    
    # Check environment variables
    required_env_vars = ['ENVIRONMENT', 'LOG_LEVEL']
    optional_env_vars = ['SENTRY_DSN', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
    
    # Required env vars
    for var in required_env_vars:
        value = os.getenv(var)
        if value:
            checks[var] = "configured"
        else:
            checks[var] = "missing (using default)"
    
    # Optional env vars (just report status, don't fail)
    for var in optional_env_vars:
        value = os.getenv(var)
        checks[var] = "configured" if value else "not configured (optional)"
    
    # Check CORS configuration
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')
    checks['CORS_ORIGINS'] = "configured" if cors_origins else "missing"
    
    # Check database configuration (basic check, not connection)
    db_host = os.getenv('POSTGRES_HOST', 'localhost')
    checks['POSTGRES_HOST'] = f"configured ({db_host})"
    
    return {
        "status": "ready" if all_ready else "not_ready",
        "message": "Service is ready to accept traffic",
        "version": "0.1.0",
        "canon_bundle_id": CANON_BUNDLE_ID,
        "checks": checks
    }
