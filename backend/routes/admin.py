from flask import Blueprint, request, jsonify, current_app
from models.user import User
from models.service import Service
from models.product import Product
from models.search_history import SearchHistory
from functools import wraps
from datetime import datetime

bp = Blueprint('admin', __name__)

# Simple admin authentication (you can enhance this later)
def admin_required(f):
    """Decorator to protect admin routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        
        # Simple admin check (username: admin, password: admin123)
        # In production, use proper authentication
        if not auth or auth.username != 'admin' or auth.password != 'admin123':
            return jsonify({'error': 'Admin authentication required'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@bp.route('/dashboard', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get admin dashboard statistics"""
    try:
        user_model = User(current_app.db)
        service_model = Service(current_app.db)
        product_model = Product(current_app.db)
        
        # User stats
        user_stats = user_model.get_user_stats()
        
        # Service stats
        total_services = current_app.db.services.count_documents({})
        popular_services = service_model.get_popular_services(limit=5)
        
        # Product stats
        total_products = current_app.db.products.count_documents({'status': 'active'})
        top_performing_ads = product_model.get_top_performing_ads(limit=5)
        
        # Engagement stats
        total_searches = current_app.db.search_history.count_documents({})
        total_ad_clicks = current_app.db.engagements.count_documents({'type': 'ad_click'})
        
        # Age distribution
        age_distribution = user_model.get_age_distribution()
        
        # Job distribution
        job_distribution = user_model.get_job_distribution()
        
        return jsonify({
            'users': user_stats,
            'services': {
                'total': total_services,
                'popular': popular_services
            },
            'products': {
                'total': total_products,
                'top_performing': top_performing_ads
            },
            'engagement': {
                'total_searches': total_searches,
                'total_ad_clicks': total_ad_clicks
            },
            'demographics': {
                'age_distribution': age_distribution,
                'job_distribution': job_distribution
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        
        user_model = User(current_app.db)
        users = user_model.get_all_users(skip=skip, limit=limit)
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/users/<user_id>', methods=['GET'])
@admin_required
def get_user_details(user_id):
    """Get detailed user information"""
    try:
        user_model = User(current_app.db)
        user = user_model.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove password
        if 'password' in user:
            del user['password']
        user['_id'] = str(user['_id'])
        
        # Get user's search history
        search_history_model = SearchHistory(current_app.db)
        search_stats = search_history_model.get_user_search_stats(user_id)
        recent_searches = search_history_model.find_by_user(user_id, limit=20)
        
        return jsonify({
            'user': user,
            'search_stats': search_stats,
            'recent_searches': recent_searches
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/products', methods=['GET'])
@admin_required
def get_all_products_admin():
    """Get all products for admin"""
    try:
        product_model = Product(current_app.db)
        products = product_model.find_all(status=None)  # Get all, including inactive
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    """Create a new product/ad"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Prepare product data
        product_data = {
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'price': float(data['price']),
            'image_url': data.get('image_url', ''),
            'product_link': data.get('product_link', ''),
            'target_categories': data.get('target_categories', []),
            'target_age_min': data.get('target_age_min'),
            'target_age_max': data.get('target_age_max'),
            'target_locations': data.get('target_locations', []),
            'status': data.get('status', 'active'),
            'featured': data.get('featured', False)
        }
        
        product_model = Product(current_app.db)
        product_id = product_model.create(product_data)
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/products/<product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update a product"""
    try:
        data = request.get_json()
        
        product_model = Product(current_app.db)
        success = product_model.update(product_id, data)
        
        if success:
            return jsonify({
                'message': 'Product updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Update failed'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/products/<product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete a product (soft delete)"""
    try:
        product_model = Product(current_app.db)
        success = product_model.delete(product_id)
        
        if success:
            return jsonify({
                'message': 'Product deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Delete failed'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/products/<product_id>/analytics', methods=['GET'])
@admin_required
def get_product_analytics(product_id):
    """Get analytics for a specific product"""
    try:
        product_model = Product(current_app.db)
        product = product_model.find_by_id(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Calculate CTR
        views = product.get('view_count', 0)
        clicks = product.get('click_count', 0)
        ctr = (clicks / views * 100) if views > 0 else 0
        
        # Get who clicked (from engagements)
        click_pipeline = [
            {
                '$match': {
                    'product_id': product_id,
                    'type': 'ad_click'
                }
            },
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user'
                }
            },
            {
                '$limit': 50
            }
        ]
        
        recent_clicks = list(current_app.db.engagements.aggregate(click_pipeline))
        
        return jsonify({
            'product': {
                '_id': str(product['_id']),
                'title': product.get('title'),
                'category': product.get('category'),
                'price': product.get('price')
            },
            'performance': {
                'views': views,
                'clicks': clicks,
                'ctr': round(ctr, 2)
            },
            'recent_clicks': len(recent_clicks)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/analytics/category-performance', methods=['GET'])
@admin_required
def get_category_performance():
    """Get performance by product category"""
    try:
        product_model = Product(current_app.db)
        performance = product_model.get_category_performance()
        
        return jsonify({
            'category_performance': performance
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/trending-searches', methods=['GET'])
@admin_required
def get_trending_searches():
    """Get trending searches"""
    try:
        days = int(request.args.get('days', 7))
        limit = int(request.args.get('limit', 10))
        
        search_history_model = SearchHistory(current_app.db)
        trending = search_history_model.get_trending_searches(days=days, limit=limit)
        popular_categories = search_history_model.get_popular_categories(days=days)
        
        return jsonify({
            'trending_searches': trending,
            'popular_categories': popular_categories
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/services', methods=['POST'])
@admin_required
def create_service():
    """Create a new service"""
    try:
        data = request.get_json()
        
        service_model = Service(current_app.db)
        service_id = service_model.create(data)
        
        return jsonify({
            'message': 'Service created successfully',
            'service_id': service_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/services/<service_id>', methods=['PUT'])
@admin_required
def update_service(service_id):
    """Update a service"""
    try:
        data = request.get_json()
        
        service_model = Service(current_app.db)
        success = service_model.update(service_id, data)
        
        if success:
            return jsonify({
                'message': 'Service updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Update failed'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/services/<service_id>', methods=['DELETE'])
@admin_required
def delete_service(service_id):
    """Delete a service"""
    try:
        service_model = Service(current_app.db)
        success = service_model.delete(service_id)
        
        if success:
            return jsonify({
                'message': 'Service deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Delete failed'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500