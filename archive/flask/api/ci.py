"""
CI module API router
REST API endpoints for Ci module
"""
from flask import Blueprint, jsonify, request
from ..services.ci_service import ci_service
from ..models.ci_models import CiChatMessage

ci_bp = Blueprint('ci', __name__, url_prefix='/api/ci')


@ci_bp.route('/state', methods=['GET'])
def get_state():
    """Get Ci module state"""
    try:
        state = ci_service.get_state()
        return jsonify(state.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@ci_bp.route('/chat', methods=['POST'])
def chat():
    """Send chat message to Ci"""
    try:
        data = request.get_json()
        message = CiChatMessage(**data)
        response = ci_service.process_chat(message)
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
