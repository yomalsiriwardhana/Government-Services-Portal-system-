import os
import time
import hashlib
from functools import wraps
from flask import request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedRateLimiter:
    def __init__(self, app=None, cache=None):
        self.app = app
        self.cache = cache
        self.blocked_ips = set()
        self.suspicious_activity = {}
        
        # Rate limiting rules for different endpoints
        self.rate_limits = {
            'default': '100 per hour',
            'api_search': '20 per minute',
            'auth_login': '5 per minute',
            'auth_register': '3 per minute',
            'admin_routes': '200 per hour',
            'public_services': '200 per hour',
            'engagement_logging': '50 per hour'
        }
        
        # Suspicious activity thresholds
        self.suspicious_thresholds = {
            'rapid_requests': 50,  # requests in 1 minute
            'failed_logins': 5,    # failed login attempts
            'ai_search_spam': 10   # AI searches in 1 minute
        }
    
    def get_client_id(self):
        """Get unique client identifier for rate limiting"""
        # Try to get user ID first (for authenticated users)
        if hasattr(g, 'current_user_id') and g.current_user_id:
            return f"user:{g.current_user_id}"
        
        # Fall back to IP address
        client_ip = get_remote_address()
        
        # For development/testing, handle local IPs
        if client_ip in ['127.0.0.1', 'localhost', '::1']:
            # Use session-based ID for local testing
            from flask import session
            session_id = session.get('rate_limit_id')
            if not session_id:
                session_id = hashlib.md5(f"{client_ip}{time.time()}".encode()).hexdigest()[:8]
                session['rate_limit_id'] = session_id
            return f"session:{session_id}"
        
        return f"ip:{client_ip}"
    
    def is_suspicious_activity(self, client_id, activity_type):
        """Check if client is showing suspicious activity patterns"""
        current_time = time.time()
        
        # Clean old entries (older than 1 hour)
        cutoff_time = current_time - 3600
        if client_id in self.suspicious_activity:
            self.suspicious_activity[client_id] = [
                timestamp for timestamp in self.suspicious_activity[client_id]
                if timestamp > cutoff_time
            ]
        
        # Initialize client tracking
        if client_id not in self.suspicious_activity:
            self.suspicious_activity[client_id] = []
        
        # Add current activity
        self.suspicious_activity[client_id].append(current_time)
        
        # Check for suspicious patterns
        recent_activity = [
            timestamp for timestamp in self.suspicious_activity[client_id]
            if timestamp > (current_time - 60)  # Last minute
        ]
        
        threshold = self.suspicious_thresholds.get(activity_type, 20)
        
        if len(recent_activity) > threshold:
            logger.warning(f"Suspicious activity detected for {client_id}: {activity_type}")
            return True
        
        return False
    
    def log_rate_limit_hit(self, client_id, endpoint, limit):
        """Log rate limit violations"""
        logger.info(f"Rate limit hit - Client: {client_id}, Endpoint: {endpoint}, Limit: {limit}")
        
        # Track repeated violations
        violation_key = f"violations:{client_id}"
        violations = self.cache.get(violation_key) or 0
        violations += 1
        self.cache.set(violation_key, violations, timeout=3600)  # 1 hour
        
        # Block IP after multiple violations
        if violations >= 10:
            self.blocked_ips.add(client_id)
            logger.warning(f"Blocked client due to repeated violations: {client_id}")
    
    def is_blocked(self, client_id):
        """Check if client is blocked"""
        return client_id in self.blocked_ips

class SmartCache:
    def __init__(self, cache):
        self.cache = cache
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0
        }
    
    def get_cache_key(self, prefix, *args, **kwargs):
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{':'.join(map(str, args))}"
        if kwargs:
            key_data += f":{':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))}"
        
        # Hash long keys
        if len(key_data) > 200:
            key_data = hashlib.md5(key_data.encode()).hexdigest()
        
        return key_data
    
    def cached_response(self, timeout=300, key_prefix='route'):
        """Decorator for caching API responses"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # Generate cache key
                cache_key = self.get_cache_key(
                    key_prefix,
                    request.path,
                    request.method,
                    str(sorted(request.args.items()))
                )
                
                # Try to get from cache
                cached_result = self.cache.get(cache_key)
                if cached_result is not None:
                    self.cache_stats['hits'] += 1
                    logger.info(f"Cache hit: {cache_key}")
                    return cached_result
                
                # Cache miss - execute function
                self.cache_stats['misses'] += 1
                result = f(*args, **kwargs)
                
                # Cache the result if it's a successful response
                if result:
                    try:
                        # Handle Flask Response objects
                        if hasattr(result, 'get_json') and result.status_code == 200:
                            cached_data = result.get_json()
                            self.cache.set(cache_key, result, timeout=timeout)
                            self.cache_stats['sets'] += 1
                            logger.info(f"Cache set: {cache_key}")
                        elif isinstance(result, (dict, list, tuple)):
                            self.cache.set(cache_key, result, timeout=timeout)
                            self.cache_stats['sets'] += 1
                            logger.info(f"Cache set: {cache_key}")
                    except Exception as e:
                        logger.warning(f"Failed to cache result for {cache_key}: {e}")
                
                return result
            return decorated_function
        return decorator
    
    def invalidate_pattern(self, pattern):
        """Invalidate cache keys matching a pattern"""
        # This is a simple implementation - Redis would be better for pattern matching
        try:
            # For simple cache, we can't do pattern matching
            # In production, use Redis for advanced cache invalidation
            logger.info(f"Cache invalidation requested for pattern: {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation failed: {e}")
    
    def get_stats(self):
        """Get cache performance statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'sets': self.cache_stats['sets'],
            'hit_rate': round(hit_rate, 2),
            'total_requests': total_requests
        }

def setup_rate_limiting_and_caching(app):
    """Initialize rate limiting and caching for Flask app"""
    
    # Initialize cache
    cache_config = {
        'CACHE_TYPE': os.getenv('CACHE_TYPE', 'simple'),
        'CACHE_DEFAULT_TIMEOUT': int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    }
    
    # Use Redis if available
    redis_url = os.getenv('REDIS_URL')
    if redis_url:
        cache_config.update({
            'CACHE_TYPE': 'redis',
            'CACHE_REDIS_URL': redis_url
        })
    
    cache = Cache(app, config=cache_config)
    smart_cache = SmartCache(cache)
    
    # Initialize advanced rate limiter first
    advanced_limiter = AdvancedRateLimiter(app, cache)
    
    # Initialize rate limiter with proper key function
    limiter = Limiter(
        key_func=advanced_limiter.get_client_id,
        app=app,
        default_limits=["1000 per hour", "100 per minute"],
        storage_uri=redis_url or "memory://"
    )
    
    # Rate limit violation handler
    @limiter.request_filter
    def filter_requests():
        client_id = advanced_limiter.get_client_id()
        if advanced_limiter.is_blocked(client_id):
            return True  # Skip rate limiting for blocked IPs (they'll get 403)
        return False
    
    @app.errorhandler(429)
    def ratelimit_handler(e):
        client_id = advanced_limiter.get_client_id()
        advanced_limiter.log_rate_limit_hit(client_id, request.endpoint or request.path, str(e.limit))
        
        return jsonify({
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Limit: {e.limit}",
            "retry_after": e.retry_after
        }), 429
    
    # Block suspicious IPs
    @app.before_request
    def check_blocked_clients():
        client_id = advanced_limiter.get_client_id()
        if advanced_limiter.is_blocked(client_id):
            return jsonify({
                "error": "Access blocked",
                "message": "Your access has been temporarily blocked due to suspicious activity"
            }), 403
    
    # Activity tracking for suspicious behavior detection
    @app.before_request
    def track_suspicious_activity():
        client_id = advanced_limiter.get_client_id()
        endpoint = request.endpoint or request.path
        
        # Track different types of suspicious activity
        activity_type = 'default'
        if 'login' in str(endpoint):
            activity_type = 'failed_logins'
        elif 'ai/search' in str(endpoint):
            activity_type = 'ai_search_spam'
        elif request.method in ['POST', 'PUT', 'DELETE']:
            activity_type = 'rapid_requests'
        
        if advanced_limiter.is_suspicious_activity(client_id, activity_type):
            # Could implement additional measures here (CAPTCHA, temporary blocks, etc.)
            pass
    
    return limiter, cache, smart_cache, advanced_limiter

# Decorators for easy use
def rate_limit(limit_string):
    """Decorator for custom rate limits on specific routes"""
    def decorator(f):
        # This will be applied by the limiter instance in app.py
        f._rate_limit = limit_string
        return f
    return decorator

def cache_result(timeout=300, key_prefix='custom'):
    """Decorator for caching function results"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This will be implemented by the smart_cache instance
            return f(*args, **kwargs)
        decorated_function._cache_timeout = timeout
        decorated_function._cache_prefix = key_prefix
        return decorated_function
    return decorator