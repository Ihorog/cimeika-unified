"""
Podija module service
Business logic for Podija (Events) module
"""
from datetime import datetime
from typing import List
from ..models.podija_models import TimelineNode, CreateTimelineNodeRequest, TimelineResponse
import uuid


class PodijaService:
    """Service for Podija module"""

    def __init__(self):
        # In-memory storage (stub)
        self.nodes: List[TimelineNode] = []

    def get_timeline(self) -> TimelineResponse:
        """Get all timeline nodes"""
        return TimelineResponse(
            timeline=self.nodes,
            count=len(self.nodes)
        )

    def create_node(self, request: CreateTimelineNodeRequest) -> TimelineNode:
        """Create a new timeline node"""
        node = TimelineNode(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            timestamp=request.timestamp,
            type=request.type,
            category=request.category or "event",
            status="planned",
            tags=request.tags,
            related_nodes=[]
        )
        self.nodes.append(node)
        return node

    def get_node(self, node_id: str) -> TimelineNode:
        """Get node by ID"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        raise ValueError(f"Node {node_id} not found")

    def update_node(self, node_id: str, updates: dict) -> TimelineNode:
        """Update a node"""
        for i, node in enumerate(self.nodes):
            if node.id == node_id:
                updated_node = node.copy(update=updates)
                self.nodes[i] = updated_node
                return updated_node
        raise ValueError(f"Node {node_id} not found")


# Singleton instance
podija_service = PodijaService()
