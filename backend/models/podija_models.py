"""
Podija module models
Data Transfer Objects for Podija (Events) module
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TimelineNode(BaseModel):
    """Timeline node model"""
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    timestamp: str  # ISO 8601 datetime
    type: str = Field(default="future")  # past, present, future
    category: str = Field(default="event")  # event, milestone, scenario
    status: str = Field(default="planned")  # planned, in_progress, completed, cancelled
    tags: Optional[List[str]] = None
    related_nodes: Optional[List[str]] = None


class CreateTimelineNodeRequest(BaseModel):
    """Request to create a timeline node"""
    title: str
    description: Optional[str] = None
    timestamp: str
    type: str = Field(default="future")
    category: Optional[str] = "event"
    tags: Optional[List[str]] = None


class TimelineResponse(BaseModel):
    """Response with timeline nodes"""
    timeline: List[TimelineNode]
    count: int
