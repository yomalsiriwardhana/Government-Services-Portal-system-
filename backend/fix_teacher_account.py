"""
Fix for new teacher account - manually add search history
"""
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

# Find the teacher
teacher = db.users.find_one({'email': 'teacher.test@example.com'})

if not teacher:
    print("❌ Teacher account not found")
    exit(1)

user_id = teacher['_id']
print(f"✅ Found teacher: {teacher.get('name')}")
print(f"   User ID: {user_id}")

# Add O/L search to history
search_record = {
    'user_id': user_id,
    'query': 'How to check O/L results',
    'search_type': 'government_service',
    'results_count': 10,
    'timestamp': datetime.utcnow(),
    'is_government_search': True,
    'search_category': 'ol_examination',
    'inferred_needs': ['exam_preparation', 'child_education', 'professional_development'],
    'confidence_score': 0.95,
    'clicked_results': []
}

# Insert search
result = db.search_history.insert_one(search_record)
print(f"\n✅ Added O/L search to history (ID: {result.inserted_id})")

# Verify
searches = list(db.search_history.find({'user_id': user_id}))
print(f"\n📊 Total searches for this user: {len(searches)}")

# Test recommendations
print("\n" + "=" * 70)
print("TESTING RECOMMENDATIONS:")
print("=" * 70)

from routes.recommendations import RecommendationEngine

engine = RecommendationEngine(db)
recommendations = engine.get_recommendations(str(user_id), limit=6)

print(f"\n✅ Got {len(recommendations)} recommendations:")

for i, rec in enumerate(recommendations, 1):
    title = rec.get('title', 'Unknown')
    score = rec.get('relevance_score', 0)
    gov_score = rec.get('score_breakdown', {}).get('government_search_intent', 0)
    
    print(f"\n{i}. {title}")
    print(f"   Total Score: {score:.1f}/100")
    print(f"   Gov Search Score: {gov_score:.1f}/25")
    print(f"   Category: {rec.get('category')}")

print("\n" + "=" * 70)
print("✅ FIX APPLIED!")
print("=" * 70)
print("\n📋 Now try these steps:")
print("1. Go to: http://localhost:5000/dashboard-enhanced.html")
print("2. You should see personalized ads for teachers!")
print("3. Expected ads:")
print("   - Bachelor/Master's degree programs")
print("   - Professional development courses")
print("   - Educational technology")
print("\n" + "=" * 70)
