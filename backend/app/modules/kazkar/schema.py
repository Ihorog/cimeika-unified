"""
Kazkar module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict


class KazkarSchema(BaseModel):
    """Base schema for Kazkar module"""
    id: int
    title: str
    content: str
    
    model_config = ConfigDict(from_attributes=True)
