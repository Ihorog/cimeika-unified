"""
Calendar module API router
REST API endpoints for Calendar module
"""
from flask import Blueprint, jsonify, request
from ..services.calendar_service import calendar_service
from ..models.calendar_models import CreateEventRequest

calendar_bp = Blueprint('calendar', __name__, url_prefix='/api/calendar')


@calendar_bp.route('/events', methods=['GET'])
def get_events():
    """Get all calendar events"""
    try:
        response = calendar_service.get_events()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route('/events', methods=['POST'])
def create_event():
    """Create a new calendar event"""
    try:
        data = request.get_json()
        event_request = CreateEventRequest(**data)
        event = calendar_service.create_event(event_request)
        return jsonify(event.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get event by ID"""
    try:
        event = calendar_service.get_event(event_id)
        return jsonify(event.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Update an event"""
    try:
        data = request.get_json()
        event = calendar_service.update_event(event_id, data)
        return jsonify(event.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@calendar_bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete an event"""
    try:
        calendar_service.delete_event(event_id)
        return jsonify({'message': 'Event deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
