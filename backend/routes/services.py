from flask import Blueprint, jsonify, request
from bson import ObjectId
from datetime import datetime

services_bp = Blueprint('services', __name__)

@services_bp.route('/', methods=['GET'])
def get_all_services():
    """Get all services"""
    try:
        from flask import current_app
        db = current_app.db
        
        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        
        # Build query
        query = {}
        if category:
            query['category'] = category
        if search:
            query['$or'] = [
                {'name': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        services = list(db.services.find(query, {'_id': 0}).sort('clicks', -1))
        
        return jsonify({
            'success': True,
            'services': services,
            'total': len(services)
        })
    except Exception as e:
        print(f"Error fetching services: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@services_bp.route('/<service_id>', methods=['GET'])
def get_service(service_id):
    """Get single service by ID with full details"""
    try:
        from flask import current_app
        db = current_app.db
        
        service = db.services.find_one({'id': service_id}, {'_id': 0})
        
        if not service:
            return jsonify({
                'success': False,
                'error': 'Service not found'
            }), 404
        
        return jsonify({
            'success': True,
            'service': service
        })
    except Exception as e:
        print(f"Error fetching service: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@services_bp.route('/popular', methods=['GET'])
def get_popular_services():
    """Get popular services"""
    try:
        from flask import current_app
        db = current_app.db
        
        # Get services marked as popular or top by clicks
        popular = list(db.services.find(
            {'popular': True},
            {'_id': 0}
        ).sort('clicks', -1).limit(6))
        
        return jsonify({
            'success': True,
            'services': popular,
            'total': len(popular)
        })
    except Exception as e:
        print(f"Error fetching popular services: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@services_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        from flask import current_app
        db = current_app.db
        
        categories = db.services.distinct('category')
        
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@services_bp.route('/<service_id>/click', methods=['POST'])
def track_service_click(service_id):
    """Track when user clicks on a service"""
    try:
        from flask import current_app
        db = current_app.db
        
        # Increment click count
        result = db.services.update_one(
            {'id': service_id},
            {'$inc': {'clicks': 1}}
        )
        
        if result.modified_count > 0:
            return jsonify({'success': True, 'message': 'Click tracked'})
        else:
            return jsonify({'success': False, 'error': 'Service not found'}), 404
            
    except Exception as e:
        print(f"Error tracking click: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Alias for compatibility
bp = services_bp