from flask import Blueprint, request, jsonify, current_app
from models.product import Product
from routes.auth import token_required
from datetime import datetime
from bson import ObjectId

bp = Blueprint('products', __name__)

@bp.route('/', methods=['GET'])
def get_all_products():
    """Get all products/ads"""
    try:
        status = request.args.get('status', None)
        category = request.args.get('category', None)
        
        product_model = Product(current_app.db)
        
        if status:
            products = product_model.find_all(status=status)
        else:
            products = product_model.find_all(status=None)
        
        if category and category != 'all':
            products = [p for p in products if p.get('category') == category]
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        print(f"Error getting products: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product_model = Product(current_app.db)
        product = product_model.find_by_id(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        product['_id'] = str(product['_id'])
        
        return jsonify({
            'product': product
        }), 200
        
    except Exception as e:
        print(f"Error getting product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/', methods=['POST'])
def create_product():
    """Create a new product"""
    try:
        data = request.get_json()
        
        print(f"Product creation request: {data}")
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'price', 'category']
        for field in required_fields:
            if field not in data or data[field] == '':
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create product data
        product_data = {
            'title': data['title'],
            'description': data['description'],
            'price': float(data['price']),
            'category': data['category'],
            'location': data.get('location', ''),
            'condition': data.get('condition', 'New'),
            'seller': data.get('seller', 'Admin'),
            'contact': data.get('contact', ''),
            'image': data.get('image', None),
            'featured': data.get('featured', False),
            'status': data.get('status', 'active'),
            'target_categories': data.get('target_categories', []),
            'target_age_min': data.get('target_age_min', None),
            'target_age_max': data.get('target_age_max', None),
            'target_locations': data.get('target_locations', []),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'view_count': 0,
            'click_count': 0
        }
        
        product_model = Product(current_app.db)
        product_id = product_model.create(product_data)
        
        print(f"Product created successfully: {product_id}")
        
        return jsonify({
            'message': 'Product created successfully',
            'product_id': product_id
        }), 201
        
    except Exception as e:
        print(f"Error creating product: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        product_model = Product(current_app.db)
        
        # Check if product exists
        existing_product = product_model.find_by_id(product_id)
        if not existing_product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Update data
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'price' in data:
            update_data['price'] = float(data['price'])
        if 'category' in data:
            update_data['category'] = data['category']
        if 'location' in data:
            update_data['location'] = data['location']
        if 'condition' in data:
            update_data['condition'] = data['condition']
        if 'seller' in data:
            update_data['seller'] = data['seller']
        if 'contact' in data:
            update_data['contact'] = data['contact']
        if 'image' in data:
            update_data['image'] = data['image']
        if 'featured' in data:
            update_data['featured'] = data['featured']
        if 'status' in data:
            update_data['status'] = data['status']
        if 'target_categories' in data:
            update_data['target_categories'] = data['target_categories']
        if 'target_age_min' in data:
            update_data['target_age_min'] = data['target_age_min']
        if 'target_age_max' in data:
            update_data['target_age_max'] = data['target_age_max']
        if 'target_locations' in data:
            update_data['target_locations'] = data['target_locations']
        
        update_data['updated_at'] = datetime.utcnow()
        
        # Update in database
        success = product_model.update(product_id, update_data)
        
        if success:
            print(f"Product updated successfully: {product_id}")
            return jsonify({
                'message': 'Product updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to update product'}), 500
        
    except Exception as e:
        print(f"Error updating product: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        product_model = Product(current_app.db)
        
        # Check if product exists
        existing_product = product_model.find_by_id(product_id)
        if not existing_product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Delete product (soft delete)
        success = product_model.delete(product_id)
        
        if success:
            print(f"Product deleted successfully: {product_id}")
            return jsonify({
                'message': 'Product deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete product'}), 500
        
    except Exception as e:
        print(f"Error deleting product: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/personalized', methods=['GET'])
@token_required
def get_personalized_ads(current_user):
    """Get personalized ads for the current user"""
    try:
        limit = int(request.args.get('limit', 5))
        
        # Get user profile data
        user_categories = current_user.get('ai_categories', [])
        user_age = current_user.get('age')
        user_location = current_user.get('location')
        
        # Get personalized ads
        product_model = Product(current_app.db)
        ads = product_model.get_personalized_ads(
            user_categories=user_categories,
            user_age=user_age,
            user_location=user_location,
            limit=limit
        )
        
        # Track ad impressions
        for ad in ads:
            product_model.increment_view_count(ad['_id'])
            
            # Log impression
            impression_data = {
                'user_id': str(current_user['_id']),
                'product_id': ad['_id'],
                'type': 'ad_impression',
                'timestamp': datetime.utcnow()
            }
            current_app.db.engagements.insert_one(impression_data)
        
        return jsonify({
            'ads': ads,
            'count': len(ads),
            'user_categories': user_categories
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<product_id>/click', methods=['POST'])
@token_required
def track_ad_click(current_user, product_id):
    """Track when a user clicks on an ad"""
    try:
        product_model = Product(current_app.db)
        product = product_model.find_by_id(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Increment click count
        product_model.increment_click_count(product_id)
        
        # Update user's ad click count
        from models.user import User
        user_model = User(current_app.db)
        user_model.increment_ad_clicks(str(current_user['_id']))
        
        # Track engagement
        click_data = {
            'user_id': str(current_user['_id']),
            'product_id': product_id,
            'type': 'ad_click',
            'timestamp': datetime.utcnow(),
            'product_title': product.get('title'),
            'product_category': product.get('category')
        }
        current_app.db.engagements.insert_one(click_data)
        
        return jsonify({
            'message': 'Click tracked successfully',
            'product_link': product.get('product_link')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/category/<category>', methods=['GET'])
def get_products_by_category(category):
    """Get products by category"""
    try:
        product_model = Product(current_app.db)
        products = product_model.find_by_category(category)
        
        return jsonify({
            'category': category,
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/top-performing', methods=['GET'])
def get_top_performing():
    """Get top performing ads"""
    try:
        limit = int(request.args.get('limit', 10))
        
        product_model = Product(current_app.db)
        products = product_model.get_top_performing_ads(limit=limit)
        
        return jsonify({
            'products': products,
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500