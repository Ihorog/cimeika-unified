"""
Malya module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict


class MalyaSchema(BaseModel):
    """Base schema for Malya module"""
    id: int
    title: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)
