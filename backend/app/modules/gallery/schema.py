"""
Gallery module Pydantic schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.config.canon import CANON_BUNDLE_ID


class GalleryItemBase(BaseModel):
    """Base schema for Gallery item"""
    title: str
    description: Optional[str] = None
    media_type: str
    url: str
    thumbnail_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    metadata: Optional[dict] = None
    tags: List[str] = Field(default_factory=list)
    source_trace: Optional[str] = None


class GalleryItemCreate(GalleryItemBase):
    """Schema for creating Gallery item"""
    pass


class GalleryItemUpdate(BaseModel):
    """Schema for updating Gallery item"""
    title: Optional[str] = None
    description: Optional[str] = None
    media_type: Optional[str] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    metadata: Optional[dict] = None
    tags: Optional[List[str]] = None
    source_trace: Optional[str] = None


class GalleryItemSchema(GalleryItemBase):
    """Complete schema for Gallery item"""
    id: int
    module: str = 'gallery'
    time: datetime
    canon_bundle_id: str = CANON_BUNDLE_ID
    
    model_config = ConfigDict(from_attributes=True)

