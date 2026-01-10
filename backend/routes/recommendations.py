"""
Smart Advertisement Recommendation Engine
Scores and ranks advertisements based on user profile, interests, behavior, life events, and government search intent
"""


from flask import Blueprint, request, jsonify, current_app
from functools import wraps
import jwt
from datetime import datetime
from bson import ObjectId


# Create blueprint
recommendations_bp = Blueprint('recommendations', __name__)


# Import models
from models.advertisement import Advertisement
from models.user_profile import UserProfile
from models.user_activity import UserActivity
from models.ad_click import AdClick
from models.user import User
# Import search analyzer for intent detection
from utils.search_analyzer import SearchAnalyzer


# ========================================
# AUTHENTICATION DECORATOR
# ========================================


def token_required(f):
    """Decorator to require JWT token for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'success': False, 'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is missing'}), 401
        
        try:
            # Decode token
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
            
            # Add user_id to kwargs
            kwargs['current_user_id'] = current_user_id
            
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


# ========================================
# RECOMMENDATION SCORING ENGINE
# ========================================


class RecommendationEngine:
    """
    Smart recommendation engine that scores advertisements based on multiple factors
    """
    
    def __init__(self, db):
        self.ad_model = Advertisement(db)
        self.profile_model = UserProfile(db)
        self.activity_model = UserActivity(db)
        self.user_model = User(db)
        self.db = db
    
    def get_recommendations(self, user_id, limit=5):
        """Get personalized ad recommendations with government search intent matching"""
        user = self.user_model.find_by_id(user_id)
        if not user:
            return []
        
        user_profile = self.profile_model.create_or_get(user_id)
        
        analyzer = SearchAnalyzer(self.db)
        user_profile_type = analyzer._determine_user_profile_type(user)
        
        all_products = list(self.db.products.find({'is_active': {'$ne': False}}))
        
        if not all_products:
            all_ads = self.ad_model.get_all_active(limit=50)
            all_products = all_ads
        
        # Get user's recent searches and extract keywords (including ALL searches, not just government)
        patterns = analyzer.get_user_search_patterns(user_id, days=30)
        all_recent_searches = patterns.get('recent_searches', [])
        search_keywords = set()
        
        # Extract keywords from all recent searches (not just government ones)
        for search in all_recent_searches[:3]:  # Last 3 searches ONLY - focus on most recent
            query = search.get('query', '').lower()
            search_keywords.update(query.split())
        
        # Also directly detect key terms for common government services
        key_terms = {
            'passport': ['passport', 'visa', 'travel', 'immigration', 'emigration'],
            'driving': ['driving', 'license', 'licence', 'motor', 'vehicle', 'car'],
            'education': ['o/l', 'a/l', 'results', 'exam', 'education', 'tuition', 'school', 'university'],
            'birth': ['birth', 'certificate', 'baby', 'newborn'],
            'marriage': ['marriage', 'wedding', 'spouse'],
            'property': ['land', 'property', 'deed', 'house', 'apartment'],
            'health': ['health', 'medical', 'hospital', 'doctor'],
            'job': ['job', 'employment', 'career', 'vacancy'],
        }
        
        # Check if any key terms are in recent searches
        detected_categories = set()
        for category, terms in key_terms.items():
            for term in terms:
                if term in search_keywords:
                    detected_categories.add(category)
                    break
        
        print(f"DEBUG: User {user_id} search keywords: {search_keywords}")
        print(f"DEBUG: Detected categories: {detected_categories}")
        
        scored_products = []
        
        for product in all_products:
            try:
                score = 50  # Base score
                
                # Bonus for matching job (10 points - REDUCED)
                if user.get('job', '').lower() in str(product.get('target_jobs', [])).lower():
                    score += 10
                
                # ENHANCED: Match specific government searches with product services
                product_gov_services = product.get('related_government_services', [])
                matched_services = 0
                
                # Check if product matches any detected category from search keywords
                if detected_categories and product_gov_services:
                    for category in detected_categories:
                        for service in product_gov_services:
                            if category in service.lower():
                                score += 100  # HUGE bonus for matching detected category!
                                matched_services += 1
                                break
                
                # Also check direct keyword matching
                if search_keywords and product_gov_services:
                    # Check if any search keyword matches any product service
                    for keyword in search_keywords:
                        for service in product_gov_services:
                            service_lower = service.lower()
                            # Direct match or partial match
                            if keyword in service_lower or service_lower in keyword:
                                score += 80  # BIG bonus for matching government service!
                                matched_services += 1
                                break
                
                # Also check inferred needs (25 points per matching need)
                all_inferred_needs = patterns.get('inferred_needs', [])
                product_solves_needs = product.get('solves_user_needs', [])
                
                if all_inferred_needs and product_solves_needs:
                    matching_needs = set(all_inferred_needs) & set(product_solves_needs)
                    if matching_needs:
                        score += 25 * len(matching_needs)
                
                product['relevance_score'] = score
                product['score_breakdown'] = {
                    'total': score,
                    'matched_services': matched_services,
                    'base': 50,
                    'job_match': 10 if user.get('job', '').lower() in str(product.get('target_jobs', [])).lower() else 0
                }
                
                if score > 40:
                    scored_products.append(product)
                
                # Debug logging for passport products
                if 'passport' in str(product_gov_services).lower():
                    print(f"DEBUG: Passport product '{product.get('title')}' scored {score} (matched: {matched_services})")
                
            except Exception as e:
                print(f"Error scoring product: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        print(f"DEBUG: Top 3 products: {[(p.get('title'), p['relevance_score']) for p in scored_products[:3]]}")
        
        return scored_products[:limit]


# ========================================
# API ENDPOINTS
# ========================================


@recommendations_bp.route('/recommendations', methods=['GET'])
@token_required
def get_personalized_ads(current_user_id):
    """Get personalized recommendations"""
    try:
        db = current_app.db
        limit = request.args.get('limit', 5, type=int)
        limit = min(limit, 10)
        
        engine = RecommendationEngine(db)
        recommendations = engine.get_recommendations(current_user_id, limit)
        
        for recommendation in recommendations:
            if '_id' in recommendation:
                recommendation['_id'] = str(recommendation['_id'])
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'count': len(recommendations),
            'message': f'Found {len(recommendations)} personalized recommendations'
        }), 200
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': 'Failed to get recommendations',
            'details': str(e)
        }), 500


@recommendations_bp.route('/ads/click', methods=['POST'])
@token_required
def track_ad_click(current_user_id):
    """Track ad click"""
    try:
        db = current_app.db
        data = request.get_json()
        
        ad_id = data.get('ad_id')
        if not ad_id:
            return jsonify({'success': False, 'error': 'ad_id is required'}), 400
        
        return jsonify({'success': True, 'message': 'Click tracked'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
