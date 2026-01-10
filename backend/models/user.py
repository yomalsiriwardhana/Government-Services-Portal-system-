from datetime import datetime
from bson import ObjectId
import bcrypt

class User:
    """User model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db.users
    
    def create(self, user_data):
        """Create a new user"""
        # PASSWORD ALREADY HASHED IN auth.py - DO NOT HASH AGAIN TO AVOID DOUBLE HASHING
        # The password in user_data should already be hashed by bcrypt in auth.py
        
        # Add timestamps
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        
        # Initialize AI categories (will be populated by AI categorizer)
        if 'ai_categories' not in user_data:
            user_data['ai_categories'] = []
        
        # Initialize engagement metrics
        user_data['total_searches'] = 0
        user_data['total_ad_clicks'] = 0
        user_data['total_service_views'] = 0
        user_data['last_active'] = datetime.utcnow()
        
        # Insert user
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def find_by_email(self, email):
        """Find user by email"""
        return self.collection.find_one({'email': email})
    
    def find_by_id(self, user_id):
        """Find user by ID"""
        return self.collection.find_one({'_id': ObjectId(user_id)})
    
    def update(self, user_id, update_data):
        """Update user data"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def update_ai_categories(self, user_id, categories):
        """Update user's AI categories"""
        result = self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'ai_categories': categories,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    def update_last_active(self, user_id):
        """Update user's last active timestamp"""
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$set': {
                    'last_active': datetime.utcnow()
                }
            }
        )
    
    def increment_searches(self, user_id):
        """Increment user's total searches count"""
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {'total_searches': 1},
                '$set': {'last_active': datetime.utcnow()}
            }
        )
    
    def increment_ad_clicks(self, user_id):
        """Increment user's total ad clicks count"""
        self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {'total_ad_clicks': 1},
                '$set': {'last_active': datetime.utcnow()}
            }
        )
    
    def verify_password(self, email, password):
        """Verify user password"""
        user = self.find_by_email(email)
        if user and 'password' in user:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                user['password'].encode('utf-8') if isinstance(user['password'], str) else user['password']
            )
        return False
    
    def _hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def get_all_users(self, skip=0, limit=100):
        """Get all users with pagination"""
        users = list(self.collection.find().skip(skip).limit(limit))
        # Convert ObjectId to string
        for user in users:
            user['_id'] = str(user['_id'])
            # Remove password from response
            if 'password' in user:
                del user['password']
        return users
    
    def get_user_stats(self):
        """Get user statistics for admin dashboard"""
        total_users = self.collection.count_documents({})
        
        # Active users (last 30 days)
        thirty_days_ago = datetime.utcnow().replace(day=datetime.utcnow().day - 30)
        active_users = self.collection.count_documents({
            'last_active': {'$gte': thirty_days_ago}
        })
        
        # New users (last 7 days)
        seven_days_ago = datetime.utcnow().replace(day=datetime.utcnow().day - 7)
        new_users = self.collection.count_documents({
            'created_at': {'$gte': seven_days_ago}
        })
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'new_users': new_users
        }
    
    def get_age_distribution(self):
        """Get user age distribution"""
        pipeline = [
            {
                '$group': {
                    '_id': {
                        '$switch': {
                            'branches': [
                                {'case': {'$and': [{'$gte': ['$age', 18]}, {'$lte': ['$age', 24]}]}, 'then': '18-24'},
                                {'case': {'$and': [{'$gte': ['$age', 25]}, {'$lte': ['$age', 34]}]}, 'then': '25-34'},
                                {'case': {'$and': [{'$gte': ['$age', 35]}, {'$lte': ['$age', 44]}]}, 'then': '35-44'},
                                {'case': {'$and': [{'$gte': ['$age', 45]}, {'$lte': ['$age', 54]}]}, 'then': '45-54'},
                                {'case': {'$gte': ['$age', 55]}, 'then': '55+'}
                            ],
                            'default': 'Unknown'
                        }
                    },
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result
    
    def get_job_distribution(self):
        """Get user job distribution"""
        pipeline = [
            {
                '$group': {
                    '_id': '$job',
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result