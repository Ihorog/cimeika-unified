"""
Malya module API router
REST API endpoints for Malya (Ideas/Creativity) module
"""
from flask import Blueprint, jsonify, request
from ..services.malya_service import malya_service
from ..models.malya_models import CreateIdeaRequest

malya_bp = Blueprint('malya', __name__, url_prefix='/api/malya')


@malya_bp.route('/ideas', methods=['GET'])
def get_ideas():
    """Get all ideas"""
    try:
        response = malya_service.get_ideas()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@malya_bp.route('/ideas', methods=['POST'])
def create_idea():
    """Create a new idea"""
    try:
        data = request.get_json()
        idea_request = CreateIdeaRequest(**data)
        idea = malya_service.create_idea(idea_request)
        return jsonify(idea.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@malya_bp.route('/ideas/<idea_id>', methods=['GET'])
def get_idea(idea_id):
    """Get idea by ID"""
    try:
        idea = malya_service.get_idea(idea_id)
        return jsonify(idea.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@malya_bp.route('/ideas/<idea_id>', methods=['PUT'])
def update_idea(idea_id):
    """Update an idea"""
    try:
        data = request.get_json()
        idea = malya_service.update_idea(idea_id, data)
        return jsonify(idea.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@malya_bp.route('/ideas/<idea_id>', methods=['DELETE'])
def delete_idea(idea_id):
    """Delete an idea"""
    try:
        malya_service.delete_idea(idea_id)
        return jsonify({'message': 'Idea deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
