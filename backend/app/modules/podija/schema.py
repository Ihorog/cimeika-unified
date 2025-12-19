"""
Podija module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PodijaSchema(BaseModel):
    """Base schema for Podija module"""
    id: int
    title: str
    event_date: datetime
    
    model_config = ConfigDict(from_attributes=True)
