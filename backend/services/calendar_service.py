"""
Calendar module service
Business logic for Calendar module
"""
from datetime import datetime
from typing import List
from ..models.calendar_models import CalendarEvent, CreateEventRequest, EventsResponse
import uuid


class CalendarService:
    """Service for Calendar module"""

    def __init__(self):
        # In-memory storage (stub)
        self.events: List[CalendarEvent] = []

    def get_events(self) -> EventsResponse:
        """Get all calendar events"""
        return EventsResponse(
            events=self.events,
            count=len(self.events)
        )

    def create_event(self, request: CreateEventRequest) -> CalendarEvent:
        """Create a new calendar event"""
        event = CalendarEvent(
            id=str(uuid.uuid4()),
            title=request.title,
            description=request.description,
            start=request.start,
            end=request.end,
            type=request.type or "event",
            status="pending",
            tags=request.tags,
            related_modules=[]
        )
        self.events.append(event)
        return event

    def get_event(self, event_id: str) -> CalendarEvent:
        """Get event by ID"""
        for event in self.events:
            if event.id == event_id:
                return event
        raise ValueError(f"Event {event_id} not found")

    def update_event(self, event_id: str, updates: dict) -> CalendarEvent:
        """Update an event"""
        for i, event in enumerate(self.events):
            if event.id == event_id:
                updated_event = event.copy(update=updates)
                self.events[i] = updated_event
                return updated_event
        raise ValueError(f"Event {event_id} not found")

    def delete_event(self, event_id: str) -> None:
        """Delete an event"""
        self.events = [e for e in self.events if e.id != event_id]


# Singleton instance
calendar_service = CalendarService()
