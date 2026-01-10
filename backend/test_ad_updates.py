"""
Test if search tracking and ad updates are working end-to-end
"""
from pymongo import MongoClient
from bson import ObjectId
import requests

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "="*80)
print("TESTING: Context-Aware Ads - Complete Flow")
print("="*80)

# 1. Find teacher
teacher = db.users.find_one({'email': 'teacher.test@example.com'})
if not teacher:
    print("\n❌ Teacher account not found!")
    print("Please create it first with: python create_teacher_test_user.py")
    exit(1)

user_id = str(teacher['_id'])
print(f"\n✅ Teacher found: {teacher.get('name')}")
print(f"   User ID: {user_id}")
print(f"   Job: {teacher.get('job')}")

# 2. Check current search history
print("\n" + "="*80)
print("STEP 1: Checking current search history")
print("="*80)

searches = list(db.search_history.find({'user_id': ObjectId(user_id)}).sort('timestamp', -1))
print(f"\n📊 Total searches in database: {len(searches)}")

if searches:
    print("\nRecent searches:")
    for i, s in enumerate(searches[:5], 1):
        print(f"{i}. {s.get('query')}")
        print(f"   Government: {s.get('is_government_search')}")
        print(f"   Category: {s.get('search_category')}")
else:
    print("\n⚠️  No searches found - this explains why ads aren't changing!")

# 3. Test recommendations BEFORE adding search
print("\n" + "="*80)
print("STEP 2: Get recommendations BEFORE passport search")
print("="*80)

from routes.recommendations import RecommendationEngine

engine = RecommendationEngine(db)
recs_before = engine.get_recommendations(user_id, limit=6)

print(f"\n📦 Got {len(recs_before)} recommendations BEFORE search:\n")
for i, rec in enumerate(recs_before, 1):
    title = rec.get('title', 'Unknown')
    score = rec.get('relevance_score', 0)
    breakdown = rec.get('score_breakdown', {})
    gov_score = breakdown.get('government_search_intent', 0)
    
    print(f"{i}. {title}")
    print(f"   Total: {score:.1f}/100 | Gov Intent: {gov_score:.1f}/25")

# 4. Add a "passport" search
print("\n" + "="*80)
print("STEP 3: Adding 'passport' search to history")
print("="*80)

from utils.search_analyzer import SearchAnalyzer
from datetime import datetime

analyzer = SearchAnalyzer(db)

# Analyze the search
passport_query = "how to get a passport"
intent = analyzer.analyze_search_query(user_id, passport_query)

print(f"\n🔍 Search: '{passport_query}'")
print(f"   Government: {intent.get('is_government_search')}")
print(f"   Category: {intent.get('search_category')}")
print(f"   Services: {intent.get('related_services', [])}")
print(f"   Needs: {intent.get('inferred_needs', [])}")

# Track it
search_id = analyzer.track_search(
    user_id,
    passport_query,
    'government_service',
    5,  # Results count
    intent
)

print(f"\n✅ Search tracked! ID: {search_id}")

# 5. Test recommendations AFTER adding search
print("\n" + "="*80)
print("STEP 4: Get recommendations AFTER passport search")
print("="*80)

recs_after = engine.get_recommendations(user_id, limit=6)

print(f"\n📦 Got {len(recs_after)} recommendations AFTER search:\n")
for i, rec in enumerate(recs_after, 1):
    title = rec.get('title', 'Unknown')
    score = rec.get('relevance_score', 0)
    breakdown = rec.get('score_breakdown', {})
    gov_score = breakdown.get('government_search_intent', 0)
    
    print(f"{i}. {title}")
    print(f"   Total: {score:.1f}/100 | Gov Intent: {gov_score:.1f}/25")

# 6. Compare
print("\n" + "="*80)
print("STEP 5: COMPARISON")
print("="*80)

before_titles = [r.get('title') for r in recs_before]
after_titles = [r.get('title') for r in recs_after]

print("\n📊 Before search:")
for i, t in enumerate(before_titles, 1):
    print(f"   {i}. {t}")

print("\n📊 After search:")
for i, t in enumerate(after_titles, 1):
    marker = "← NEW!" if t not in before_titles else ""
    print(f"   {i}. {t} {marker}")

changed = before_titles != after_titles
if changed:
    print("\n✅ SUCCESS! Ads changed after search!")
else:
    print("\n⚠️  WARNING: Ads didn't change")
    print("   Possible reasons:")
    print("   1. No travel products in database")
    print("   2. Travel products not tagged with 'passport' service")
    print("   3. Scoring weights too low")

# 7. Check travel products
print("\n" + "="*80)
print("STEP 6: Checking travel products in database")
print("="*80)

travel_products = list(db.products.find({
    'related_government_services': {'$in': ['passport', 'visa', 'immigration']}
}))

print(f"\n📦 Found {len(travel_products)} travel-related products:")
for p in travel_products:
    print(f"   • {p.get('title')}")
    print(f"     Services: {p.get('related_government_services', [])}")

if len(travel_products) == 0:
    print("\n❌ PROBLEM FOUND: No travel products in database!")
    print("   Run: python run_government_context_setup.py")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

if changed and len(travel_products) >0:
    print("\n✅ System is working correctly!")
    print("   Ads change based on searches.")
elif len(travel_products) == 0:
    print("\n❌ Missing travel products in database")
    print("   Fix: python run_government_context_setup.py")
else:
    print("\n⚠️  System partially working")
    print("   Backend logic OK, but ads not changing enough")
    print("   May need to adjust scoring weights")

print("\n" + "="*80)
