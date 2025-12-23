"""
Podija module API router
REST API endpoints for Podija (Events) module
"""
from flask import Blueprint, jsonify, request
from ..services.podija_service import podija_service
from ..models.podija_models import CreateTimelineNodeRequest

podija_bp = Blueprint('podija', __name__, url_prefix='/api/podija')


@podija_bp.route('/timeline', methods=['GET'])
def get_timeline():
    """Get all timeline nodes"""
    try:
        response = podija_service.get_timeline()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@podija_bp.route('/timeline', methods=['POST'])
def create_node():
    """Create a new timeline node"""
    try:
        data = request.get_json()
        node_request = CreateTimelineNodeRequest(**data)
        node = podija_service.create_node(node_request)
        return jsonify(node.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@podija_bp.route('/timeline/<node_id>', methods=['GET'])
def get_node(node_id):
    """Get node by ID"""
    try:
        node = podija_service.get_node(node_id)
        return jsonify(node.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@podija_bp.route('/timeline/<node_id>', methods=['PUT'])
def update_node(node_id):
    """Update a node"""
    try:
        data = request.get_json()
        node = podija_service.update_node(node_id, data)
        return jsonify(node.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
