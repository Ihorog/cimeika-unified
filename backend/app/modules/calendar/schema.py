"""
Calendar module Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime


class CalendarSchema(BaseModel):
    """Base schema for Calendar module"""
    id: int
    title: str
    scheduled_at: datetime
    
    class Config:
        from_attributes = True
