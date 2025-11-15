import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import bcrypt
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]

# Collections
users_col = db["users"]
engagements_col = db["engagements"]

def create_test_user():
    """Create a test user for premium suggestions"""
    
    # Check if user already exists
    existing_user = users_col.find_one({"email": "jeewansiriwardhana5@gmail.com"})
    if existing_user:
        print("Test user already exists")
        return str(existing_user["_id"])
    
    # Create test user
    test_user = {
        "email": "jeewansiriwardhana5@gmail.com",
        "password_hash": bcrypt.hashpw("testpass123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "name": "Jeevan Siriwardhana",
        "phone": "+94771234567",
        "age": 28,
        "location": "Negombo, Western Province",
        "interests": ["education", "business", "health"],
        "created_at": datetime.utcnow() - timedelta(days=30),
        "last_login": datetime.utcnow() - timedelta(days=1),
        "is_active": True,
        "profile_completed": True,
        "engagement_count": 0,
        "favorite_services": [],
        "notification_preferences": {
            "email_updates": True,
            "service_recommendations": True,
            "premium_suggestions": True
        }
    }
    
    result = users_col.insert_one(test_user)
    print(f"Created test user with ID: {result.inserted_id}")
    return str(result.inserted_id)

def create_premium_engagement_pattern(user_id):
    """Create engagement pattern that qualifies for premium suggestions"""
    
    # Clear existing engagements for this user
    engagements_col.delete_many({"user_id": user_id})
    
    # Create repeated engagements for Ministry of Education
    base_time = datetime.utcnow() - timedelta(days=5)
    
    engagements = [
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher",
            "desires": ["school registration", "education documents"],
            "question_clicked": "How to register a new school?",
            "service": "Ministry of Education",
            "timestamp": base_time + timedelta(days=0, hours=2)
        },
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher", 
            "desires": ["school registration", "licensing"],
            "question_clicked": "What documents are required for school registration?",
            "service": "Ministry of Education",
            "timestamp": base_time + timedelta(days=1, hours=3)
        },
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher",
            "desires": ["school registration", "approval process"],
            "question_clicked": "How long does school approval take?",
            "service": "Ministry of Education", 
            "timestamp": base_time + timedelta(days=2, hours=1)
        },
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher",
            "desires": ["school registration", "fees"],
            "question_clicked": "What are the fees for school registration?",
            "service": "Ministry of Education",
            "timestamp": base_time + timedelta(days=3, hours=4)
        },
        # Also add some engagements for Ministry of Health (different pattern)
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher",
            "desires": ["health services", "clinic registration"], 
            "question_clicked": "How to register a private clinic?",
            "service": "Ministry of Health",
            "timestamp": base_time + timedelta(days=1, hours=6)
        },
        {
            "user_id": user_id,
            "age": 28,
            "job": "Teacher",
            "desires": ["health services", "medical license"],
            "question_clicked": "Medical practice license requirements?",
            "service": "Ministry of Health",
            "timestamp": base_time + timedelta(days=3, hours=2)
        }
    ]
    
    # Insert engagements
    result = engagements_col.insert_many(engagements)
    print(f"Created {len(result.inserted_ids)} test engagements")
    
    # Update user engagement count
    users_col.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"engagement_count": len(engagements)}}
    )

def create_additional_test_users():
    """Create a few more test users for better demo data"""
    
    additional_users = [
        {
            "email": "test.user1@example.com",
            "name": "Kasun Perera",
            "interests": ["transport", "business"],
            "engagements": [
                {"service": "Ministry of Transport", "question": "How to get driving license?", "days_ago": 2},
                {"service": "Ministry of Transport", "question": "Vehicle registration process?", "days_ago": 1},
                {"service": "Ministry of Transport", "question": "License renewal fees?", "days_ago": 0}
            ]
        },
        {
            "email": "test.user2@example.com", 
            "name": "Nimali Silva",
            "interests": ["housing", "finance"],
            "engagements": [
                {"service": "Ministry of Housing", "question": "Housing loan application?", "days_ago": 4},
                {"service": "Ministry of Housing", "question": "Property registration process?", "days_ago": 2},
                {"service": "Ministry of Finance", "question": "Tax calculation for property?", "days_ago": 1}
            ]
        }
    ]
    
    for user_data in additional_users:
        # Check if user exists
        if users_col.find_one({"email": user_data["email"]}):
            continue
            
        # Create user
        user_doc = {
            "email": user_data["email"],
            "password_hash": bcrypt.hashpw("testpass123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "name": user_data["name"],
            "age": 25,
            "location": "Colombo, Western Province",
            "interests": user_data["interests"],
            "created_at": datetime.utcnow() - timedelta(days=20),
            "last_login": datetime.utcnow() - timedelta(hours=2),
            "is_active": True,
            "profile_completed": True,
            "engagement_count": len(user_data["engagements"]),
            "notification_preferences": {
                "email_updates": True,
                "service_recommendations": True,
                "premium_suggestions": True
            }
        }
        
        result = users_col.insert_one(user_doc)
        user_id = str(result.inserted_id)
        
        # Create engagements
        for eng in user_data["engagements"]:
            engagement_doc = {
                "user_id": user_id,
                "age": 25,
                "job": "Professional",
                "desires": user_data["interests"],
                "question_clicked": eng["question"],
                "service": eng["service"], 
                "timestamp": datetime.utcnow() - timedelta(days=eng["days_ago"])
            }
            engagements_col.insert_one(engagement_doc)
        
        print(f"Created additional test user: {user_data['name']}")

if __name__ == "__main__":
    print("Creating test data for premium suggestions...")
    
    # Create main test user
    user_id = create_test_user()
    
    # Create engagement patterns
    create_premium_engagement_pattern(user_id)
    
    # Create additional test users
    create_additional_test_users()
    
    print("\nTest data creation completed!")
    print("Now the premium suggestions feature should have data to work with.")
    print("\nTest user credentials:")
    print("Email: jeewansiriwardhana5@gmail.com") 
    print("Password: testpass123")