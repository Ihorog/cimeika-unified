"""
Malya module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class MalyaIdeaBase(BaseModel):
    """Base schema for Malya idea"""
    title: str
    description: str
    idea_type: Optional[str] = None
    status: Optional[str] = None
    related_ideas: Optional[List[int]] = None
    resources: Optional[List[str]] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class MalyaIdeaCreate(MalyaIdeaBase):
    """Schema for creating Malya idea"""
    pass


class MalyaIdeaUpdate(BaseModel):
    """Schema for updating Malya idea"""
    title: Optional[str] = None
    description: Optional[str] = None
    idea_type: Optional[str] = None
    status: Optional[str] = None
    related_ideas: Optional[List[int]] = None
    resources: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class MalyaIdeaSchema(MalyaIdeaBase):
    """Complete schema for Malya idea"""
    id: int
    module: str = 'malya'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

