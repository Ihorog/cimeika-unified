"""
Gallery module API router
REST API endpoints for Gallery module
"""
from flask import Blueprint, jsonify, request
from ..services.gallery_service import gallery_service
from ..models.gallery_models import CreateGalleryItemRequest

gallery_bp = Blueprint('gallery', __name__, url_prefix='/api/gallery')


@gallery_bp.route('/items', methods=['GET'])
def get_items():
    """Get all gallery items"""
    try:
        response = gallery_service.get_items()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gallery_bp.route('/items', methods=['POST'])
def create_item():
    """Create a new gallery item"""
    try:
        data = request.get_json()
        item_request = CreateGalleryItemRequest(**data)
        item = gallery_service.create_item(item_request)
        return jsonify(item.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gallery_bp.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    """Get item by ID"""
    try:
        item = gallery_service.get_item(item_id)
        return jsonify(item.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@gallery_bp.route('/items/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """Delete an item"""
    try:
        gallery_service.delete_item(item_id)
        return jsonify({'message': 'Item deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
