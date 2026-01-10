"""
Complete diagnostic test for ad recommendation system
Tests the entire flow from search tracking to ad display
"""

from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

# Get teacher user
user = db.users.find_one({'email': 'teacher.test@example.com'})
user_id = str(user['_id'])

print("=" * 70)
print("DIAGNOSTIC TEST: Ad Recommendation Flow")
print("=" * 70)

# Test 1: Check if passport search exists in database
print("\n1️⃣  CHECKING SEARCH HISTORY")
print("-" * 70)
searches = list(db.search_history.find({'user_id': user_id}).sort('timestamp', -1).limit(10))
print(f"Total searches for user: {len(searches)}")
print("\nLast 5 searches:")
for i, search in enumerate(searches[:5], 1):
    print(f"  {i}. '{search.get('query')}' - {search.get('timestamp')}")
    print(f"     Category: {search.get('category', 'N/A')}")
    print(f"     Gov search: {search.get('is_government_search', False)}")

passport_searches = [s for s in searches if 'passport' in s.get('query', '').lower()]
print(f"\n✓ Passport searches found: {len(passport_searches)}")

# Test 2: Check search analyzer results
print("\n\n2️⃣  TESTING SEARCH ANALYZER")
print("-" * 70)
from utils.search_analyzer import SearchAnalyzer
analyzer = SearchAnalyzer(db)
patterns = analyzer.get_user_search_patterns(user_id, days=30)

print(f"Total searches: {patterns.get('total_searches', 0)}")
print(f"Government searches: {patterns.get('government_searches_count', 0)}")
print(f"Inferred needs: {patterns.get('inferred_needs', [])}")
print(f"Recent searches count: {len(patterns.get('recent_searches', []))}")

gov_searches = [s for s in patterns.get('recent_searches', []) if s.get('is_government_search')]
print(f"\n✓ Government searches detected: {len(gov_searches)}")
if gov_searches:
    print("  Recent government searches:")
    for gs in gov_searches[:3]:
        print(f"    - '{gs.get('query')}' (category: {gs.get('search_category')})")

# Test 3: Test recommendation engine
print("\n\n3️⃣  TESTING RECOMMENDATION ENGINE")
print("-" * 70)
from routes.recommendations import RecommendationEngine

engine = RecommendationEngine(db)
recommendations = engine.get_recommendations(user_id, limit=6)

print(f"Total recommendations: {len(recommendations)}")
print("\nTop 6 recommendations:")
for i, rec in enumerate(recommendations, 1):
    title = rec.get('title', 'Unknown')
    score = rec.get('relevance_score', 0)
    gov_services = rec.get('related_government_services', [])
    print(f"  {i}. {title[:50]}")
    print(f"     Score: {score} | Services: {', '.join(gov_services[:3])}")

# Check if passport products are in top 6
passport_in_top = [r for r in recommendations if 'passport' in str(r.get('related_government_services', [])).lower()]
print(f"\n✓ Passport products in top 6: {len(passport_in_top)}")

# Test 4: Check product scores
print("\n\n4️⃣  DETAILED SCORING FOR PASSPORT PRODUCTS")
print("-" * 70)
all_products = list(db.products.find({'is_active': {'$ne': False}}))
passport_products = [p for p in all_products if 'passport' in str(p.get('related_government_services', [])).lower()]

print(f"Total passport products in DB: {len(passport_products)}")

# Score top 3 passport products manually
from models.user import User
user_model = User(db)
user_obj = user_model.find_by_id(user_id)

print("\nScoring first 3 passport products:")
for i, product in enumerate(passport_products[:3], 1):
    # Simulate scoring
    score = 50
    if gov_searches:
        search_keywords = set()
        for search in gov_searches[:5]:
            query = search.get('query', '').lower()
            search_keywords.update(query.split())
        
        product_gov_services = product.get('related_government_services', [])
        matched = 0
        for keyword in search_keywords:
            for service in product_gov_services:
                if keyword in service.lower() or service.lower() in keyword:
                    score += 50
                    matched += 1
                    break
        
        print(f"  {i}. {product['title'][:50]}")
        print(f"     Base: 50 | Keywords matched: {matched} | Final score: {score}")
        print(f"     Services: {product_gov_services}")

# Summary
print("\n\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✓ Searches tracked: {len(searches) > 0}")
print(f"✓ Passport searches exist: {len(passport_searches) > 0}")
print(f"✓ Government searches detected: {len(gov_searches) > 0}")
print(f"✓ Recommendations generated: {len(recommendations) > 0}")
print(f"✓ Passport products in top 6: {len(passport_in_top) > 0}")

if len(passport_in_top) == 0:
    print("\n⚠️  PROBLEM FOUND: Passport products NOT in top recommendations!")
    print("   Possible causes:")
    print("   1. Search not properly tagged as government search")
    print("   2. Scoring algorithm not matching keywords")
    print("   3. Non-passport products scoring higher")
else:
    print("\n✅ SUCCESS: Passport products ARE in recommendations!")
    print("   The backend is working correctly.")
    print("   Problem might be in frontend caching or API call.")
