import os
from datetime import timedelta

class Config:
    """Configuration class for the Government Portal application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    
    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'
    MONGO_DB_NAME = 'government_portal'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-this'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # Upload Configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # AI Configuration
    AI_CATEGORIES = [
        # Demographic Categories
        'young_adult',           # 18-24
        'early_career',          # 25-35
        'mid_career_family',     # 36-45
        'established_professional', # 46-60
        'senior',                # 60+
        
        # Professional Categories
        'student',
        'government_employee',
        'education_professional',
        'tech_professional',
        'business_owner',
        'management',
        
        # Behavioral Categories
        'education_seeker',
        'course_buyer',
        'book_buyer',
        'tech_enthusiast',
        'electronics_buyer',
        'vehicle_buyer',
        'property_seeker',
        'job_seeker',
        'travel_seeker',
        'health_focused',
        'parent',
        'power_user',
        'engaged_user'
    ]
    
    # Service Categories
    SERVICE_CATEGORIES = [
        'Education',
        'Health',
        'Business',
        'Immigration',
        'Employment',
        'Technology',
        'Transport',
        'Housing',
        'Financial'
    ]
    
    # Product Categories
    PRODUCT_CATEGORIES = [
        'Education',
        'Electronics',
        'Vehicles',
        'Property',
        'Courses',
        'Services'
    ]
    
    # Search Configuration
    SEARCH_HISTORY_DAYS = 30
    MIN_SEARCH_LENGTH = 2
    
    # Ad Configuration
    ADS_PER_PAGE = 5
    AD_REFRESH_INTERVAL = 300000  # 5 minutes in milliseconds