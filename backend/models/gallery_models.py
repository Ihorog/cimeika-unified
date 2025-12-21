"""
Gallery module models
Data Transfer Objects for Gallery module
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class GalleryItem(BaseModel):
    """Gallery item model"""
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    type: str = Field(default="image")  # image, video, audio, document
    url: str
    thumbnail_url: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: str  # ISO 8601 datetime
    updated_at: str  # ISO 8601 datetime
    metadata: Optional[Dict[str, Any]] = None


class CreateGalleryItemRequest(BaseModel):
    """Request to create a gallery item"""
    title: str
    description: Optional[str] = None
    type: str = Field(default="image")
    url: str
    tags: Optional[List[str]] = None


class GalleryItemsResponse(BaseModel):
    """Response with gallery items"""
    items: List[GalleryItem]
    count: int
