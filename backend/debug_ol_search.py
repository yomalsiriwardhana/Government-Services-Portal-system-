"""Debug O/L results search issue"""
from pymongo import MongoClient

db = MongoClient('mongodb://localhost:27017/').government_portal

print("=" * 60)
print("DEBUG: O/L Results Search Issue")
print("=" * 60)

# Check products with education/O/L tags
print("\n1. Products with education-related tags:")
education_products = list(db.products.find({
    'related_government_services': {'$in': ['o/l results', 'education', 'a/l results']}
}))
print(f"   Found: {len(education_products)} products")
for p in education_products[:5]:
    print(f"   - {p.get('title', 'N/A')[:50]}")
    print(f"     Tags: {p.get('related_government_services', [])}")

# Check advertisements with education tags
print("\n2. Advertisements with education-related tags:")
education_ads = list(db.advertisements.find({
    'related_government_services': {'$in': ['o/l results', 'education', 'a/l results']}
}))
print(f"   Found: {len(education_ads)} ads")
for a in education_ads[:5]:
    print(f"   - {a.get('title', 'N/A')[:50]}")
    print(f"     Tags: {a.get('related_government_services', [])}")

# Check recent searches
print("\n3. Recent searches tracked:")
recent_searches = list(db.search_history.find({}).sort('timestamp', -1).limit(5))
for s in recent_searches:
    print(f"   - '{s.get('query', 'N/A')}' at {s.get('timestamp', 'N/A')}")

# Check if any products have 'past paper' or 'tuition' in title
print("\n4. Products with 'past paper', 'tuition', or 'exam' in title:")
tuition_products = list(db.products.find({
    '$or': [
        {'title': {'$regex': 'past paper', '$options': 'i'}},
        {'title': {'$regex': 'tuition', '$options': 'i'}},
        {'title': {'$regex': 'exam', '$options': 'i'}},
        {'title': {'$regex': 'o/l', '$options': 'i'}},
        {'title': {'$regex': 'education', '$options': 'i'}},
    ]
}))
print(f"   Found: {len(tuition_products)} products")
for p in tuition_products[:10]:
    print(f"   - {p.get('title', 'N/A')}")

print("\n5. ALL products in database (first 10):")
all_products = list(db.products.find({}).limit(10))
for p in all_products:
    print(f"   - {p.get('title', 'N/A')[:40]} | cat: {p.get('category', 'N/A')}")

print("\n" + "=" * 60)
