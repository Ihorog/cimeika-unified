"""
Participant API for CI/CD integration
Handles analysis of CI failures and provides actionable guidance
"""
from fastapi import APIRouter, Depends, Request, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from datetime import datetime

from app.core.security import verify_api_key
from app.core.metrics import (
    increment_interaction_count,
    update_participant_last_call,
    record_request,
    record_error
)
from app.core.logging import get_logger
from app.engines.rule_engine import RuleEngine

logger = get_logger(__name__)
router = APIRouter(prefix="/api/participant", tags=["participant"])

# Initialize rule engine
rule_engine = RuleEngine()


# Request/Response Schemas
class Artifact(BaseModel):
    """Artifact with base64-encoded content"""
    name: str = Field(..., description="Artifact name (e.g., 'package.json', 'error.log')")
    content_base64: str = Field(..., description="Base64-encoded content")


class InputMetadata(BaseModel):
    """Metadata about the input source"""
    source: Literal["ci", "ci-cd", "user"] = Field(default="ci", description="Source of the request")
    repo: Optional[str] = Field(None, description="Repository name")
    run_id: Optional[str] = Field(None, description="CI run ID")
    pr: Optional[int] = Field(None, description="Pull request number")


class ParticipantInput(BaseModel):
    """Input data for participant analysis"""
    text: str = Field(..., description="Text to analyze (logs, errors, etc.)")
    artifacts: List[Artifact] = Field(default_factory=list, description="Optional artifacts")
    metadata: InputMetadata = Field(default_factory=InputMetadata, description="Request metadata")


class ParticipantRequest(BaseModel):
    """Participant message request"""
    conversation_id: str = Field(..., description="Conversation identifier")
    mode: Literal["analysis", "autofix", "logger"] = Field(
        default="analysis",
        description="Operation mode"
    )
    topic: str = Field(..., description="Topic or context of the request")
    input: ParticipantInput = Field(..., description="Input data")


class Action(BaseModel):
    """Suggested action"""
    type: Literal["suggest", "check", "patch"] = Field(..., description="Action type")
    title: str = Field(..., description="Action title")
    details: str = Field(..., description="Action details")


class ParticipantOutputs(BaseModel):
    """Participant response outputs"""
    patch_unified_diff: Optional[str] = Field(None, description="Unified diff patch (if available)")
    actions: List[Action] = Field(default_factory=list, description="Suggested actions")


class ParticipantResponse(BaseModel):
    """Participant message response"""
    participant: str = Field(default="cimeika-api", description="Participant identifier")
    message: str = Field(..., description="Response message")
    severity: Literal["info", "warn", "error"] = Field(..., description="Message severity")
    outputs: ParticipantOutputs = Field(..., description="Response outputs")


# Rate limiting storage (in-memory MVP)
_rate_limit_storage: Dict[str, List[float]] = {}
_RATE_LIMIT_WINDOW = 60  # 1 minute
_RATE_LIMIT_MAX = 30  # 30 requests per minute per key


def check_rate_limit(api_key: str) -> bool:
    """
    Check if request is within rate limit
    
    Args:
        api_key: API key making the request
        
    Returns:
        bool: True if allowed, False if rate limited
    """
    import time
    
    now = time.time()
    cutoff = now - _RATE_LIMIT_WINDOW
    
    # Clean old entries
    if api_key in _rate_limit_storage:
        _rate_limit_storage[api_key] = [
            ts for ts in _rate_limit_storage[api_key] if ts > cutoff
        ]
    else:
        _rate_limit_storage[api_key] = []
    
    # Check limit
    if len(_rate_limit_storage[api_key]) >= _RATE_LIMIT_MAX:
        return False
    
    # Add current request
    _rate_limit_storage[api_key].append(now)
    return True


# Audit log storage (in-memory MVP)
_audit_log: List[Dict[str, Any]] = []


def log_audit(path: str, status_code: int, latency_ms: float, metadata: Optional[Dict] = None):
    """
    Log audit entry (minimal, no sensitive data)
    
    Args:
        path: Request path
        status_code: Response status code
        latency_ms: Request latency in milliseconds
        metadata: Optional metadata (non-sensitive)
    """
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "path": path,
        "status_code": status_code,
        "latency_ms": latency_ms,
        "metadata": metadata or {}
    }
    _audit_log.append(entry)
    
    # Keep only last 1000 entries
    if len(_audit_log) > 1000:
        _audit_log.pop(0)


@router.post("/message", response_model=ParticipantResponse, status_code=status.HTTP_200_OK)
async def participant_message(
    request: Request,
    data: ParticipantRequest,
    api_key: str = Depends(verify_api_key)
) -> ParticipantResponse:
    """
    Participant message endpoint for CI/CD integration
    
    Analyzes CI failures and provides actionable guidance.
    Requires X-API-KEY header for authentication.
    """
    import time
    start_time = time.time()
    
    try:
        # Record request
        record_request()
        
        # Check rate limit
        if not check_rate_limit(api_key):
            record_error()
            latency_ms = (time.time() - start_time) * 1000
            log_audit(str(request.url.path), 429, latency_ms, {"reason": "rate_limit"})
            
            from fastapi import HTTPException
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Maximum 30 requests per minute."
            )
        
        # Log request (minimal)
        logger.info(
            f"Participant message received: conversation_id={data.conversation_id}, "
            f"mode={data.mode}, topic={data.topic}"
        )
        
        # Analyze using rule engine
        artifacts_list = [
            {"name": a.name, "content_base64": a.content_base64}
            for a in data.input.artifacts
        ] if data.input.artifacts else None
        
        analysis = rule_engine.analyze(
            text=data.input.text,
            mode=data.mode,
            artifacts=artifacts_list
        )
        
        # Build response
        response = ParticipantResponse(
            participant="cimeika-api",
            message=analysis["message"],
            severity=analysis["severity"],
            outputs=ParticipantOutputs(
                patch_unified_diff=analysis["outputs"]["patch_unified_diff"],
                actions=[Action(**action) for action in analysis["outputs"]["actions"]]
            )
        )
        
        # Update metrics
        increment_interaction_count()
        update_participant_last_call()
        
        # Log audit
        latency_ms = (time.time() - start_time) * 1000
        log_audit(
            str(request.url.path),
            200,
            latency_ms,
            {
                "mode": data.mode,
                "severity": response.severity,
                "actions_count": len(response.outputs.actions)
            }
        )
        
        logger.info(
            f"Participant message processed: severity={response.severity}, "
            f"actions={len(response.outputs.actions)}, latency={latency_ms:.2f}ms"
        )
        
        return response
        
    except Exception as e:
        record_error()
        latency_ms = (time.time() - start_time) * 1000
        log_audit(str(request.url.path), 500, latency_ms, {"error": str(e)[:100]})
        logger.error(f"Error processing participant message: {e}", exc_info=True)
        raise
