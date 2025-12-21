"""
Kazkar module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class KazkarStoryBase(BaseModel):
    """Base schema for Kazkar story"""
    title: str
    content: str
    story_type: Optional[str] = None
    participants: Optional[List[str]] = None
    location: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class KazkarStoryCreate(KazkarStoryBase):
    """Schema for creating Kazkar story"""
    pass


class KazkarStoryUpdate(BaseModel):
    """Schema for updating Kazkar story"""
    title: Optional[str] = None
    content: Optional[str] = None
    story_type: Optional[str] = None
    participants: Optional[List[str]] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class KazkarStorySchema(KazkarStoryBase):
    """Complete schema for Kazkar story"""
    id: int
    module: str = 'kazkar'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

