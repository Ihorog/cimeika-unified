"""
Base Pydantic schemas for Cimeika entities
Defines the minimal entity contract according to UI specification
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class BaseEntitySchema(BaseModel):
    """
    Base entity schema implementing minimal contract for Cimeika entities
    
    Required fields according to UI specification:
    - id: unique identifier
    - module: module name
    - time: timestamp
    - tags: list of tags
    - source_trace: source tracking information
    - canon_bundle_id: canonical bundle identifier
    """
    id: int
    module: str
    time: datetime = Field(default_factory=datetime.utcnow)
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)


class BaseEntityCreateSchema(BaseModel):
    """Base schema for creating entities"""
    module: str
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)


class EntityStatusSchema(BaseModel):
    """
    Schema for entity audit status
    Minimal implementation without simulation of full audit system
    """
    status: str = Field(default="draft", description="Entity status: draft or confirmed")
    
    model_config = ConfigDict(from_attributes=True)
