"""
Malya module service
Business logic for Malya (Ideas/Creativity) module
"""
from datetime import datetime
from typing import List
from ..models.malya_models import MalyaIdea, CreateIdeaRequest, IdeasResponse
import uuid


class MalyaService:
    """Service for Malya module"""

    def __init__(self):
        # In-memory storage (stub)
        self.ideas: List[MalyaIdea] = []

    def get_ideas(self) -> IdeasResponse:
        """Get all ideas"""
        return IdeasResponse(
            ideas=self.ideas,
            count=len(self.ideas)
        )

    def create_idea(self, request: CreateIdeaRequest) -> MalyaIdea:
        """Create a new idea"""
        now = datetime.utcnow().isoformat()
        idea = MalyaIdea(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            category=request.category or "creative",
            status="draft",
            priority=request.priority or "medium",
            tags=request.tags,
            created_at=now,
            updated_at=now,
            related_modules=[]
        )
        self.ideas.append(idea)
        return idea

    def get_idea(self, idea_id: str) -> MalyaIdea:
        """Get idea by ID"""
        for idea in self.ideas:
            if idea.id == idea_id:
                return idea
        raise ValueError(f"Idea {idea_id} not found")

    def update_idea(self, idea_id: str, updates: dict) -> MalyaIdea:
        """Update an idea"""
        for i, idea in enumerate(self.ideas):
            if idea.id == idea_id:
                updates['updated_at'] = datetime.utcnow().isoformat()
                updated_idea = idea.copy(update=updates)
                self.ideas[i] = updated_idea
                return updated_idea
        raise ValueError(f"Idea {idea_id} not found")

    def delete_idea(self, idea_id: str) -> None:
        """Delete an idea"""
        self.ideas = [i for i in self.ideas if i.id != idea_id]


# Singleton instance
malya_service = MalyaService()
