"""
Nastrij module models
Data Transfer Objects for Nastrij (Mood/Emotions) module
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MoodEntry(BaseModel):
    """Mood entry model"""
    id: Optional[str] = None
    mood: str  # e.g., "happy", "sad", "anxious", "calm"
    intensity: int = Field(ge=1, le=10)  # 1-10 scale
    notes: Optional[str] = None
    timestamp: str  # ISO 8601 datetime
    tags: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None


class CreateMoodEntryRequest(BaseModel):
    """Request to create a mood entry"""
    mood: str
    intensity: int = Field(ge=1, le=10)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class MoodAnalytics(BaseModel):
    """Mood analytics"""
    average_intensity: float
    most_common_mood: str
    mood_distribution: Dict[str, int]
    trend: str  # improving, stable, declining


class NastrijState(BaseModel):
    """Nastrij module state"""
    status: str = Field(default="idle")
    current_mood: Optional[MoodEntry] = None
    mood_history: List[MoodEntry] = Field(default_factory=list)


class MoodHistoryResponse(BaseModel):
    """Response with mood history"""
    history: List[MoodEntry]
    count: int
