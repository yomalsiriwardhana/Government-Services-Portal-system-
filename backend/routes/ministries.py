from flask import Blueprint, request, jsonify, current_app
from models.ministry import Ministry
from routes.auth import token_required

bp = Blueprint('ministries', __name__)

@bp.route('/', methods=['GET'])
def get_all_ministries():
    """Get all ministries"""
    try:
        ministry_model = Ministry(current_app.db)
        ministries = ministry_model.get_all_ministries_with_counts()
        
        return jsonify({
            'ministries': ministries,
            'count': len(ministries)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<ministry_id>', methods=['GET'])
def get_ministry(ministry_id):
    """Get a specific ministry by ID"""
    try:
        ministry_model = Ministry(current_app.db)
        ministry = ministry_model.find_by_id(ministry_id)
        
        if not ministry:
            return jsonify({'error': 'Ministry not found'}), 404
        
        # Increment view count
        ministry_model.increment_view_count(ministry_id)
        
        return jsonify({
            'ministry': ministry
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<ministry_id>/subservices', methods=['GET'])
def get_ministry_subservices(ministry_id):
    """Get all subservices for a ministry"""
    try:
        ministry_model = Ministry(current_app.db)
        
        # Verify ministry exists
        ministry = ministry_model.find_by_id(ministry_id)
        if not ministry:
            return jsonify({'error': 'Ministry not found'}), 404
        
        subservices = ministry_model.find_subservices_by_ministry(ministry_id)
        
        return jsonify({
            'ministry': ministry,
            'subservices': subservices,
            'count': len(subservices)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<ministry_id>/complete', methods=['GET'])
def get_ministry_complete(ministry_id):
    """Get ministry with all its subservices"""
    try:
        ministry_model = Ministry(current_app.db)
        ministry_with_subservices = ministry_model.get_ministry_with_subservices(ministry_id)
        
        if not ministry_with_subservices:
            return jsonify({'error': 'Ministry not found'}), 404
        
        # Increment view count
        ministry_model.increment_view_count(ministry_id)
        
        return jsonify({
            'ministry': ministry_with_subservices
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/search', methods=['GET'])
def search_ministries():
    """Search ministries by text"""
    try:
        query = request.args.get('q', '')
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Search query too short'}), 400
        
        ministry_model = Ministry(current_app.db)
        ministries = ministry_model.search(query)
        
        return jsonify({
            'query': query,
            'ministries': ministries,
            'count': len(ministries)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/subservices/<subservice_id>', methods=['GET'])
def get_subservice(subservice_id):
    """Get a specific subservice by ID"""
    try:
        ministry_model = Ministry(current_app.db)
        subservice = ministry_model.find_subservice_by_id(subservice_id)
        
        if not subservice:
            return jsonify({'error': 'Subservice not found'}), 404
        
        # Increment view count
        ministry_model.increment_subservice_view_count(subservice_id)
        
        # Get parent ministry info
        ministry = ministry_model.find_by_id(subservice['ministry_id'])
        if ministry:
            subservice['ministry_name'] = ministry['name']
        
        return jsonify({
            'subservice': subservice
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/subservices/search', methods=['GET'])
def search_subservices():
    """Search subservices by text"""
    try:
        query = request.args.get('q', '')
        ministry_id = request.args.get('ministry_id')
        
        if not query or len(query) < 2:
            return jsonify({'error': 'Search query too short'}), 400
        
        ministry_model = Ministry(current_app.db)
        subservices = ministry_model.search_subservices(query, ministry_id)
        
        # Enrich with ministry names
        for subservice in subservices:
            ministry = ministry_model.find_by_id(subservice['ministry_id'])
            if ministry:
                subservice['ministry_name'] = ministry['name']
        
        return jsonify({
            'query': query,
            'subservices': subservices,
            'count': len(subservices)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/create', methods=['POST'])
@token_required
def create_ministry(current_user):
    """Create a new ministry (admin only)"""
    try:
        # Check if user is admin
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Unauthorized - Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        ministry_model = Ministry(current_app.db)
        ministry_id = ministry_model.create(data)
        
        return jsonify({
            'message': 'Ministry created successfully',
            'ministry_id': ministry_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<ministry_id>/subservices/create', methods=['POST'])
@token_required
def create_subservice(current_user, ministry_id):
    """Create a new subservice (admin only)"""
    try:
        # Check if user is admin
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Unauthorized - Admin access required'}), 403
        
        ministry_model = Ministry(current_app.db)
        
        # Verify ministry exists
        ministry = ministry_model.find_by_id(ministry_id)
        if not ministry:
            return jsonify({'error': 'Ministry not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add ministry_id to data
        data['ministry_id'] = ministry_id
        
        subservice_id = ministry_model.create_subservice(data)
        
        return jsonify({
            'message': 'Subservice created successfully',
            'subservice_id': subservice_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500