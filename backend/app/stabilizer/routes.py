import hashlib
import os
from fastapi import APIRouter, HTTPException, Header, Depends
from .models import StabilizeRequest, StabilizeResponse, StabilizeReport, AxisActivateRequest
from .axis_manager import AxisManager
from .engine import StabilizerEngine

router = APIRouter(prefix="/stabilizer", tags=["stabilizer"])
axis_manager = AxisManager()
engine = StabilizerEngine(axis_manager)


def verify_admin(x_ci_key: str = Header(None)):
    expected = os.getenv("CI_ADMIN_KEY")
    if not expected or x_ci_key != expected:
        raise HTTPException(status_code=403, detail="Admin auth required")
    return True


@router.post("/stabilize", response_model=StabilizeResponse)
async def stabilize(req: StabilizeRequest, _: bool = Depends(verify_admin)):
    trace_id = hashlib.sha256((req.intent + req.draft).encode()).hexdigest()[:16]

    final, report_data = engine.stabilize(req.intent, req.draft, req.mode)

    report = StabilizeReport(
        cut_flags=report_data["cut_flags"],
        trimmed_chars=report_data["trimmed_chars"],
        removed_new_topics=report_data["removed_new_topics"],
        policy_allowed=True,
        trace_id=trace_id,
        deterministic_score=engine.deterministic_score(final)
    )

    return StabilizeResponse(final=final, report=report)


@router.post("/axis/activate")
async def activate_axis(req: AxisActivateRequest, _: bool = Depends(verify_admin)):
    success = axis_manager.activate(req.profile)
    if not success:
        raise HTTPException(status_code=404, detail=f"Profile '{req.profile}' not found")
    return {"active_profile": axis_manager.active_profile}


@router.get("/axis/active")
async def get_active_axis():
    return {
        "profile": axis_manager.active_profile,
        "config": axis_manager.get_active()
    }
