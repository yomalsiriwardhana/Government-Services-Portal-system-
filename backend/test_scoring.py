from routes.recommendations import RecommendationEngine
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

teacher = db.users.find_one({'email': 'teacher.test@example.com'})
user_id = str(teacher['_id'])

print("User:", teacher.get('name'))
print("ID:", user_id)
print("")

# Check search history
searches = list(db.search_history.find({'user_id': teacher['_id']}))
print(f"Searches in DB: {len(searches)}")
for s in searches:
    print(f"  {s.get('query')} - gov:{s.get('is_government_search')}")
    
print("")

# Test one travel product scoring
travel_product = db.products.find_one({'title': 'International Flight Tickets - Economy Class'})
if travel_product:
    print("Testing travel product scoring:")
    print(f"Product: {travel_product.get('title')}")
    print(f"Tags: {travel_product.get('related_government_services', [])}")
    
    # Test the scoring directly
    engine = RecommendationEngine(db)
    user = db.users.find_one({'_id': ObjectId(user_id)})
    profile = db.user_profiles.find_one({'user_id': user_id}) or {}
    
    scores = engine.calculate_total_score(travel_product, user, profile, user_id)
    print(f"Total Score: {scores['total_score']:.1f}")
    print(f"Gov Search Score: {scores['government_search_intent_score']:.1f}")
else:
    print("Travel product NOT FOUND")
    
print("")

# Get top recommendations
recs = engine.get_recommendations(user_id, 6)
print(f"Top {len(recs)} recommendations:")
for i, r in enumerate(recs, 1):
    breakdown = r.get('score_breakdown', {})
    gov_score = breakdown.get('government_search_intent', 0)
    print(f"{i}. {r.get('title')}")
    print(f"   Score: {r.get('relevance_score'):.1f} (Gov: {gov_score:.1f})")
