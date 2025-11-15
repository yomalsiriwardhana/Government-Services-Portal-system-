import bcrypt
import re
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import email_validator


class UserAuthManager:
    def __init__(self, db):
        self.db = db
        self.users_col = db["users"]
        self.user_sessions_col = db["user_sessions"]
    
    def validate_email(self, email):
        """Validate email format"""
        try:
            email_validator.validate_email(email)
            return True
        except email_validator.EmailNotValidError:
            return False
    
    def validate_password(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r"[A-Za-z]", password):
            return False, "Password must contain letters"
        if not re.search(r"\d", password):
            return False, "Password must contain numbers"
        return True, "Valid password"
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def register_user(self, email, password, name, phone=None, age=None, location=None, interests=None):
        """Register a new user"""
        # Validate email
        if not self.validate_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        # Check if user already exists
        if self.users_col.find_one({"email": email.lower().strip()}):
            return {"success": False, "message": "Email already registered"}
        
        # Validate password
        valid, message = self.validate_password(password)
        if not valid:
            return {"success": False, "message": message}
        
        # Create user document
        user_doc = {
            "email": email.lower().strip(),
            "password_hash": self.hash_password(password),
            "name": name.strip(),
            "phone": phone,
            "age": int(age) if age else None,
            "location": location,
            "interests": interests or [],
            "created_at": datetime.utcnow(),
            "last_login": None,
            "is_active": True,
            "profile_completed": bool(phone and age and location),
            "engagement_count": 0,
            "favorite_services": [],
            "notification_preferences": {
                "email_updates": True,
                "service_recommendations": True,
                "premium_suggestions": True
            }
        }
        
        try:
            result = self.users_col.insert_one(user_doc)
            return {
                "success": True,
                "message": "User registered successfully",
                "user_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def authenticate_user(self, email, password):
        """Authenticate user login"""
        user = self.users_col.find_one({"email": email.lower().strip()})
        
        if not user:
            return {"success": False, "message": "User not found"}
        
        if not user.get("is_active", True):
            return {"success": False, "message": "Account deactivated"}
        
        if not self.verify_password(password, user["password_hash"]):
            return {"success": False, "message": "Invalid password"}
        
        # Update last login
        self.users_col.update_one(
            {"_id": user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        # Create access token
        access_token = create_access_token(
            identity=str(user["_id"]),
            expires_delta=timedelta(days=7)
        )
        
        return {
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "user_id": str(user["_id"]),
            "user": {
                "id": str(user["_id"]),
                "email": user["email"],
                "name": user["name"],
                "profile_completed": user.get("profile_completed", False)
            }
        }
    
    def get_user_profile(self, user_id):
        """Get user profile information"""
        try:
            from bson import ObjectId
            user = self.users_col.find_one(
                {"_id": ObjectId(user_id)},
                {"password_hash": 0}  # Exclude password hash
            )
            
            if user:
                user["_id"] = str(user["_id"])
                return {"success": True, "user": user}
            else:
                return {"success": False, "message": "User not found"}
        except Exception as e:
            return {"success": False, "message": f"Error fetching profile: {str(e)}"}
    
    def update_user_profile(self, user_id, updates):
        """Update user profile"""
        try:
            from bson import ObjectId
            
            # Remove sensitive fields that shouldn't be updated this way
            safe_updates = {k: v for k, v in updates.items()
                          if k not in ['password_hash', '_id', 'created_at', 'email']}
            
            if 'age' in safe_updates:
                safe_updates['age'] = int(safe_updates['age']) if safe_updates['age'] else None
            
            safe_updates['updated_at'] = datetime.utcnow()
            
            result = self.users_col.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": safe_updates}
            )
            
            if result.modified_count > 0:
                return {"success": True, "message": "Profile updated successfully"}
            else:
                return {"success": False, "message": "No changes made"}
        except Exception as e:
            return {"success": False, "message": f"Update failed: {str(e)}"}
    
    def record_user_engagement(self, user_id, engagement_data):
        """Record user engagement with personalized tracking"""
        try:
            from bson import ObjectId
            
            # Add user_id to engagement data
            engagement_data["user_id"] = user_id
            engagement_data["timestamp"] = datetime.utcnow()
            
            # Store in engagements collection
            self.db["engagements"].insert_one(engagement_data)
            
            # Update user engagement count
            self.users_col.update_one(
                {"_id": ObjectId(user_id)},
                {"$inc": {"engagement_count": 1}}
            )
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def get_user_recommendations(self, user_id):
        """Get personalized service recommendations"""
        try:
            from bson import ObjectId
            
            # Get user profile
            user = self.users_col.find_one({"_id": ObjectId(user_id)})
            if not user:
                return {"success": False, "message": "User not found"}
            
            # Get user's engagement history
            engagements = list(self.db["engagements"].find({"user_id": user_id}))
            
            # Simple recommendation algorithm
            recommendations = []
            user_interests = user.get("interests", [])
            user_age = user.get("age")
            
            # Get all services
            services = list(self.db["services"].find({}, {"_id": 0}))
            
            for service in services:
                score = 0
                reasons = []
                
                # Score based on interests
                service_name = service.get("name", {}).get("en", "").lower()
                for interest in user_interests:
                    if interest.lower() in service_name:
                        score += 2
                        reasons.append(f"Matches your interest in {interest}")
                
                # Score based on age appropriateness
                if user_age:
                    if "youth" in service_name and user_age < 30:
                        score += 1
                        reasons.append("Relevant for your age group")
                    elif "education" in service_name and user_age < 25:
                        score += 1
                        reasons.append("Educational opportunities")
                
                # Score based on past engagements
                for eng in engagements:
                    if eng.get("service") == service.get("name", {}).get("en"):
                        score += 1
                        reasons.append("Based on your previous activity")
                
                if score > 0:
                    recommendations.append({
                        "service": service,
                        "score": score,
                        "reasons": reasons
                    })
            
            # Sort by score and return top 5
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            return {
                "success": True,
                "recommendations": recommendations[:5],
                "total_services": len(services)
            }
        except Exception as e:
            return {"success": False, "message": str(e)}


def user_required(f):
    """Decorator to require user authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function