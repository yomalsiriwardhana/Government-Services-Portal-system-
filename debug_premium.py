import os
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]

def debug_engagements():
    """Check what engagements exist in the database"""
    print("=== DEBUGGING ENGAGEMENTS ===")
    
    engagements = list(db["engagements"].find().sort("timestamp", -1))
    print(f"Total engagements in database: {len(engagements)}")
    
    # Show recent engagements
    print("\nRecent engagements:")
    for i, eng in enumerate(engagements[:10]):
        print(f"{i+1}. User: {eng.get('user_id')}")
        print(f"   Service: {eng.get('service')}")
        print(f"   Question: {eng.get('question_clicked')}")
        print(f"   Timestamp: {eng.get('timestamp')}")
        print()
    
    # Check engagements in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_engagements = list(db["engagements"].find({
        "timestamp": {"$gte": week_ago}
    }))
    print(f"\nEngagements in last 7 days: {len(recent_engagements)}")
    
    # Group by user and service
    user_service_counts = {}
    for eng in recent_engagements:
        user_id = eng.get('user_id')
        service = eng.get('service')
        if user_id and service:
            key = f"{user_id}:{service}"
            if key not in user_service_counts:
                user_service_counts[key] = []
            user_service_counts[key].append(eng.get('question_clicked'))
    
    print("\nUser-Service engagement patterns:")
    for key, questions in user_service_counts.items():
        user_id, service = key.split(':', 1)
        print(f"User {user_id} → {service}: {len(questions)} engagements")
        print(f"  Questions: {questions}")
        print()

def debug_premium_algorithm():
    """Test the premium detection algorithm step by step"""
    print("=== DEBUGGING PREMIUM ALGORITHM ===")
    
    # Replicate the algorithm from email_service.py
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    # MongoDB aggregation pipeline
    pipeline = [
        {
            "$match": {
                "user_id": {"$ne": None},
                "timestamp": {"$gte": week_ago}
            }
        },
        {
            "$group": {
                "_id": {
                    "user_id": "$user_id",
                    "service": "$service"
                },
                "count": {"$sum": 1},
                "questions": {"$addToSet": "$question_clicked"}
            }
        },
        {
            "$match": {"count": {"$gte": 2}}
        }
    ]
    
    print("Running aggregation pipeline...")
    candidates = list(db["engagements"].aggregate(pipeline))
    print(f"Raw candidates from aggregation: {len(candidates)}")
    
    for candidate in candidates:
        print(f"Candidate: {candidate}")
        user_id = candidate["_id"]["user_id"]
        service_name = candidate["_id"]["service"]
        engagement_count = candidate["count"]
        questions = candidate["questions"]
        
        print(f"  User ID: {user_id}")
        print(f"  Service: {service_name}")
        print(f"  Engagement Count: {engagement_count}")
        print(f"  Questions: {questions}")
        
        # Check if user exists
        user = db["users"].find_one({"_id": {"$in": [user_id]}})
        print(f"  User found in users collection: {user is not None}")
        if user:
            print(f"  User email: {user.get('email')}")
            print(f"  User name: {user.get('name')}")
        print()

def fix_user_id_format():
    """Fix potential user_id format issues"""
    print("=== CHECKING USER ID FORMATS ===")
    
    # Check user IDs in engagements
    user_ids_in_engagements = db["engagements"].distinct("user_id")
    print(f"Unique user IDs in engagements: {user_ids_in_engagements}")
    
    # Check user IDs in users collection
    users = list(db["users"].find({}, {"_id": 1, "email": 1}))
    print(f"Users in users collection:")
    for user in users:
        print(f"  ID: {user['_id']} (type: {type(user['_id'])})")
        print(f"  Email: {user.get('email')}")
    
    # Check if we need to convert user_id formats
    from bson import ObjectId
    print(f"\nChecking user_id matching...")
    for user in users:
        user_id_str = str(user['_id'])
        user_id_obj = user['_id']
        
        # Check both string and ObjectId formats
        engagements_str = db["engagements"].count_documents({"user_id": user_id_str})
        engagements_obj = db["engagements"].count_documents({"user_id": user_id_obj})
        
        print(f"User {user.get('email')}:")
        print(f"  String format matches: {engagements_str}")
        print(f"  ObjectId format matches: {engagements_obj}")

if __name__ == "__main__":
    debug_engagements()
    print("\n" + "="*50 + "\n")
    debug_premium_algorithm()
    print("\n" + "="*50 + "\n")
    fix_user_id_format()