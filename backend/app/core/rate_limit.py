"""
Rate limiting middleware for CIMEIKA API
Simple in-memory rate limiting per IP address
"""
import time
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.logging import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter
    
    Tracks requests per IP address and enforces rate limits
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Maximum requests per minute per IP
            requests_per_hour: Maximum requests per hour per IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        
        # Storage: {ip: [(timestamp, count_minute, count_hour), ...]}
        self.storage: Dict[str, Tuple[float, int, int]] = {}
        
        # Cleanup interval (seconds)
        self.last_cleanup = time.time()
        self.cleanup_interval = 300  # 5 minutes
    
    def _cleanup_old_entries(self) -> None:
        """Remove old entries from storage to prevent memory leak"""
        now = time.time()
        
        if now - self.last_cleanup < self.cleanup_interval:
            return
        
        # Remove entries older than 1 hour
        cutoff = now - 3600
        to_remove = [
            ip for ip, (timestamp, _, _) in self.storage.items()
            if timestamp < cutoff
        ]
        
        for ip in to_remove:
            del self.storage[ip]
        
        self.last_cleanup = now
        
        if to_remove:
            logger.debug(f"Cleaned up {len(to_remove)} old rate limit entries")
    
    def is_allowed(self, ip: str) -> Tuple[bool, str]:
        """
        Check if request from IP is allowed
        
        Args:
            ip: Client IP address
            
        Returns:
            Tuple of (allowed: bool, reason: str)
        """
        now = time.time()
        
        # Periodic cleanup
        self._cleanup_old_entries()
        
        # Get or initialize counters for this IP
        if ip not in self.storage:
            self.storage[ip] = (now, 1, 1)
            return True, "OK"
        
        last_time, count_minute, count_hour = self.storage[ip]
        
        # Calculate time windows
        minute_ago = now - 60
        hour_ago = now - 3600
        
        # Reset counters if outside time windows
        if last_time < minute_ago:
            # More than a minute passed, reset minute counter
            count_minute = 0
        
        if last_time < hour_ago:
            # More than an hour passed, reset hour counter
            count_hour = 0
        
        # Increment counters
        count_minute += 1
        count_hour += 1
        
        # Check limits
        if count_minute > self.requests_per_minute:
            logger.warning(
                f"Rate limit exceeded for IP {ip}: {count_minute} requests/minute"
            )
            return False, f"Too many requests. Limit: {self.requests_per_minute}/minute"
        
        if count_hour > self.requests_per_hour:
            logger.warning(
                f"Rate limit exceeded for IP {ip}: {count_hour} requests/hour"
            )
            return False, f"Too many requests. Limit: {self.requests_per_hour}/hour"
        
        # Update storage
        self.storage[ip] = (now, count_minute, count_hour)
        
        return True, "OK"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for rate limiting
    """
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        exclude_paths: list = None
    ):
        """
        Initialize middleware
        
        Args:
            app: FastAPI application
            requests_per_minute: Max requests per minute
            requests_per_hour: Max requests per hour
            exclude_paths: List of paths to exclude from rate limiting
        """
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute, requests_per_hour)
        self.exclude_paths = exclude_paths or ["/health", "/ready", "/api/docs", "/api/redoc"]
        
        logger.info(
            f"Rate limiting enabled: {requests_per_minute}/min, {requests_per_hour}/hour"
        )
    
    async def dispatch(self, request: Request, call_next):
        """
        Process request through rate limiter
        
        Args:
            request: Incoming request
            call_next: Next middleware/handler
            
        Returns:
            Response or rate limit error
        """
        # Skip rate limiting for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Get client IP
        # Check X-Forwarded-For header first (for proxy/load balancer)
        client_ip = request.headers.get("X-Forwarded-For")
        if client_ip:
            # X-Forwarded-For can contain multiple IPs, take the first one
            client_ip = client_ip.split(",")[0].strip()
        else:
            # Fallback to direct connection IP
            client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limit
        allowed, reason = self.limiter.is_allowed(client_ip)
        
        if not allowed:
            logger.warning(
                f"Rate limit exceeded for {client_ip} on {request.url.path}: {reason}"
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "rate_limit_exceeded",
                    "message": reason,
                    "detail": "Please try again later"
                },
                headers={
                    "Retry-After": "60"  # Suggest retry after 60 seconds
                }
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers to response
        response.headers["X-RateLimit-Limit-Minute"] = str(self.limiter.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(self.limiter.requests_per_hour)
        
        return response
