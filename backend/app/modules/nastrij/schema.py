"""
Nastrij module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict


class NastrijSchema(BaseModel):
    """Base schema for Nastrij module"""
    id: int
    mood: str
    
    model_config = ConfigDict(from_attributes=True)
