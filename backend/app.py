from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from config import Config
from pymongo import MongoClient
import os

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# MongoDB connection
try:
    client = MongoClient(app.config['MONGO_URI'])
    db = client.government_portal
    print("✅ Connected to MongoDB successfully")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")
    db = None

# Make db available to routes
app.db = db

# Get the absolute path to the frontend directory
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
print(f"📁 Frontend directory: {FRONTEND_DIR}")
print(f"📁 Frontend exists: {os.path.exists(FRONTEND_DIR)}")

# Serve frontend files BEFORE registering blueprints
@app.route('/')
def index():
    """Serve the main index page"""
    try:
        return send_from_directory(FRONTEND_DIR, 'index.html')
    except Exception as e:
        print(f"Error serving index: {str(e)}")
        return jsonify({"error": f"Could not load index.html: {str(e)}"}), 500

@app.route('/<path:filename>')
def serve_frontend(filename):
    """Serve frontend static files - registered BEFORE blueprints to take priority"""
    try:
        # If it contains .html, .css, .js, or common extensions, try to serve it
        if any(filename.endswith(ext) for ext in ['.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.json']):
            file_path = os.path.join(FRONTEND_DIR, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(FRONTEND_DIR, filename)
        
        # If it starts with known frontend directories
        if any(filename.startswith(prefix) for prefix in ['css/', 'js/', 'admin/', 'assets/', 'images/']):
            file_path = os.path.join(FRONTEND_DIR, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(FRONTEND_DIR, filename)
        
        # If nothing matched, continue to blueprints (will return 404 if not found)
        return jsonify({"error": f"File not found: {filename}"}), 404
        
    except Exception as e:
        print(f"Error serving {filename}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Import and register blueprints AFTER static file routes
try:
    from routes.auth import auth_bp
except ImportError:
    from routes.auth import bp as auth_bp

try:
    from routes.services import services_bp
except ImportError:
    from routes.services import bp as services_bp

try:
    from routes.products import products_bp
except ImportError:
    from routes.products import bp as products_bp

try:
    from routes.search import search_bp
except ImportError:
    from routes.search import bp as search_bp

try:
    from routes.announcements import announcements_bp
except ImportError:
    from routes.announcements import bp as announcements_bp

try:
    from routes.ministries import ministries_bp
except ImportError:
    from routes.ministries import bp as ministries_bp

try:
    from routes.admin import admin_bp
except ImportError:
    from routes.admin import bp as admin_bp
try:
    from routes.recommendations import recommendations_bp
except ImportError:
    from routes.recommendations import bp as recommendations_bp
try:
    from routes.ai_search import ai_search_bp
except ImportError:
    from routes.ai_search import bp as ai_search_bp

try:
    from routes.chat import chat_bp
except ImportError:
    from routes.chat import bp as chat_bp

# Register blueprints with url_prefix to avoid conflicts
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(services_bp, url_prefix='/api/services')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(search_bp, url_prefix='/api/search')
app.register_blueprint(announcements_bp, url_prefix='/api/announcements')
app.register_blueprint(recommendations_bp, url_prefix='/api')
app.register_blueprint(ministries_bp, url_prefix='/api/ministries')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(ai_search_bp)  # Already has /api prefix in blueprint
app.register_blueprint(chat_bp, url_prefix='/api')  # Chat endpoint at /api/chat

print("✅ All blueprints registered successfully")

# Print all registered routes for debugging
print("\n📍 Registered API Routes:")
api_routes = [rule for rule in app.url_map.iter_rules() if rule.rule.startswith('/api/')]
for rule in api_routes:
    methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
    print(f"  {rule.rule} -> {rule.endpoint} [{methods}]")
print()

# Error handlers
@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    print(f"500 error: {str(e)}")
    import traceback
    traceback.print_exc()
    return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print("🌐 Access the application at: http://localhost:5000")
    print("🌐 Dashboard: http://localhost:5000/dashboard-enhanced.html")
    print("📡 AI Search endpoint: http://localhost:5000/api/ai-search/ministry")
    print()
    app.run(host='0.0.0.0', port=5000, debug=True)