"""
Test Government Context-Aware Advertisement System
Tests the 4 scenarios mentioned by the user
"""

from pymongo import MongoClient
from bson import ObjectId
import requests
import json

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "=" * 80)
print("🧪 TESTING CONTEXT-AWARE ADVERTISEMENT SYSTEM")
print("=" * 80)

# Test configuration
API_BASE = "http://localhost:5000/api"

def get_or_create_test_user(job, name, age=30):
    """Get or create a test user with specific job"""
    user = db.users.find_one({'job': {'$regex': job, '$options': 'i'}})
    
    if not user:
        print(f"⚠️  No {job} found in database")
        return None
    
    user_id = str(user['_id'])
    user_name = user.get('name', name)
    print(f"✅ Found user: {user_name} ({job}) - ID: {user_id}")
    return user_id, user

def simulate_government_search(user_id, search_query, search_category):
    """Simulate a government service search"""
    print(f"\n🔍 Simulating search: '{search_query}'")
    
    # Track search in database
    from utils.search_analyzer import SearchAnalyzer
    analyzer = SearchAnalyzer(db)
    
    # Analyze search intent
    intent_analysis = analyzer.analyze_search_query(user_id, search_query)
    
    # Track the search
    search_id = analyzer.track_search(
        user_id,
        search_query,
        'government_service',
        10,  # mock results count
        intent_analysis
    )
    
    print(f"   ✓ Search tracked (ID: {search_id})")
    print(f"   ✓ Government search: {intent_analysis.get('is_government_search')}")
    print(f"   ✓ Category: {intent_analysis.get('search_category')}")
    print(f"   ✓ Inferred needs: {', '.join(intent_analysis.get('inferred_needs', []))}")
    
    return intent_analysis

def get_recommendations(user_id):
    """Get personalized ad recommendations"""
    url = f"{API_BASE}/recommendations/test/{user_id}?limit=5"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('recommendations', [])
        else:
            print(f"❌ Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Request failed: {e}")
        # Fallback: use recommendation engine directly
        from routes.recommendations import RecommendationEngine
        engine = RecommendationEngine(db)
        return engine.get_recommendations(user_id, limit=5)

def display_ads(recommendations, scenario_name):
    """Display recommended ads"""
    print(f"\n📺 DASHBOARD ADS for {scenario_name}:")
    print("-" * 80)
    
    if not recommendations:
        print("   ⚠️  No recommendations found")
        return
    
    for i, ad in enumerate(recommendations, 1):
        title = ad.get('title', 'Unknown')
        category = ad.get('category', 'N/A')
        price = ad.get('price', 0)
        score = ad.get('relevance_score', 0)
        
        score_breakdown = ad.get('score_breakdown', {})
        gov_score = score_breakdown.get('government_search_intent', 0)
        
        print(f"\n   {i}. {title}")
        print(f"      Category: {category} | Price: Rs. {price:,}")
        print(f"      Relevance Score: {score:.1f}/100")
        print(f"      Government Search Score: {gov_score:.1f}/25")
        
        # Show why it was recommended
        solves = ad.get('solves_user_needs', [])
        if solves:
            print(f"      Solves: {', '.join(solves[:3])}")

print("\n" + "=" * 80)
print("SCENARIO 1: Teacher Searches O/L Results")
print("=" * 80)

# Get teacher user
teacher_id, teacher_user = get_or_create_test_user('teacher', 'Ms. Silva')

if teacher_id:
    # Simulate O/L search
    simulate_government_search(teacher_id, "How to check O/L results", "ol_examination")
    
    # Get recommendations
    ads = get_recommendations(teacher_id)
    display_ads(ads, "Teacher after O/L search")
    
    print("\n✅ Expected ads: Degree programs, Professional courses, Teaching materials")

print("\n" + "=" * 80)
print("SCENARIO 2: Software Engineer Searches O/L Results (has children)")
print("=" * 80)

# Get software engineer user
engineer_id, engineer_user = get_or_create_test_user('software engineer', 'Mr. Fernando')

if engineer_id:
    # Simulate O/L search
    simulate_government_search(engineer_id, "O/L results check", "ol_examination")
    
    # Get recommendations
    ads = get_recommendations(engineer_id)
    display_ads(ads, "Software Engineer after O/L search")
    
    print("\n✅ Expected ads: O/L past papers, Tuition classes, Educational apps")

print("\n" + "=" * 80)
print("SCENARIO 3: Software Engineer Searches Passport")
print("=" * 80)

if engineer_id:
    # Simulate passport search
    simulate_government_search(engineer_id, "How to get passport", "passport_immigration")
    
    # Get recommendations
    ads = get_recommendations(engineer_id)
    display_ads(ads, "Software Engineer after Passport search")
    
    print("\n✅ Expected ads: Air tickets, Travel services, Visa assistance")

print("\n" + "=" * 80)
print("SCENARIO 4: Teacher Searches Driving License")
print("=" * 80)

if teacher_id:
    # Simulate driving license search
    simulate_government_search(teacher_id, "How to apply for driving license", "driving_license")
    
    # Get recommendations
    ads = get_recommendations(teacher_id)
    display_ads(ads, "Teacher after Driving License search")
    
    print("\n✅ Expected ads: Degree programs, Car advertisements, Driving school")

print("\n" + "=" * 80)
print("✅ ALL SCENARIOS TESTED")
print("=" * 80)

# Summary statistics
print("\n📊 SYSTEM STATISTICS:")
print(f"   • Total users: {db.users.count_documents({})}")
print(f"   • Total products: {db.products.count_documents({})}")
print(f"   • Government-tagged products: {db.products.count_documents({'related_government_services': {'$exists': True}})}")
print(f"   • Search mappings: {db.search_to_product_mappings.count_documents({})}")
print(f"   • Search history entries: {db.search_history.count_documents({})}")

print("\n" + "=" * 80)
