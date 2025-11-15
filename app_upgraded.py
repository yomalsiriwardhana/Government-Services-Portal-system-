import os
import json
from flask import Flask, jsonify, render_template, request, session, redirect, send_file, abort
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
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
import pathlib
import numpy as np
from sentence_transformers import SentenceTransformer

# Try to import FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available, using fallback search")

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

# NEW collections for Task 07
categories_col = db["categories"]
officers_col = db["officers"]
ads_col = db["ads"]
users_col = db["users"]

# Initialize services
auth_manager = UserAuthManager(db)
email_service = EmailService()
premium_service = PremiumSuggestionService(db, email_service)

# Embedding model (lazy-init)
EMBED_MODEL = None
INDEX_PATH = pathlib.Path("./data/faiss.index")
META_PATH = pathlib.Path("./data/faiss_meta.json")
VECTOR_DIM = 384

def get_embedding_model():
    global EMBED_MODEL
    if EMBED_MODEL is None:
        EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return EMBED_MODEL

# Helper function
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

# ==================== PUBLIC ROUTES ====================
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

# ==================== NEW API ENDPOINTS ====================

# Categories API
@app.route("/api/categories")
@limiter.limit("200 per hour")
def get_categories():
    cache_key = "categories_list"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    cats = list(categories_col.find({}, {"_id": 0}))
    
    # If no categories, create dynamic ones from services
    if not cats:
        pipeline = [
            {"$project": {"id": 1, "name": 1, "category": 1}},
            {"$group": {"_id": "$category", "ministries": {"$push": {"id": "$id", "name": "$name"}}}}
        ]
        try:
            groups = list(services_col.aggregate(pipeline))
            cats = [{"id": g["_id"] or "uncategorized", "name": {"en": g["_id"] or "Uncategorized"}, "ministries": g["ministries"]} for g in groups]
        except:
            cats = []
    
    cache.set(cache_key, cats, timeout=600)
    return jsonify(cats)

# Autosuggest API
@app.route("/api/search/autosuggest")
@limiter.limit("100 per hour")
def autosuggest():
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

# Progressive Profile API
@app.route("/api/profile/step", methods=["POST"])
@limiter.limit("20 per hour")
def profile_step():
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
    
    # Fallback - create anonymous profile
    new_id = users_col.insert_one({
        "profile": {step: data},
        "created": datetime.utcnow()
    }).inserted_id
    return jsonify({"status": "ok", "profile_id": str(new_id)})

# Ads API
@app.route("/api/ads")
@limiter.limit("200 per hour")
def get_ads():
    cache_key = "ads_list"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    ads = list(ads_col.find({}, {"_id": 0}))
    cache.set(cache_key, ads, timeout=600)
    return jsonify(ads)

# ==================== AI SEARCH WITH FAISS ====================

def build_vector_index():
    """Build or rebuild FAISS index from services"""
    os.makedirs("data", exist_ok=True)
    docs = []
    
    # Flatten services to searchable documents
    for svc in services_col.find():
        svc_id = svc.get("id")
        svc_name = svc.get("name", {}).get("en") or svc.get("name")
        for sub in svc.get("subservices", []):
            sub_id = sub.get("id")
            sub_name = sub.get("name", {}).get("en") or sub.get("name")
            for q in sub.get("questions", []):
                q_text = q.get("q", {}).get("en") or q.get("q")
                a_text = q.get("answer", {}).get("en") or q.get("answer")
                content = " | ".join([svc_name or "", sub_name or "", q_text or "", a_text or ""])
                docs.append({
                    "doc_id": f"{svc_id}::{sub_id}::{q_text[:80] if q_text else 'unknown'}",
                    "service_id": svc_id,
                    "subservice_id": sub_id,
                    "title": q_text,
                    "content": content,
                    "metadata": {
                        "downloads": q.get("downloads", []),
                        "location": q.get("location"),
                        "instructions": q.get("instructions")
                    }
                })
    
    if not docs:
        return {"count": 0, "error": "No documents to index"}
    
    # Generate embeddings
    model = get_embedding_model()
    texts = [d["content"] for d in docs]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    embeddings = embeddings / norms
    
    if FAISS_AVAILABLE:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings.astype(np.float32))
        faiss.write_index(index, str(INDEX_PATH))
    else:
        np.save("data/embeddings.npy", embeddings)
    
    # Save metadata
    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    
    return {"count": len(docs), "faiss": FAISS_AVAILABLE}

def search_vectors(query, top_k=5):
    """Search using vector similarity"""
    model = get_embedding_model()
    q_emb = model.encode([query], convert_to_numpy=True)
    q_emb = q_emb / (np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-10)
    
    if FAISS_AVAILABLE and INDEX_PATH.exists() and META_PATH.exists():
        index = faiss.read_index(str(INDEX_PATH))
        D, I = index.search(q_emb.astype(np.float32), top_k)
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
        hits = []
        for idx in I[0]:
            if idx < len(meta):
                hits.append(meta[idx])
        return hits
    else:
        # Fallback: linear scan
        if not META_PATH.exists():
            return []
        meta = json.load(open(META_PATH, "r", encoding="utf-8"))
        db_emb = np.load("data/embeddings.npy")
        sims = (db_emb @ q_emb[0]).tolist()
        idxs = np.argsort(sims)[::-1][:top_k]
        return [meta[int(i)] for i in idxs]

@app.route("/api/ai/search", methods=["POST"])
@limiter.limit("20 per minute, 100 per hour")
def ai_search_upgraded():
    payload = request.json or {}
    query = payload.get("query", "").strip()
    top_k = int(payload.get("top_k", 5))
    
    if not query:
        return jsonify({"error": "empty query"}), 400
    
    # Check cache
    cache_key = f"ai_search:{hash(query)}"
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    hits = search_vectors(query, top_k)
    
    # Build answer
    answer_parts = []
    sources = []
    for h in hits:
        txt = h.get("content", "")
        answer_parts.append(txt[:800])
        sources.append({
            "service_id": h.get("service_id"),
            "subservice_id": h.get("subservice_id"),
            "title": h.get("title"),
            **h.get("metadata", {})
        })
    
    answer = "\n\n---\n\n".join(answer_parts) if answer_parts else "No matching content found."
    result = {
        "query": query,
        "answer": answer,
        "sources": sources,
        "hits": len(sources),
        "confidence": 0.85 if sources else 0.0
    }
    
    cache.set(cache_key, result, timeout=600)
    return jsonify(result)

@app.route("/api/admin/build_index", methods=["POST"])
@admin_required
def admin_build_index():
    """Admin endpoint to rebuild the vector index"""
    res = build_vector_index()
    return jsonify(res)

# ==================== KEEP ALL YOUR EXISTING ENDPOINTS ====================
# (Your existing /api/services, /api/engagement, /api/admin/*, etc.)

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

# ... (keep all your other existing routes: admin, auth, user dashboard, etc.)

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

# ... (keep all remaining existing routes)

if __name__ == "__main__":
    if admins_col.count_documents({}) == 0:
        admins_col.insert_one({
            "username": "admin",
            "password": os.getenv("ADMIN_PWD", "admin123")
        })
    
    print("🚀 Starting upgraded application...")
    print("🔍 Initializing AI search engine...")
    try:
        initialize_search_engine()
        print("✅ AI search engine ready!")
    except Exception as e:
        print(f"⚠️  AI search initialization warning: {e}")
    
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))