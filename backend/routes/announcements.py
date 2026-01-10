from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from bson import ObjectId

bp = Blueprint('announcements', __name__)

@bp.route('/', methods=['GET'])
def get_announcements():
    """Get all announcements"""
    try:
        announcements = list(current_app.db.announcements.find().sort('created_at', -1))
        
        # Convert ObjectId to string
        for announcement in announcements:
            announcement['_id'] = str(announcement['_id'])
        
        return jsonify({
            'announcements': announcements,
            'count': len(announcements)
        }), 200
        
    except Exception as e:
        print(f"Error getting announcements: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<announcement_id>', methods=['GET'])
def get_announcement(announcement_id):
    """Get a specific announcement by ID"""
    try:
        announcement = current_app.db.announcements.find_one({'_id': ObjectId(announcement_id)})
        
        if not announcement:
            return jsonify({'error': 'Announcement not found'}), 404
        
        announcement['_id'] = str(announcement['_id'])
        
        return jsonify({
            'announcement': announcement
        }), 200
        
    except Exception as e:
        print(f"Error getting announcement: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_announcement():
    """Create a new announcement"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'title' not in data or not data['title']:
            return jsonify({'error': 'Title is required'}), 400
        
        if 'content' not in data or not data['content']:
            return jsonify({'error': 'Content is required'}), 400
        
        # Create announcement
        announcement_data = {
            'title': data['title'],
            'content': data['content'],
            'type': data.get('type', 'general'),
            'priority': data.get('priority', 'normal'),
            'status': data.get('status', 'active'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = current_app.db.announcements.insert_one(announcement_data)
        announcement_id = str(result.inserted_id)
        
        print(f"Announcement created successfully: {announcement_id}")
        
        return jsonify({
            'message': 'Announcement created successfully',
            'announcement_id': announcement_id
        }), 201
        
    except Exception as e:
        print(f"Error creating announcement: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/<announcement_id>', methods=['PUT'])
def update_announcement(announcement_id):
    """Update an announcement"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Check if announcement exists
        announcement = current_app.db.announcements.find_one({'_id': ObjectId(announcement_id)})
        if not announcement:
            return jsonify({'error': 'Announcement not found'}), 404
        
        # Update data
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'content' in data:
            update_data['content'] = data['content']
        if 'type' in data:
            update_data['type'] = data['type']
        if 'priority' in data:
            update_data['priority'] = data['priority']
        if 'status' in data:
            update_data['status'] = data['status']
        
        update_data['updated_at'] = datetime.utcnow()
        
        # Update in database
        current_app.db.announcements.update_one(
            {'_id': ObjectId(announcement_id)},
            {'$set': update_data}
        )
        
        print(f"Announcement updated successfully: {announcement_id}")
        
        return jsonify({
            'message': 'Announcement updated successfully'
        }), 200
        
    except Exception as e:
        print(f"Error updating announcement: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<announcement_id>', methods=['DELETE'])
def delete_announcement(announcement_id):
    """Delete an announcement"""
    try:
        # Check if announcement exists
        announcement = current_app.db.announcements.find_one({'_id': ObjectId(announcement_id)})
        if not announcement:
            return jsonify({'error': 'Announcement not found'}), 404
        
        # Delete from database
        current_app.db.announcements.delete_one({'_id': ObjectId(announcement_id)})
        
        print(f"Announcement deleted successfully: {announcement_id}")
        
        return jsonify({
            'message': 'Announcement deleted successfully'
        }), 200
        
    except Exception as e:
        print(f"Error deleting announcement: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/active', methods=['GET'])
def get_active_announcements():
    """Get only active announcements"""
    try:
        announcements = list(
            current_app.db.announcements.find({'status': 'active'})
            .sort('created_at', -1)
        )
        
        # Convert ObjectId to string
        for announcement in announcements:
            announcement['_id'] = str(announcement['_id'])
        
        return jsonify({
            'announcements': announcements,
            'count': len(announcements)
        }), 200
        
    except Exception as e:
        print(f"Error getting active announcements: {str(e)}")
        return jsonify({'error': str(e)}), 500