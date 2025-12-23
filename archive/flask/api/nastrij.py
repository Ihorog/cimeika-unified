"""
Nastrij module API router
REST API endpoints for Nastrij (Mood/Emotions) module
"""
from flask import Blueprint, jsonify, request
from ..services.nastrij_service import nastrij_service
from ..models.nastrij_models import CreateMoodEntryRequest

nastrij_bp = Blueprint('nastrij', __name__, url_prefix='/api/nastrij')


@nastrij_bp.route('/state', methods=['GET'])
def get_state():
    """Get Nastrij module state"""
    try:
        state = nastrij_service.get_state()
        return jsonify(state.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nastrij_bp.route('/mood-history', methods=['GET'])
def get_mood_history():
    """Get mood history"""
    try:
        response = nastrij_service.get_mood_history()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nastrij_bp.route('/mood', methods=['POST'])
def create_mood_entry():
    """Create a new mood entry"""
    try:
        data = request.get_json()
        entry_request = CreateMoodEntryRequest(**data)
        entry = nastrij_service.create_mood_entry(entry_request)
        return jsonify(entry.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nastrij_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get mood analytics"""
    try:
        analytics = nastrij_service.get_analytics()
        return jsonify(analytics.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
