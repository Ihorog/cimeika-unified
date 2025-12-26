"""
Monitoring integration for CIMEIKA API
Optional Sentry error tracking and performance monitoring
"""
import os
from typing import Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def init_sentry() -> Optional[object]:
    """
    Initialize Sentry SDK if SENTRY_DSN is configured
    
    Returns:
        Sentry SDK instance if initialized, None otherwise
    """
    if not settings.SENTRY_DSN:
        logger.info("Sentry monitoring not configured (SENTRY_DSN not set)")
        return None
    
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
        
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            environment=settings.ENVIRONMENT,
            release=f"cimeika-backend@{settings.API_VERSION}",
            
            # Integrations
            integrations=[
                FastApiIntegration(),
                StarletteIntegration(),
            ],
            
            # Performance monitoring
            traces_sample_rate=0.1 if settings.is_production else 1.0,
            
            # Error sampling
            sample_rate=1.0,
            
            # Options
            send_default_pii=False,  # Don't send personally identifiable information
            attach_stacktrace=True,
            max_breadcrumbs=50,
            
            # Filter out health check requests
            before_send=_before_send_filter,
        )
        
        logger.info(
            f"Sentry monitoring initialized (environment: {settings.ENVIRONMENT}, "
            f"release: cimeika-backend@{settings.API_VERSION})"
        )
        
        return sentry_sdk
        
    except ImportError:
        logger.warning(
            "Sentry SDK not installed. Install with: pip install sentry-sdk"
        )
        return None
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}", exc_info=True)
        return None


def _before_send_filter(event, hint):
    """
    Filter Sentry events before sending
    
    Args:
        event: Sentry event dict
        hint: Additional context
        
    Returns:
        Modified event or None to drop the event
    """
    # Filter out health check requests
    if event.get("request"):
        url = event["request"].get("url", "")
        if any(path in url for path in ["/health", "/ready", "/api/docs"]):
            return None
    
    # Filter out specific errors if needed
    if event.get("exception"):
        exc_info = hint.get("exc_info")
        if exc_info:
            exc_type = exc_info[0]
            # Filter out common non-critical errors
            if exc_type.__name__ in ["KeyboardInterrupt", "SystemExit"]:
                return None
    
    return event


def capture_exception(exception: Exception, **kwargs) -> Optional[str]:
    """
    Capture an exception and send to Sentry if configured
    
    Args:
        exception: Exception to capture
        **kwargs: Additional context to include
        
    Returns:
        Event ID if sent to Sentry, None otherwise
    """
    if not settings.SENTRY_DSN:
        return None
    
    try:
        import sentry_sdk
        
        # Add extra context
        if kwargs:
            with sentry_sdk.configure_scope() as scope:
                for key, value in kwargs.items():
                    scope.set_extra(key, value)
        
        event_id = sentry_sdk.capture_exception(exception)
        logger.debug(f"Exception captured by Sentry: {event_id}")
        return event_id
        
    except Exception as e:
        logger.error(f"Failed to capture exception in Sentry: {e}")
        return None


def capture_message(message: str, level: str = "info", **kwargs) -> Optional[str]:
    """
    Capture a message and send to Sentry if configured
    
    Args:
        message: Message to capture
        level: Severity level (debug, info, warning, error, fatal)
        **kwargs: Additional context to include
        
    Returns:
        Event ID if sent to Sentry, None otherwise
    """
    if not settings.SENTRY_DSN:
        return None
    
    try:
        import sentry_sdk
        
        # Add extra context
        if kwargs:
            with sentry_sdk.configure_scope() as scope:
                for key, value in kwargs.items():
                    scope.set_extra(key, value)
        
        event_id = sentry_sdk.capture_message(message, level=level)
        logger.debug(f"Message captured by Sentry: {event_id}")
        return event_id
        
    except Exception as e:
        logger.error(f"Failed to capture message in Sentry: {e}")
        return None


def is_enabled() -> bool:
    """
    Check if Sentry monitoring is enabled
    
    Returns:
        True if Sentry is configured and initialized, False otherwise
    """
    return settings.SENTRY_DSN is not None


def get_monitoring_status() -> dict:
    """
    Get current monitoring status
    
    Returns:
        Dict with monitoring configuration and status
    """
    return {
        "sentry_enabled": is_enabled(),
        "sentry_dsn_configured": settings.SENTRY_DSN is not None,
        "environment": settings.ENVIRONMENT,
        "release": f"cimeika-backend@{settings.API_VERSION}",
    }
