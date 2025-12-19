"""
Podija module Pydantic schemas
"""
from pydantic import BaseModel
from datetime import datetime


class PodijaSchema(BaseModel):
    """Base schema for Podija module"""
    id: int
    title: str
    event_date: datetime
    
    class Config:
        from_attributes = True
