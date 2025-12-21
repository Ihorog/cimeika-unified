"""
Malya module models
Data Transfer Objects for Malya (Ideas/Creativity) module
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MalyaIdea(BaseModel):
    """Malya idea model"""
    id: Optional[str] = None
    title: str
    description: str
    category: str = Field(default="creative")  # innovation, creative, improvement, experiment
    status: str = Field(default="draft")  # draft, active, completed, archived
    priority: str = Field(default="medium")  # low, medium, high
    tags: Optional[List[str]] = None
    created_at: str  # ISO 8601 datetime
    updated_at: str  # ISO 8601 datetime
    related_modules: Optional[List[str]] = None


class CreateIdeaRequest(BaseModel):
    """Request to create an idea"""
    title: str
    description: str
    category: Optional[str] = "creative"
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = None


class IdeasResponse(BaseModel):
    """Response with ideas"""
    ideas: List[MalyaIdea]
    count: int
