"""
Calendar module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CalendarSchema(BaseModel):
    """Base schema for Calendar module"""
    id: int
    title: str
    scheduled_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
