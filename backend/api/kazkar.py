"""
Kazkar module API router
REST API endpoints for Kazkar (Memory/Stories) module
"""
from flask import Blueprint, jsonify, request
from ..services.kazkar_service import kazkar_service
from ..models.kazkar_models import CreateKazkarEntryRequest

kazkar_bp = Blueprint('kazkar', __name__, url_prefix='/api/kazkar')


@kazkar_bp.route('/library', methods=['GET'])
def get_library():
    """Get library overview"""
    try:
        library = kazkar_service.get_library()
        return jsonify(library.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kazkar_bp.route('/entries', methods=['GET'])
def get_entries():
    """Get all entries"""
    try:
        response = kazkar_service.get_entries()
        return jsonify(response.dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kazkar_bp.route('/entries', methods=['POST'])
def create_entry():
    """Create a new entry"""
    try:
        data = request.get_json()
        entry_request = CreateKazkarEntryRequest(**data)
        entry = kazkar_service.create_entry(entry_request)
        return jsonify(entry.dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kazkar_bp.route('/entries/<entry_id>', methods=['GET'])
def get_entry(entry_id):
    """Get entry by ID"""
    try:
        entry = kazkar_service.get_entry(entry_id)
        return jsonify(entry.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kazkar_bp.route('/entries/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an entry"""
    try:
        data = request.get_json()
        entry = kazkar_service.update_entry(entry_id, data)
        return jsonify(entry.dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@kazkar_bp.route('/entries/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete an entry"""
    try:
        kazkar_service.delete_entry(entry_id)
        return jsonify({'message': 'Entry deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
