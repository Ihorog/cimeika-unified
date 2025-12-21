"""
Nastrij module service
Business logic for Nastrij (Mood/Emotions) module
"""
from datetime import datetime
from typing import List
from ..models.nastrij_models import (
    MoodEntry, CreateMoodEntryRequest, MoodAnalytics,
    NastrijState, MoodHistoryResponse
)
import uuid


class NastrijService:
    """Service for Nastrij module"""

    def __init__(self):
        # In-memory storage (stub)
        self.mood_entries: List[MoodEntry] = []

    def get_state(self) -> NastrijState:
        """Get current Nastrij state"""
        current_mood = self.mood_entries[-1] if self.mood_entries else None
        return NastrijState(
            status="ready",
            current_mood=current_mood,
            mood_history=self.mood_entries
        )

    def get_mood_history(self) -> MoodHistoryResponse:
        """Get mood history"""
        return MoodHistoryResponse(
            history=self.mood_entries,
            count=len(self.mood_entries)
        )

    def create_mood_entry(self, request: CreateMoodEntryRequest) -> MoodEntry:
        """Create a new mood entry"""
        entry = MoodEntry(
            id=str(uuid.uuid4()),
            mood=request.mood,
            intensity=request.intensity,
            notes=request.notes,
            timestamp=datetime.utcnow().isoformat(),
            tags=request.tags,
            context={}
        )
        self.mood_entries.append(entry)
        return entry

    def get_analytics(self) -> MoodAnalytics:
        """Get mood analytics (stub)"""
        if not self.mood_entries:
            return MoodAnalytics(
                average_intensity=0.0,
                most_common_mood="neutral",
                mood_distribution={},
                trend="stable"
            )

        avg_intensity = sum(e.intensity for e in self.mood_entries) / len(self.mood_entries)
        mood_counts = {}
        for entry in self.mood_entries:
            mood_counts[entry.mood] = mood_counts.get(entry.mood, 0) + 1

        most_common = max(mood_counts, key=mood_counts.get) if mood_counts else "neutral"

        return MoodAnalytics(
            average_intensity=avg_intensity,
            most_common_mood=most_common,
            mood_distribution=mood_counts,
            trend="stable"
        )


# Singleton instance
nastrij_service = NastrijService()
