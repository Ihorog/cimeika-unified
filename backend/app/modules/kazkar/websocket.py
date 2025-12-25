"""
WebSocket manager for Kazkar real-time updates
Handles WebSocket connections and broadcasts events to connected clients
"""
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class KazkarWebSocketManager:
    """Manages WebSocket connections for Kazkar module"""
    
    def __init__(self):
        # Store active connections
        self.active_connections: Set[WebSocket] = set()
        
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"New WebSocket connection. Total: {len(self.active_connections)}")
        
        # Send initial connection confirmation
        await websocket.send_json({
            "event": "connected",
            "timestamp": int(datetime.now().timestamp()),
            "message": "Connected to Kazkar real-time updates"
        })
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, event: Dict):
        """
        Broadcast an event to all connected clients
        
        Args:
            event: Dictionary containing event data
        """
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return
        
        # Add timestamp if not present
        if "timestamp" not in event:
            event["timestamp"] = int(datetime.now().timestamp())
        
        logger.info(f"Broadcasting event to {len(self.active_connections)} clients: {event.get('event', 'unknown')}")
        
        # Send to all connections
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(event)
            except Exception as e:
                logger.error(f"Error sending to client: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_to(self, websocket: WebSocket, event: Dict):
        """
        Send an event to a specific client
        
        Args:
            websocket: The WebSocket connection
            event: Dictionary containing event data
        """
        if "timestamp" not in event:
            event["timestamp"] = int(datetime.now().timestamp())
        
        try:
            await websocket.send_json(event)
        except Exception as e:
            logger.error(f"Error sending to specific client: {e}")
            self.disconnect(websocket)


# Global WebSocket manager instance
kazkar_ws_manager = KazkarWebSocketManager()


async def broadcast_legend_event(event_type: str, legend_id: int = None, sense: str = None, data: Dict = None):
    """
    Helper function to broadcast legend-related events
    
    Args:
        event_type: Type of event (e.g., 'legend_sense_activated', 'legend_updated')
        legend_id: ID of the legend involved
        sense: Sense that was activated (if applicable)
        data: Additional event data
    """
    event = {
        "event": event_type,
        "legend_id": legend_id,
        "sense": sense,
        "data": data or {}
    }
    
    await kazkar_ws_manager.broadcast(event)
