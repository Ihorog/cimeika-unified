"""
Structured logging configuration for CIMEIKA API
Provides consistent logging across all modules
"""
import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict
from app.core.config import settings


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in structured JSON format
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON
        
        Args:
            record: Log record to format
            
        Returns:
            str: JSON-formatted log entry
        """
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data["extra"] = record.extra
        
        return json.dumps(log_data)


class SimpleFormatter(logging.Formatter):
    """
    Simple human-readable formatter for development
    """
    
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


def setup_logging() -> logging.Logger:
    """
    Configure and return the root logger
    
    Returns:
        logging.Logger: Configured root logger
    """
    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Use structured logging in production, simple in development
    if settings.is_production:
        formatter = StructuredFormatter()
    else:
        formatter = SimpleFormatter()
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set specific log levels for noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


# Setup logging on module import
logger = setup_logging()


# Convenience functions for structured logging
def log_with_context(
    level: int,
    message: str,
    logger_name: str = "cimeika",
    **context: Any
) -> None:
    """
    Log a message with additional context
    
    Args:
        level: Logging level (logging.INFO, logging.ERROR, etc.)
        message: Log message
        logger_name: Logger name to use
        **context: Additional context fields to include in structured logs
    """
    log = get_logger(logger_name)
    
    if settings.is_production:
        # In production, add context to log record
        extra_data = {"extra": context}
        log.log(level, message, extra=extra_data)
    else:
        # In development, append context to message
        if context:
            context_str = " | " + " | ".join(f"{k}={v}" for k, v in context.items())
            message = message + context_str
        log.log(level, message)


def log_api_call(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    **extra: Any
) -> None:
    """
    Log an API call with standard fields
    
    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration_ms: Request duration in milliseconds
        **extra: Additional fields
    """
    log_with_context(
        logging.INFO,
        f"{method} {path} - {status_code}",
        logger_name="cimeika.api",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        **extra
    )
