"""
Comprehensive debug to find why ads aren't updating
"""
import requests
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "=" * 80)
print("COMPREHENSIVE DEBUG - Why Ads Aren't Changing")
print("=" * 80)

# 1. Find teacher
teacher = db.users.find_one({'email': 'teacher.test@example.com'})
if not teacher:
    print("❌ Teacher not found!")
    exit(1)

user_id = str(teacher['_id'])
print(f"\n✅ Teacher found: {teacher.get('name')}")
print(f"   User ID: {user_id}")
print(f"   Job: {teacher.get('job')}")

# 2. Check search history
print("\n" + "=" * 80)
print("SEARCH HISTORY CHECK:")
print("=" * 80)

searches = list(db.search_history.find({'user_id': ObjectId(user_id)}))
print(f"Total searches: {len(searches)}")

for i, search in enumerate(searches, 1):
    print(f"\n{i}. {search.get('query')}")
    print(f"   Government: {search.get('is_government_search')}")
    print(f"   Category: {search.get('search_category')}")
    print(f"   Needs: {search.get('inferred_needs')}")

# 3. Test recommendation API directly
print("\n" + "=" * 80)
print("TESTING RECOMMENDATION ENDPOINT (without auth):")
print("=" * 80)

url = f"http://localhost:5000/api/recommendations/test/{user_id}?limit=6"
print(f"URL: {url}")

try:
    response = requests.get(url, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API works!")
        print(f"   Recommendations: {len(data.get('recommendations', []))}")
        print(f"   User profile type: {data.get('user_info', {}).get('profile_type')}")
        
        recs = data.get('recommendations', [])
        print(f"\n📺 RECOMMENDATIONS RETURNED:")
        for i, rec in enumerate(recs, 1):
            print(f"\n{i}. {rec.get('title')}")
            print(f"   Category: {rec.get('category')}")
            print(f"   Score: {rec.get('relevance_score', 0):.1f}/100")
            print(f"   Best for: {rec.get('best_for_user_types')}")
    else:
        print(f"❌ API error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Request failed: {e}")

# 4. Check what products exist for teachers
print("\n" + "=" * 80)
print("PRODUCTS TAGGED FOR TEACHERS:")
print("=" * 80)

teacher_products = list(db.products.find({
    'best_for_user_types': 'teacher'
}).limit(10))

print(f"Found {len(teacher_products)} products for teachers:")
for i, prod in enumerate(teacher_products[:5], 1):
    print(f"\n{i}. {prod.get('title')}")
    print(f"   Category: {prod.get('category')}")
    print(f"   Related services: {prod.get('related_government_services', [])}")

# 5. THE ROOT CAUSE CHECK
print("\n" + "=" * 80)
print("🎯 ROOT CAUSE ANALYSIS:")
print("=" * 80)

print("\nChecking if dashboard can access recommendations...")
print("\n⚠️  IMPORTANT: The dashboard needs to:")
print("1. Have valid JWT token in localStorage")
print("2. Call /api/recommendations (WITH auth header)")
print("3. Server must return recommendations")

print("\n📋 SOLUTION:")
print("=" * 80)
print("""
The issue is likely one of these:

1. **JWT Token Invalid/Expired**
   - Solution: Logout and login again
   
2. **Search not triggering ad refresh**
   - Solution: The search needs to happen THROUGH the dashboard search bar
   - NOT just typing in browser address bar
   
3. **Dashboard cache**
   - Solution: Hard refresh (Ctrl+Shift+R) or clear browser cache

4. **API endpoint returning wrong data**
   - Test this URL in browser (while logged in):
     http://localhost:5000/api/recommendations/test/{user_id}
""")

print("\n💡 QUICK FIX FOR YOU:")
print("=" * 80)
print("""
1. Open dashboard: http://localhost:5000/dashboard-enhanced.html
2. Open browser console (F12)
3. Type this command:
   
   localStorage.clear(); location.reload();
   
4. Login again with teacher.test@example.com / test123
5. Ads should now load correctly!

OR try the test endpoint directly in your browser:
http://localhost:5000/api/recommendations/test/""" + user_id + """

This will show you what recommendations the system is generating.
""")

print("=" * 80)
