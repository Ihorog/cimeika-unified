"""
Podija module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class PodijaEventBase(BaseModel):
    """Base schema for Podija event"""
    title: str
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_type: Optional[str] = None
    is_completed: bool = False
    participants: Optional[List[str]] = None
    location: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class PodijaEventCreate(PodijaEventBase):
    """Schema for creating Podija event"""
    pass


class PodijaEventUpdate(BaseModel):
    """Schema for updating Podija event"""
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_type: Optional[str] = None
    is_completed: Optional[bool] = None
    participants: Optional[List[str]] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class PodijaEventSchema(PodijaEventBase):
    """Complete schema for Podija event"""
    id: int
    module: str = 'podija'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

