"""
Ci module Pydantic schemas
CANON v1.0.0 compliant
"""
from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class CiEntityBase(BaseModel):
    """Base schema for Ci entity"""
    name: str
    description: Optional[str] = None
    context_data: Optional[dict] = None
    orchestration_state: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class CiEntityCreate(CiEntityBase):
    """Schema for creating Ci entity"""
    pass


class CiEntityUpdate(BaseModel):
    """Schema for updating Ci entity"""
    name: Optional[str] = None
    description: Optional[str] = None
    context_data: Optional[dict] = None
    orchestration_state: Optional[str] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class CiEntitySchema(CiEntityBase):
    """Complete schema for Ci entity"""
    id: int
    module: str = 'ci'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)


# CANON v1.0.0: ci.capture() schemas
class CiCaptureRequest(BaseModel):
    """
    Schema for ci.capture() - Step 0: Contact
    Accepts text, voice, or image input
    """
    type: str = Field(..., description="Input type: text, voice, or image")
    content: str = Field(..., description="The captured content")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata")


class CiCaptureResponse(BaseModel):
    """
    Schema for ci.capture() response - Step 2: Reveal
    Shows event, time_position, related_traces
    """
    event_id: str
    event: dict
    time_position: str
    related_traces: List[dict] = Field(default_factory=list)
    expand_options: List[str] = Field(
        default_factory=lambda: ["open_calendar", "open_gallery", "add_narrative", "close"]
    )

