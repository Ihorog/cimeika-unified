"""
Ci module Pydantic schemas
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

