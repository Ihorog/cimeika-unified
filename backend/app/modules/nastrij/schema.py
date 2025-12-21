"""
Nastrij module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class NastrijEmotionBase(BaseModel):
    """Base schema for Nastrij emotion"""
    emotion_state: str
    intensity: Optional[float] = None
    context: Optional[str] = None
    triggers: Optional[List[str]] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class NastrijEmotionCreate(NastrijEmotionBase):
    """Schema for creating Nastrij emotion"""
    pass


class NastrijEmotionUpdate(BaseModel):
    """Schema for updating Nastrij emotion"""
    emotion_state: Optional[str] = None
    intensity: Optional[float] = None
    context: Optional[str] = None
    triggers: Optional[List[str]] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class NastrijEmotionSchema(NastrijEmotionBase):
    """Complete schema for Nastrij emotion"""
    id: int
    module: str = 'nastrij'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

