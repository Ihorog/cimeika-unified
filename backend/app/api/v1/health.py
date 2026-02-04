"""
Health check endpoints for CIMEIKA API
Provides health and readiness checks for monitoring and orchestration
"""
import os
from fastapi import APIRouter, status
from typing import Dict, Any
from sqlalchemy import text
from app.config.canon import CANON_BUNDLE_ID
from app.core.monitoring import get_monitoring_status
from app.config.database import engine

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> Dict[str, Any]:
    """
    Basic health check endpoint with database connectivity check
    
    Returns:
        dict: Health status including database and pgvector status
    """
    health_status = {
        "status": "healthy",
        "database": "disconnected",
        "pgvector": "unknown"
    }
    
    try:
        # Test database connection
        with engine.connect() as conn:
            # Test basic query
            conn.execute(text("SELECT 1"))
            health_status["database"] = "connected"
            
            # Check if pgvector extension is available
            result = conn.execute(
                text("SELECT 1 FROM pg_extension WHERE extname='vector'")
            )
            if result.fetchone():
                health_status["pgvector"] = "enabled"
            else:
                health_status["pgvector"] = "not_installed"
                
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
    
    return health_status


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
