"""
Ci module Pydantic schemas
"""
from pydantic import BaseModel, ConfigDict


class CiSchema(BaseModel):
    """Base schema for Ci module"""
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)
