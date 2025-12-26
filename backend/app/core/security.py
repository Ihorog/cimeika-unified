"""
Security utilities for CIMEIKA API
API key validation and security middleware
"""
import os
from typing import Optional
from fastapi import Header, HTTPException, status
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_participant_api_key() -> Optional[str]:
    """
    Get the participant API key from environment
    
    Returns:
        str | None: API key or None if not configured
    """
    # Try multiple env var names for flexibility
    return (
        os.getenv("CIMEIKA_PARTICIPANT_KEY") or 
        os.getenv("PARTICIPANT_API_KEY") or
        None
    )


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-KEY")) -> str:
    """
    Verify API key from header
    
    Args:
        x_api_key: API key from X-API-KEY header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    expected_key = get_participant_api_key()
    
    if not expected_key:
        logger.error("Participant API key not configured in environment")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API key not configured on server"
        )
    
    if not x_api_key:
        logger.warning("API request without X-API-KEY header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="X-API-KEY header required"
        )
    
    if x_api_key != expected_key:
        logger.warning("API request with invalid X-API-KEY")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return x_api_key


def is_api_key_configured() -> bool:
    """
    Check if participant API key is configured
    
    Returns:
        bool: True if key is configured
    """
    return get_participant_api_key() is not None
