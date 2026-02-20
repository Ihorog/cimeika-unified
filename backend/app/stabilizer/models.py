from pydantic import BaseModel, Field
from typing import Optional, List


class StabilizeRequest(BaseModel):
    intent: str = Field(default="", description="User intent/context")
    draft: str = Field(..., description="AI-generated draft text")
    mode: str = Field(default="normal", pattern="^(normal|smart|critical)$")


class StabilizeReport(BaseModel):
    cut_flags: List[str] = []
    trimmed_chars: int = 0
    removed_new_topics: int = 0
    policy_allowed: bool
    trace_id: str
    deterministic_score: float = Field(ge=0.0, le=1.0)


class StabilizeResponse(BaseModel):
    final: str
    report: StabilizeReport


class AxisActivateRequest(BaseModel):
    profile: str = Field(..., description="Profile name from ci_axis.yaml")
