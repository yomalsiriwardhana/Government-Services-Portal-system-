from pymongo import MongoClient
from utils.search_analyzer import SearchAnalyzer

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

teacher = db.users.find_one({'email': 'teacher.test@example.com'})
user_id = str(teacher['_id'])

# Check what search patterns look like
analyzer = SearchAnalyzer(db)
patterns = analyzer.get_user_search_patterns(user_id, days=30)

print("Search Patterns:")
print(f"Recent searches: {len(patterns.get('recent_searches', []))}")

for s in patterns.get('recent_searches', [])[:5]:
    print(f"\nQuery: {s.get('query')}")
    print(f"  Category: {s.get('search_category')}")
    print(f"  Inferred needs: {s.get('inferred_needs', [])}")
    print(f"  Related services: {s.get('related_services', [])}")
    
print(f"\nAll inferred needs: {patterns.get('inferred_needs', [])}")
