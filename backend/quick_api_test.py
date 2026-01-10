"""
Quick test to see what the API actually returns
"""
import requests

# Get teacher user ID from database
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal
user = db.users.find_one({'email': 'teacher.test@example.com'})
user_id = str(user['_id'])

print(f"Testing for user: {user['name']} ({user_id})")

# Track a passport search first
print("\n1. Tracking passport search...")
response = requests.post(
    'http://localhost:5000/api/search/track',
    json={
        'query': 'passport',
        'user_id': user_id,
        'category': 'government'
    }
)
print(f"   Status: {response.status_code}")

# Get recommendations (need JWT token, let's use test endpoint instead)
print("\n2. Getting recommendations...")
response = requests.get(
    f'http://localhost:5000/api/products/',
)
if response.status_code == 200:
    data = response.json()
    print(f"   Total products available: {len(data.get('products', []))}")
    
    # Check passport products
    passport_products = [p for p in data.get('products', []) 
                        if 'passport' in str(p.get('related_government_services', [])).lower()]
    print(f"   Passport products: {len(passport_products)}")
    if passport_products:
        print("\n   First 3 passport products:")
        for p in passport_products[:3]:
            print(f"     - {p['title']}")

print("\n3. Checking search history...")
searches = list(db.search_history.find({'user_id': user_id}).sort('timestamp', -1).limit(3))
print(f"   Last 3 searches:")
for s in searches:
    print(f"     - '{s.get('query')}' (gov: {s.get('is_government_search', False)})")

print("\n✅ Test complete. Check Flask console for DEBUG output from recommendations.py")
print("   Look for lines like: 'DEBUG: Passport product ... scored'")
print("   and 'DEBUG: Top 3 products:'")
