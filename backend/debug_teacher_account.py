"""
Debug script to check if search was tracked and recommendations work
"""
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "=" * 70)
print("DEBUGGING: New Teacher Account")
print("=" * 70)

# Find the newly created teacher
teacher = db.users.find_one({'email': 'teacher.test@example.com'})

if not teacher:
    print("❌ User not found!")
    exit(1)

user_id = str(teacher['_id'])
print(f"\n✅ Found user: {teacher.get('name')}")
print(f"   User ID: {user_id}")
print(f"   Job: {teacher.get('job')}")
print(f"   Age: {teacher.get('age')}")

# Check search history
print("\n" + "=" * 70)
print("SEARCH HISTORY:")
print("=" * 70)

searches = list(db.search_history.find({'user_id': ObjectId(user_id)}).sort('timestamp', -1).limit(5))

if searches:
    for i, search in enumerate(searches, 1):
        print(f"\n{i}. Query: {search.get('query')}")
        print(f"   Government Search: {search.get('is_government_search')}")
        print(f"   Category: {search.get('search_category')}")
        print(f"   Inferred Needs: {search.get('inferred_needs', [])}")
else:
    print("\n❌ No search history found!")
    print("   This is the problem - search wasn't tracked properly")

# Test recommendation API directly
print("\n" + "=" * 70)
print("TESTING RECOMMENDATION ENGINE:")
print("=" * 70)

from routes.recommendations import RecommendationEngine

engine = RecommendationEngine(db)
recommendations = engine.get_recommendations(user_id, limit=5)

print(f"\n✅ Got {len(recommendations)} recommendations:")

for i, rec in enumerate(recommendations, 1):
    title = rec.get('title', 'Unknown')
    score = rec.get('relevance_score', 0)
    category = rec.get('category', 'N/A')
    
    score_breakdown = rec.get('score_breakdown', {})
    gov_score = score_breakdown.get('government_search_intent', 0)
    
    print(f"\n{i}. {title}")
    print(f"   Category: {category}")
    print(f"   Total Score: {score:.1f}/100")
    print(f"   Gov Search Score: {gov_score:.1f}/25")
    print(f"   Best For: {rec.get('best_for_user_types', [])}")

print("\n" + "=" * 70)
print("RECOMMENDATION API URL:")
print("=" * 70)
print(f"\nTest this URL in your browser:")
print(f"http://localhost:5000/api/recommendations/test/{user_id}?limit=5")
print("\nOr with authentication:")
print(f"http://localhost:5000/api/recommendations")
print("(Must be logged in)")

print("\n" + "=" * 70)
