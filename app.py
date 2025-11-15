import os
from flask import Flask, jsonify, render_template, request, session, redirect, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, verify_jwt_in_request, create_access_token
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
from io import StringIO
import csv
import io
from dotenv import load_dotenv
from ai_search import perform_ai_search, initialize_search_engine
from auth import UserAuthManager
from email_service import EmailService, PremiumSuggestionService
from rate_limiting import setup_rate_limiting_and_caching
from recommendation_engine import get_recommendation_engine
from ai_categorizer import get_ai_categorizer

# Phase 1 - Step 2: Import search tracker
from search_tracker import SearchTracker

# Phase 1 - Step 3: Import ad matcher
from ad_matcher import AdMatcher

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET", "dev-secret")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET", "jwt-secret-change-this")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

CORS(app)
jwt = JWTManager(app)

# Initialize Rate Limiting and Caching
limiter, cache, smart_cache, advanced_limiter = setup_rate_limiting_and_caching(app)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]

services_col = db["services"]
eng_col = db["engagements"]
admins_col = db["admins"]
categories_col = db["categories"]
officers_col = db["officers"]
ads_col = db["ads"]
users_col = db["users"]
products_col = db["products"]
orders_col = db["orders"]
payments_col = db["payments"]

# Initialize services
auth_manager = UserAuthManager(db)
email_service = EmailService()
premium_service = PremiumSuggestionService(db, email_service)
ai_categorizer = get_ai_categorizer(db)

# Phase 1 - Step 2: Initialize search tracker
search_tracker = SearchTracker(db)

# Phase 1 - Step 3: Initialize ad matcher
ad_matcher = AdMatcher(db)

# --- Helpers ---
def admin_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*a, **kw):
        if not session.get("admin_logged_in"):
            if request.path.startswith('/api/'):
                return jsonify({"error": "unauthorized", "redirect": "/admin/login"}), 401
            return redirect("/admin/login")
        return fn(*a, **kw)
    return wrapper

# --- Public routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("user_dashboard.html")

@app.route("/profile")
def profile_page():
    return render_template("user_dashboard.html")

# Phase 1 - Step 2: Search history page route
@app.route("/search-history")
def search_history_page():
    """User's search history page"""
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('search_history.html')

# ==================== API ENDPOINTS ====================

@app.route("/api/services")
@limiter.limit("200 per hour, 50 per minute")
def get_services():
    cache_key = "services_list"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    docs = list(services_col.find({}, {"_id": 0}))
    cache.set(cache_key, docs, timeout=600)
    return jsonify(docs)

@app.route("/api/categories")
@limiter.limit("200 per hour")
def get_categories():
    """Get all categories"""
    try:
        cache_key = "categories_list"
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(cached_result)
        cats = list(categories_col.find({}, {"_id": 0}))
        if not cats:
            pipeline = [
                {"$project": {"id": 1, "name": 1, "category": 1}},
                {"$group": {"_id": "$category", "ministries": {"$push": {"id": "$id", "name": "$name"}}}}
            ]
            try:
                groups = list(services_col.aggregate(pipeline))
                cats = [
                    {
                        "id": g["_id"] or "uncategorized",
                        "name": {"en": g["_id"] or "Uncategorized"},
                        "ministry_ids": [m["id"] for m in g["ministries"]]
                    }
                    for g in groups
                ]
            except:
                cats = []
        cache.set(cache_key, cats, timeout=600)
        return jsonify(cats)
    except Exception as e:
        print(f"Error in get_categories: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/ads")
@limiter.limit("200 per hour")
def get_ads():
    """Get all ads/announcements"""
    try:
        cache_key = "ads_list"
        cached_result = cache.get(cache_key)
        if cached_result:
            return jsonify(cached_result)
        ads = list(ads_col.find({}, {"_id": 0}))
        cache.set(cache_key, ads, timeout=600)
        return jsonify(ads)
    except Exception as e:
        print(f"Error in get_ads: {e}")
        return jsonify({"error": str(e)}), 500

# Phase 1 - Step 2: UPDATED Search endpoint with tracking
@app.route('/api/search', methods=['POST'])
@limiter.limit("100 per hour")
def api_search():
    """Search for services with tracking"""
    try:
        data = request.json or {}
        query = data.get('query', '').lower().strip()
        category = data.get('category')
        user_id = session.get('user_id')
        
        # Build search query
        results = []
        if query:
            regex = {"$regex": query, "$options": "i"}
            search_filter = {
                "$or": [
                    {"name.en": regex},
                    {"description": regex},
                    {"department": regex},
                    {"subservices.name.en": regex}
                ]
            }
            
            if category:
                search_filter["category"] = category
            
            results = list(services_col.find(
                search_filter,
                {"_id": 0, "id": 1, "name": 1, "category": 1, "description": 1, "department": 1, "link": 1}
            ).limit(20))
        
        # TRACK THE SEARCH
        search_id = None
        if user_id and query:
            try:
                search_id = search_tracker.track_search(
                    user_id=user_id,
                    query=query,
                    category=category,
                    results_count=len(results),
                    session_id=session.get('session_id')
                )
                print(f"🔍 Search tracked: '{query}' by user {user_id} (Search ID: {search_id})")
            except Exception as e:
                print(f"⚠️ Search tracking error: {e}")
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'search_id': search_id
        })
        
    except Exception as e:
        print(f"Error in api_search: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Phase 1 - Step 2: Track search result clicks
@app.route('/api/search/click', methods=['POST'])
def api_search_click():
    """Track when user clicks on a search result"""
    try:
        data = request.json or {}
        search_id = data.get('search_id')
        clicked_result = data.get('clicked_result')
        
        if search_id and clicked_result:
            search_tracker.track_click(search_id, clicked_result)
            return jsonify({'success': True})
        
        return jsonify({
            'success': False,
            'message': 'Missing search_id or clicked_result'
        }), 400
        
    except Exception as e:
        print(f"Error in api_search_click: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Phase 1 - Step 2: Get user's search history
@app.route('/api/user/search-history', methods=['GET'])
def api_user_search_history():
    """Get current user's search history"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Not logged in'
            }), 401
        
        limit = request.args.get('limit', 20, type=int)
        
        history = search_tracker.get_user_search_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        print(f"Error in api_user_search_history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Phase 1 - Step 2: Get user's search patterns
@app.route('/api/user/search-patterns', methods=['GET'])
def api_user_search_patterns():
    """Get current user's search patterns and interests"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Not logged in'
            }), 401
        
        patterns = search_tracker.get_user_search_patterns(user_id)
        
        if not patterns:
            return jsonify({
                'success': True,
                'patterns': None,
                'message': 'No search history yet'
            })
        
        return jsonify({
            'success': True,
            'patterns': patterns
        })
        
    except Exception as e:
        print(f"Error in api_user_search_patterns: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route("/api/search/autosuggest")
@limiter.limit("100 per hour")
def autosuggest():
    """Autosuggest search endpoint"""
    try:
        q = request.args.get("q", "").strip()
        
        if not q or len(q) < 2:
            return jsonify([])
        
        regex = {"$regex": q, "$options": "i"}
        results = []
        for s in services_col.find(
            {"$or": [{"name.en": regex}, {"subservices.name.en": regex}]},
            {"_id": 0, "id": 1, "name": 1, "subservices": 1}
        ).limit(10):
            results.append(s)
        
        return jsonify(results)
        
    except Exception as e:
        print(f"Error in autosuggest: {e}")
        return jsonify([]), 500

# ==================== PHASE 1 STEP 3: AD DISPLAY ENDPOINTS ====================

@app.route('/api/ads/personalized', methods=['GET'])
def api_personalized_ads():
    """Get personalized ads for current user"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            # Return featured/default ads for non-logged-in users
            ads = list(products_col.find({"status": "active", "featured": True}).limit(5))
            for ad in ads:
                ad['_id'] = str(ad['_id'])
            return jsonify({
                'success': True,
                'ads': ads,
                'personalized': False
            })
        
        # Get personalized ads
        limit = request.args.get('limit', 5, type=int)
        context = request.args.get('context', 'sidebar')
        
        ads = ad_matcher.get_personalized_ads(user_id, limit, context)
        
        return jsonify({
            'success': True,
            'ads': ads,
            'personalized': True
        })
        
    except Exception as e:
        print(f"Error in api_personalized_ads: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/ads/click', methods=['POST'])
def api_ad_click():
    """Track ad click and redirect"""
    try:
        data = request.json or {}
        ad_id = data.get('ad_id')
        user_id = session.get('user_id')
        context = data.get('context', 'sidebar')
        
        if not ad_id:
            return jsonify({
                'success': False,
                'message': 'Ad ID required'
            }), 400
        
        # Track click if user is logged in
        if user_id:
            ad_matcher.track_ad_click(user_id, ad_id, context)
        
        # Get ad details for redirect URL
        ad = products_col.find_one({"_id": ObjectId(ad_id)})
        
        if ad:
            return jsonify({
                'success': True,
                'redirect_url': ad.get('link') or ad.get('url'),
                'ad': {
                    'title': ad.get('title'),
                    'category': ad.get('category')
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Ad not found'
            }), 404
            
    except Exception as e:
        print(f"Error in api_ad_click: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/user/ad-history', methods=['GET'])
def api_user_ad_history():
    """Get user's ad interaction history"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Not logged in'
            }), 401
        
        limit = request.args.get('limit', 20, type=int)
        history = ad_matcher.get_user_ad_history(user_id, limit)
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        print(f"Error in api_user_ad_history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== OTHER API ENDPOINTS ====================

@app.route("/api/profile/step", methods=["POST"])
@limiter.limit("20 per hour")
def profile_step():
    """Progressive profile saving"""
    try:
        payload = request.json or {}
        profile_id = payload.get("profile_id")
        email = payload.get("email")
        step = payload.get("step", "unknown")
        data = payload.get("data", {})
        
        if profile_id:
            try:
                users_col.update_one(
                    {"_id": ObjectId(profile_id)},
                    {"$set": {f"profile.{step}": data, "updated": datetime.utcnow()}},
                    upsert=True
                )
                return jsonify({"status": "ok", "profile_id": profile_id})
            except:
                pass
        
        if email:
            res = users_col.find_one_and_update(
                {"email": email},
                {"$set": {f"profile.{step}": data, "updated": datetime.utcnow()}},
                upsert=True,
                return_document=True
            )
            return jsonify({"status": "ok", "profile_id": str(res.get("_id"))})
        
        # Fallback - create anonymous
        new_id = users_col.insert_one({
            "profile": {step: data},
            "created": datetime.utcnow()
        }).inserted_id
        return jsonify({"status": "ok", "profile_id": str(new_id)})
        
    except Exception as e:
        print(f"Error in profile_step: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/service/<service_id>")
@limiter.limit("100 per hour")
def get_service(service_id):
    cache_key = f"service_{service_id}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    doc = services_col.find_one({"id": service_id}, {"_id": 0})
    result = doc or {}
    cache.set(cache_key, result, timeout=300)
    return jsonify(result)

@app.route("/api/engagement", methods=["POST"])
@limiter.limit("50 per hour, 10 per minute")
def log_engagement():
    payload = request.json or {}
    user_id = None
    try:
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
    except:
        pass
    
    doc = {
        "user_id": user_id,
        "anonymous_user_id": payload.get("user_id") if not user_id else None,
        "age": int(payload.get("age")) if payload.get("age") else None,
        "job": payload.get("job"),
        "desires": payload.get("desires") or [],
        "question_clicked": payload.get("question_clicked"),
        "service": payload.get("service"),
        "ad": payload.get("ad"),
        "source": payload.get("source"),
        "timestamp": datetime.utcnow()
    }
    result = eng_col.insert_one(doc)
    
    if user_id:
        auth_manager.record_user_engagement(user_id, payload)
    
    return jsonify({"status": "ok", "engagement_id": str(result.inserted_id)})

# ==================== USER AUTHENTICATION ENDPOINTS ====================

@app.route("/api/auth/register", methods=["POST"])
@limiter.limit("10 per hour")
def api_register():
    """User registration endpoint"""
    try:
        data = request.json or {}
        email = data.get("email", "").strip()
        password = data.get("password", "")
        name = data.get("name", "").strip()
        phone = data.get("phone", "")
        age = data.get("age")
        location = data.get("location", "")
        job = data.get("job", "")
        interests = data.get("interests", [])
        
        # Validate required fields
        if not email or not password or not name:
            return jsonify({
                "success": False,
                "message": "Email, password, and name are required"
            }), 400
        
        # Use auth manager to register
        result = auth_manager.register_user(
            email=email,
            password=password,
            name=name,
            phone=phone,
            age=age,
            location=location,
            interests=interests
        )
        
        if result["success"]:
            user_id = result["user_id"]
            
            # AUTOMATIC AI CATEGORIZATION
            try:
                categorization_data = {
                    "age": age,
                    "job": job,
                    "location": location,
                    "interests": interests
                }
                
                # Get AI categories using advanced categorizer
                categories = ai_categorizer.categorize_user_on_registration(categorization_data)
                
                # Update user with AI categories
                users_col.update_one(
                    {"_id": ObjectId(user_id)},
                    {"$set": {"ai_categories": categories}}
                )
                
                print(f"✅ User registered and auto-categorized: {categories.get('categories', [])}")
                
            except Exception as e:
                print(f"⚠️ Auto-categorization warning: {e}")
                import traceback
                traceback.print_exc()
            
            # Create access token
            access_token = create_access_token(identity=user_id)
            
            # Store user_id in session
            session['user_id'] = user_id
            
            return jsonify({
                "success": True,
                "message": "Registration successful",
                "user_id": result["user_id"],
                "access_token": access_token,
                "ai_categories": categories.get('categories', []) if 'categories' in locals() else []
            }), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        print(f"Registration error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": "Registration failed. Please try again."
        }), 500

@app.route("/api/auth/login", methods=["POST"])
@limiter.limit("20 per hour")
def api_login():
    """User login endpoint"""
    try:
        data = request.json or {}
        email = data.get("email", "").strip()
        password = data.get("password", "")
        
        if not email or not password:
            return jsonify({
                "success": False,
                "message": "Email and password are required"
            }), 400
        
        # Use auth manager to login
        result = auth_manager.authenticate_user(email, password)
        
        if result["success"]:
            # Create access token
            access_token = create_access_token(identity=result["user_id"])
            
            # Store user_id in session for search tracking
            session['user_id'] = result["user_id"]
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user_id": result["user_id"],
                "user": result.get("user"),
                "access_token": access_token
            }), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({
            "success": False,
            "message": "Login failed. Please try again."
        }), 500

@app.route("/api/auth/user")
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = users_col.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
        
        if user:
            user["_id"] = str(user["_id"])
            return jsonify({
                "success": True,
                "user": user
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
    except Exception as e:
        print(f"Get user error: {e}")
        return jsonify({
            "success": False,
            "message": "Failed to retrieve user"
        }), 500

@app.route("/api/user/profile")
def api_user_profile():
    """Get user profile (for search history page)"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                "success": False,
                "message": "Not logged in"
            }), 401
        
        user = users_col.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
        
        if user:
            user["_id"] = str(user["_id"])
            return jsonify({
                "success": True,
                "user": user
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404
            
    except Exception as e:
        print(f"Get profile error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def api_logout():
    """User logout endpoint"""
    try:
        user_id = get_jwt_identity()
        
        # Clear session
        session.pop('user_id', None)
        
        return jsonify({
            "success": True,
            "message": "Logout successful"
        }), 200
        
    except Exception as e:
        print(f"Logout error: {e}")
        return jsonify({
            "success": False,
            "message": "Logout failed"
        }), 500

@app.route("/api/user/categories/<user_id>")
def get_user_ai_categories(user_id):
    """Get user's AI categories"""
    try:
        categories = ai_categorizer.get_user_categories(user_id)
        user = users_col.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        
        ai_data = user.get("ai_categories", {})
        
        return jsonify({
            "success": True,
            "categories": categories,
            "category_scores": ai_data.get("category_scores", {}),
            "categorized_at": ai_data.get("categorized_at"),
            "last_recategorized": ai_data.get("last_recategorized"),
            "categorization_type": ai_data.get("categorization_type")
        })
        
    except Exception as e:
        print(f"Error getting categories: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ==================== ADMIN ENDPOINTS ====================

@app.route("/admin")
def admin_page():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login")
    return render_template("admin.html")

@app.route("/admin/manage")
@admin_required
def manage_page():
    return render_template("manage.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin.html")
    
    data = request.form
    username = data.get("username")
    password = data.get("password")
    
    admin = admins_col.find_one({"username": username})
    if admin and admin.get("password") == password:
        session["admin_logged_in"] = True
        session["admin_user"] = username
        return redirect("/admin")
    
    return "Login failed", 401

@app.route("/api/admin/insights")
@admin_required
def admin_insights():
    """Enhanced admin analytics endpoint"""
    try:
        # User metrics
        total_users = users_col.count_documents({})
        active_users = users_col.count_documents({
            "last_login": {"$gte": datetime.utcnow() - timedelta(days=30)}
        })
        new_users_7d = users_col.count_documents({
            "created_at": {"$gte": datetime.utcnow() - timedelta(days=7)}
        })
        
        # Engagement metrics
        total_engagements = eng_col.count_documents({})
        recent_engagements = eng_col.count_documents({
            "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
        })
        
        # Age distribution
        age_groups = {}
        for user in users_col.find({"age": {"$exists": True}}):
            age = user.get("age")
            if age:
                if age < 25:
                    group = "18-24"
                elif age < 35:
                    group = "25-34"
                elif age < 45:
                    group = "35-44"
                elif age < 55:
                    group = "45-54"
                else:
                    group = "55+"
                age_groups[group] = age_groups.get(group, 0) + 1
        
        # Job distribution
        jobs = {}
        for user in users_col.find({"job": {"$exists": True}}):
            job = user.get("job", "Unknown")
            jobs[job] = jobs.get(job, 0) + 1
        
        # Service engagement
        services = {}
        for eng in eng_col.find({"service": {"$exists": True}}):
            service = eng.get("service")
            if service:
                services[service] = services.get(service, 0) + 1
        
        return jsonify({
            "success": True,
            "metrics": {
                "total_users": total_users,
                "active_users": active_users,
                "new_users_7d": new_users_7d,
                "total_engagements": total_engagements,
                "recent_engagements": recent_engagements
            },
            "age_groups": age_groups,
            "jobs": jobs,
            "services": services
        })
        
    except Exception as e:
        print(f"Error in admin_insights: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Phase 1 - Step 2: Admin endpoint to view trending searches
@app.route('/api/admin/trending-searches', methods=['GET'])
@admin_required
def api_trending_searches():
    """Get trending searches (admin only)"""
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        trending = search_tracker.get_trending_searches(days, limit)
        popular_categories = search_tracker.get_popular_categories(days)
        
        return jsonify({
            'success': True,
            'trending_searches': trending,
            'popular_categories': popular_categories
        })
        
    except Exception as e:
        print(f"Error in api_trending_searches: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== PHASE 1 STEP 3: ADMIN PRODUCT MANAGEMENT ====================

@app.route('/api/admin/products', methods=['GET', 'POST'])
@admin_required
def api_admin_products():
    """Get all products or create new product (admin only)"""
    
    if request.method == 'GET':
        try:
            products = list(products_col.find({}))
            for product in products:
                product['_id'] = str(product['_id'])
            
            return jsonify({
                'success': True,
                'products': products
            })
            
        except Exception as e:
            print(f"Error getting products: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'POST':
        try:
            data = request.json or {}
            
            product_doc = {
                "title": data.get("title"),
                "description": data.get("description"),
                "category": data.get("category"),
                "price": float(data.get("price", 0)),
                "image_url": data.get("image_url"),
                "link": data.get("link"),
                "target_categories": data.get("target_categories", []),
                "target_age_min": data.get("target_age_min"),
                "target_age_max": data.get("target_age_max"),
                "target_locations": data.get("target_locations", []),
                "interests": data.get("interests", []),
                "status": data.get("status", "active"),
                "featured": data.get("featured", False),
                "views": 0,
                "clicks": 0,
                "created_at": datetime.utcnow(),
                "created_by": session.get("admin_user")
            }
            
            result = products_col.insert_one(product_doc)
            
            return jsonify({
                'success': True,
                'message': 'Product created successfully',
                'product_id': str(result.inserted_id)
            }), 201
            
        except Exception as e:
            print(f"Error creating product: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

@app.route('/api/admin/products/<product_id>', methods=['GET', 'PUT', 'DELETE'])
@admin_required
def api_admin_product(product_id):
    """Get, update, or delete a specific product (admin only)"""
    
    if request.method == 'GET':
        try:
            product = products_col.find_one({"_id": ObjectId(product_id)})
            if product:
                product['_id'] = str(product['_id'])
                return jsonify({
                    'success': True,
                    'product': product
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'PUT':
        try:
            data = request.json or {}
            
            update_doc = {
                "title": data.get("title"),
                "description": data.get("description"),
                "category": data.get("category"),
                "price": float(data.get("price", 0)),
                "image_url": data.get("image_url"),
                "link": data.get("link"),
                "target_categories": data.get("target_categories", []),
                "target_age_min": data.get("target_age_min"),
                "target_age_max": data.get("target_age_max"),
                "target_locations": data.get("target_locations", []),
                "interests": data.get("interests", []),
                "status": data.get("status", "active"),
                "featured": data.get("featured", False),
                "updated_at": datetime.utcnow(),
                "updated_by": session.get("admin_user")
            }
            
            products_col.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": update_doc}
            )
            
            return jsonify({
                'success': True,
                'message': 'Product updated successfully'
            })
            
        except Exception as e:
            print(f"Error updating product: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    elif request.method == 'DELETE':
        try:
            result = products_col.delete_one({"_id": ObjectId(product_id)})
            
            if result.deleted_count > 0:
                return jsonify({
                    'success': True,
                    'message': 'Product deleted successfully'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Product not found'
                }), 404
                
        except Exception as e:
            print(f"Error deleting product: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

@app.route('/api/ads/performance/<ad_id>', methods=['GET'])
@admin_required
def api_ad_performance(ad_id):
    """Get performance metrics for an ad (admin only)"""
    try:
        days = request.args.get('days', 30, type=int)
        performance = ad_matcher.get_ad_performance(ad_id, days)
        
        return jsonify({
            'success': True,
            'performance': performance
        })
        
    except Exception as e:
        print(f"Error in api_ad_performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/ads/top-performing', methods=['GET'])
@admin_required
def api_top_performing_ads():
    """Get top performing ads (admin only)"""
    try:
        limit = request.args.get('limit', 10, type=int)
        days = request.args.get('days', 30, type=int)
        
        top_ads = ad_matcher.get_top_performing_ads(limit, days)
        
        return jsonify({
            'success': True,
            'top_ads': top_ads
        })
        
    except Exception as e:
        print(f"Error in api_top_performing_ads: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/admin/ads/category-performance', methods=['GET'])
@admin_required
def api_category_performance():
    """Get performance by category (admin only)"""
    try:
        days = request.args.get('days', 30, type=int)
        category_stats = ad_matcher.get_category_performance(days)
        
        return jsonify({
            'success': True,
            'category_performance': category_stats
        })
        
    except Exception as e:
        print(f"Error in api_category_performance: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== RUN APP ====================

if __name__ == "__main__":
    print("🚀 Starting Citizen Portal with ALL Phase 1 Features...")
    print("✅ Phase 1 - Step 1: AI Auto-Categorization")
    print("✅ Phase 1 - Step 2: Search Tracking & Interest Profiling")
    print("✅ Phase 1 - Step 3: Personalized Ad Display")
    print("📊 Visit /search-history to view your search activity")
    print("📢 Personalized ads will appear in the sidebar")
    app.run(debug=True, host="0.0.0.0", port=5000)