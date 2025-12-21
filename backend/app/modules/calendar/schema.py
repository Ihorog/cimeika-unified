"""
Calendar module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class CalendarEntryBase(BaseModel):
    """Base schema for Calendar entry"""
    title: str
    description: Optional[str] = None
    scheduled_at: datetime
    end_time: Optional[datetime] = None
    entry_type: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[dict] = None
    location: Optional[str] = None
    participants: Optional[List[str]] = None
    reminder_settings: Optional[dict] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class CalendarEntryCreate(CalendarEntryBase):
    """Schema for creating Calendar entry"""
    pass


class CalendarEntryUpdate(BaseModel):
    """Schema for updating Calendar entry"""
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    end_time: Optional[datetime] = None
    entry_type: Optional[str] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[dict] = None
    location: Optional[str] = None
    participants: Optional[List[str]] = None
    reminder_settings: Optional[dict] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class CalendarEntrySchema(CalendarEntryBase):
    """Complete schema for Calendar entry"""
    id: int
    module: str = 'calendar'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

