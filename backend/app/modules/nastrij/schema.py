"""
Nastrij module Pydantic schemas
"""
from pydantic import BaseModel


class NastrijSchema(BaseModel):
    """Base schema for Nastrij module"""
    id: int
    mood: str
    
    class Config:
        from_attributes = True
