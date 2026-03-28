"""
Agent API — FastAPI router for Ci Agent System v1
Endpoints: POST /ci/process, GET /ci/memory/snapshot, DELETE /ci/memory/session/{session_id}
"""
import logging
from fastapi import APIRouter
from pydantic import BaseModel

from app.core.ci_agent import AgentResponse, OutputStatus, ci_agent
from app.core.grok_engine import grok

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ci", tags=["ci-agent"])


class AgentRequest(BaseModel):
    input: str
    session_id: str = "default"


@router.post("/process", response_model=AgentResponse)
async def process_input(req: AgentRequest) -> AgentResponse:
    """Main agent entry point — routes input through Ci Agent pipeline."""
    try:
        return await ci_agent.process(req.input, req.session_id)
    except Exception as exc:
        logger.error("Agent /process unhandled error: %s", exc)
        return AgentResponse(
            intent="unknown",
            source="ci",
            status=OutputStatus.UNAVAILABLE,
            result=str(exc),
            marker=ci_agent.structural.get_marker("unavailable"),
            grok_backend=grok.backend_name,
        )


@router.get("/memory/snapshot")
async def memory_snapshot() -> dict:
    """Debug endpoint — returns current active session memory."""
    return ci_agent.active_memory.snapshot()


@router.delete("/memory/session/{session_id}")
async def clear_session_memory(session_id: str) -> dict:
    """Clear active memory for a session (full clear in v1)."""
    ci_agent.active_memory.clear()
    return {"cleared": True}
