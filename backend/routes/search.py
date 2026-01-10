"""
Search routes with enhanced government search intent detection
"""

from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime
from bson import ObjectId

# Create blueprint
search_bp = Blueprint('search', __name__)

# Import utilities
from utils.search_analyzer import SearchAnalyzer

# ========================================
# AUTHENTICATION DECORATOR
# ========================================

def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
            kwargs['current_user_id'] = current_user_id
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

# ========================================
# SEARCH ROUTES
# ========================================

@search_bp.route('/keyword', methods=['POST'])
@token_required
def keyword_search(current_user_id):
    """
    Keyword-based search with government intent detection
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        db = current_app.db
        
        # Initialize search analyzer
        analyzer = SearchAnalyzer(db)
        
        # Analyze the search query to detect government intent
        intent_analysis = analyzer.analyze_search_query(current_user_id, query)
        
        # Perform the actual search across services
        search_results = []
        services_collection = db.services
        
        # Search in services (case-insensitive)
        services = services_collection.find({
            '$or': [
                {'name': {'$regex': query, '$options': 'i'}},
                {'description': {'$regex': query, '$options': 'i'}},
                {'category': {'$regex': query, '$options': 'i'}}
            ]
        }).limit(20)
        
        for service in services:
            service['_id'] = str(service['_id'])
            if 'ministry_id' in service:
                service['ministry_id'] = str(service['ministry_id'])
            search_results.append(service)
        
        # Track the search with intent analysis
        search_id = analyzer.track_search(
            user_id=current_user_id,
            search_query=query,
            search_type='keyword',
            results_count=len(search_results),
            intent_analysis=intent_analysis
        )
        
        # Detect life events based on this search
        life_events = analyzer.detect_life_events(current_user_id, days=30)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': search_results,
            'results_count': len(search_results),
            'search_id': search_id,
            'intent_analysis': {
                'is_government_search': intent_analysis.get('is_government_search'),
                'search_category': intent_analysis.get('search_category'),
                'inferred_needs': intent_analysis.get('inferred_needs'),
                'confidence_score': intent_analysis.get('confidence_score'),
                'recommended_categories': intent_analysis.get('recommended_product_categories')
            },
            'detected_life_events': life_events
        })
        
    except Exception as e:
        print(f"Search error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/history', methods=['GET'])
@token_required
def get_search_history(current_user_id):
    """
    Get user's search history with intent analysis
    """
    try:
        db = current_app.db
        analyzer = SearchAnalyzer(db)
        
        # Get search patterns
        patterns = analyzer.get_user_search_patterns(current_user_id, days=30)
        
        # Format recent searches for response
        recent_searches = []
        for search in patterns.get('recent_searches', []):
            search['_id'] = str(search['_id'])
            search['user_id'] = str(search['user_id'])
            recent_searches.append(search)
        
        return jsonify({
            'success': True,
            'search_history': recent_searches,
            'statistics': {
                'total_searches': patterns.get('total_searches'),
                'government_searches': patterns.get('government_searches_count'),
                'product_searches': patterns.get('product_searches_count'),
                'inferred_needs': patterns.get('inferred_needs'),
                'category_distribution': patterns.get('category_distribution')
            }
        })
        
    except Exception as e:
        print(f"Error fetching search history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/track', methods=['POST'])
@token_required
def track_search_activity(current_user_id):
    """
    Track search activity - saves search to database for recommendation engine
    
    Request body:
        {
            "query": "passport",
            "search_type": "government_service" (optional)
        }
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        search_type = data.get('search_type', 'general')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        db = current_app.db
        analyzer = SearchAnalyzer(db)
        
        # Analyze the search query to detect government intent
        intent_analysis = analyzer.analyze_search_query(current_user_id, query)
        
        # Track the search with intent analysis
        search_id = analyzer.track_search(
            user_id=current_user_id,
            search_query=query,
            search_type=search_type,
            results_count=0,
            intent_analysis=intent_analysis
        )
        
        print(f"✅ Search tracked: '{query}' by user {current_user_id}")
        print(f"   Government search: {intent_analysis.get('is_government_search')}")
        print(f"   Category: {intent_analysis.get('search_category')}")
        
        return jsonify({
            'success': True,
            'message': 'Search tracked successfully',
            'search_id': search_id,
            'is_government_search': intent_analysis.get('is_government_search'),
            'search_category': intent_analysis.get('search_category')
        })
        
    except Exception as e:
        print(f"Error tracking search: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@search_bp.route('/intent-analysis', methods=['POST'])
@token_required
def analyze_intent(current_user_id):
    """
    Analyze search intent without performing actual search
    Useful for testing and debugging
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query is required'
            }), 400
        
        db = current_app.db
        analyzer = SearchAnalyzer(db)
        
        # Analyze the search query
        intent_analysis = analyzer.analyze_search_query(current_user_id, query)
        
        # Get user context
        user = db.users.find_one({'_id': ObjectId(current_user_id)})
        user_type = analyzer._determine_user_profile_type(user)
        
        # Get life events
        life_events = analyzer.detect_life_events(current_user_id, days=30)
        
        return jsonify({
            'success': True,
            'query': query,
            'user_profile_type': user_type,
            'intent_analysis': intent_analysis,
            'detected_life_events': life_events
        })
        
    except Exception as e:
        print(f"Error analyzing intent: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@search_bp.route('/recommendations-based-on-searches', methods=['GET'])
@token_required
def get_search_based_recommendations(current_user_id):
    """
    Get product recommendations based on user's search history
    """
    try:
        db = current_app.db
        analyzer = SearchAnalyzer(db)
        
        # Get recommended products based on searches
        products = analyzer.get_recommended_products_based_on_searches(current_user_id, limit=10)
        
        # Format products
        formatted_products = []
        for product in products:
            product['_id'] = str(product['_id'])
            formatted_products.append(product)
        
        return jsonify({
            'success': True,
            'products': formatted_products,
            'count': len(formatted_products)
        })
        
    except Exception as e:
        print(f"Error getting search-based recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500