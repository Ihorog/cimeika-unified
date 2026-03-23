"""
Internal service authentication for CIT control-plane.
Implements X-CI-SERVICE-TOKEN validation for service-to-service communication.
"""
import os
from fastapi import Header, HTTPException, status
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_service_token() -> str:
    """
    Get CI_SERVICE_TOKEN from environment.
    
    Returns:
        str: Service token or empty string if not configured
    """
    return os.getenv("CI_SERVICE_TOKEN", "")


async def verify_service_token(
    x_ci_service_token: str = Header(..., alias="X-CI-SERVICE-TOKEN")
) -> str:
    """
    Verify internal service authentication.
    
    Required for:
    - Control-plane endpoints (/internal/*)
    - Cross-service calls (ci-gitapi ↔ MI House Master ↔ CIT)
    
    Args:
        x_ci_service_token: Token from X-CI-SERVICE-TOKEN header
        
    Returns:
        str: Validated token
        
    Raises:
        HTTPException: 401 if missing, 403 if invalid, 500 if not configured
    """
    expected = get_service_token()
    
    if not expected:
        logger.error("CI_SERVICE_TOKEN not configured in environment")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service token not configured on server"
        )
    
    if not x_ci_service_token:
        logger.warning("Internal API request without X-CI-SERVICE-TOKEN header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-CI-SERVICE-TOKEN header required"
        )
    
    if x_ci_service_token != expected:
        logger.warning("Invalid service token attempt")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid service token"
        )
    
    logger.debug("Service token validated successfully")
    return x_ci_service_token


def is_service_token_configured() -> bool:
    """
    Check if service token is configured.
    
    Returns:
        bool: True if token is set
    """
    return bool(get_service_token())
