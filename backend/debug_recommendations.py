from routes.recommendations import RecommendationEngine
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

# Get teacher
teacher = db.users.find_one({'email': 'teacher.test@example.com'})
user_id = str(teacher['_id'])

print("="*60)
print("TESTING: Why ads aren't changing")
print("="*60)

# Check searches
searches = list(db.search_history.find({'user_id': teacher['_id']}).sort('timestamp', -1))
print(f"\nUser ID: {user_id}")
print(f"Total searches: {len(searches)}")
print("\nRecent searches:")
for s in searches[:5]:
    print(f"  - {s.get('query')}")
    print(f"    Government: {s.get('is_government_search')}")
    print(f"    Category: {s.get('search_category')}")

# Get recommendations
print("\n" + "="*60)
print("CURRENT RECOMMENDATIONS:")
print("="*60)

engine = RecommendationEngine(db)
recs = engine.get_recommendations(user_id, 6)

for i, rec in enumerate(recs, 1):
    title = rec.get('title')
    score = rec.get('relevance_score', 0)
    category = rec.get('category')
    breakdown = rec.get('score_breakdown', {})
    gov_score = breakdown.get('government_search_intent', 0)
    
    print(f"\n{i}. {title}")
    print(f"   Category: {category}")
    print(f"   Total Score: {score:.1f}/100")
    print(f"   Gov Search Score: {gov_score:.1f}/25")

# Check travel products
print("\n" + "="*60)
print("TRAVEL PRODUCTS IN DATABASE:")
print("="*60)

travel_products = list(db.products.find({
    'related_government_services': {'$in': ['passport']}
}).limit(5))

print(f"Total travel products (passport tag): {len(travel_products)}")
for p in travel_products:
    print(f"  - {p.get('title')}")

print("\n" + "="*60)
