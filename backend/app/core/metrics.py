"""
Metrics tracking for CIMEIKA API
Tracks uptime, interaction counts, and rolling statistics
"""
import time
from datetime import datetime, timezone
from typing import Dict, Any
from collections import deque
from threading import Lock
from zoneinfo import ZoneInfo

# Application start time
_start_time = time.time()

# Interaction counter
_interaction_count = 0
_interaction_lock = Lock()

# Participant API tracking
_participant_last_call: datetime | None = None
_participant_lock = Lock()

# Rolling request/error tracking (last 5 minutes)
_request_timestamps = deque(maxlen=1000)  # Keep last 1000 requests
_error_timestamps = deque(maxlen=1000)    # Keep last 1000 errors
_rolling_lock = Lock()

# Kyiv timezone
KYIV_TZ = ZoneInfo("Europe/Kyiv")


def get_uptime_seconds() -> float:
    """
    Get application uptime in seconds
    
    Returns:
        float: Uptime in seconds
    """
    return time.time() - _start_time


def get_uptime_formatted() -> str:
    """
    Get formatted uptime string (HH:MM:SS)
    
    Returns:
        str: Formatted uptime
    """
    uptime_seconds = int(get_uptime_seconds())
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def increment_interaction_count() -> int:
    """
    Increment total interaction counter
    
    Returns:
        int: New interaction count
    """
    global _interaction_count
    with _interaction_lock:
        _interaction_count += 1
        return _interaction_count


def get_interaction_count() -> int:
    """
    Get total interaction count
    
    Returns:
        int: Total interactions
    """
    with _interaction_lock:
        return _interaction_count


def update_participant_last_call() -> None:
    """Update participant API last call timestamp"""
    global _participant_last_call
    with _participant_lock:
        _participant_last_call = datetime.now(timezone.utc)


def get_participant_last_call() -> str | None:
    """
    Get participant API last call timestamp
    
    Returns:
        str | None: ISO8601 timestamp or None if never called
    """
    with _participant_lock:
        if _participant_last_call is None:
            return None
        return _participant_last_call.isoformat()


def record_request() -> None:
    """Record a request timestamp for rolling statistics"""
    with _rolling_lock:
        _request_timestamps.append(time.time())


def record_error() -> None:
    """Record an error timestamp for rolling statistics"""
    with _rolling_lock:
        _error_timestamps.append(time.time())


def _count_recent(timestamps: deque, window_seconds: int) -> int:
    """
    Count timestamps within the given window
    
    Args:
        timestamps: Deque of timestamps
        window_seconds: Time window in seconds
        
    Returns:
        int: Count of timestamps within window
    """
    cutoff = time.time() - window_seconds
    return sum(1 for ts in timestamps if ts > cutoff)


def get_requests_last_5m() -> int:
    """
    Get number of requests in the last 5 minutes
    
    Returns:
        int: Request count
    """
    with _rolling_lock:
        return _count_recent(_request_timestamps, 300)  # 5 minutes = 300 seconds


def get_errors_last_5m() -> int:
    """
    Get number of errors in the last 5 minutes
    
    Returns:
        int: Error count
    """
    with _rolling_lock:
        return _count_recent(_error_timestamps, 300)


def get_kyiv_time() -> datetime:
    """
    Get current time in Europe/Kyiv timezone
    
    Returns:
        datetime: Current Kyiv time
    """
    return datetime.now(KYIV_TZ)


def get_utc_time() -> datetime:
    """
    Get current UTC time
    
    Returns:
        datetime: Current UTC time
    """
    return datetime.now(timezone.utc)


def get_full_metrics() -> Dict[str, Any]:
    """
    Get all metrics for status endpoint
    
    Returns:
        dict: Complete metrics dictionary
    """
    kyiv_time = get_kyiv_time()
    utc_time = get_utc_time()
    
    return {
        "загальна_кількість_взаємодій": get_interaction_count(),
        "uptime": get_uptime_formatted(),
        "timezone": "Europe/Kyiv",
        "utc_time": utc_time.isoformat(),
        "local_time": kyiv_time.isoformat(),
        "participant_api": {
            "enabled": True,
            "last_call_at": get_participant_last_call()
        },
        "requests_last_5m": get_requests_last_5m(),
        "errors_last_5m": get_errors_last_5m()
    }
