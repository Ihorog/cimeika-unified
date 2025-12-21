"""
Calendar module models
Data Transfer Objects for Calendar module
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class CalendarEvent(BaseModel):
    """Calendar event model"""
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    start: str  # ISO 8601 datetime
    end: str  # ISO 8601 datetime
    type: str = Field(default="event")  # event, task, reminder
    status: str = Field(default="pending")  # pending, completed, cancelled
    tags: Optional[List[str]] = None
    related_modules: Optional[List[str]] = None


class CreateEventRequest(BaseModel):
    """Request to create a calendar event"""
    title: str
    description: Optional[str] = None
    start: str
    end: str
    type: Optional[str] = "event"
    tags: Optional[List[str]] = None


class EventsResponse(BaseModel):
    """Response with list of events"""
    events: List[CalendarEvent]
    count: int
