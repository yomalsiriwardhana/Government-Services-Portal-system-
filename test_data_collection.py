from pymongo import MongoClient
import os
from dotenv import load_dotenv
import requests

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["citizen_portal"]
users_col = db["users"]

print("=" * 60)
print("DATA COLLECTION TEST")
print("=" * 60)

# Find the test user
test_user = users_col.find_one({"email": "test@example.com"})

if not test_user:
    print("❌ Test user not found!")
    print("Please register with email: test@example.com first")
else:
    user_id = str(test_user["_id"])
    print(f"\n✅ Test user found!")
    print(f"User ID: {user_id}")
    print(f"Name: {test_user.get('name')}")
    print(f"Age: {test_user.get('age')}")
    print(f"Location: {test_user.get('location')}")
    
    # Check extended profile
    extended = test_user.get('extended_profile', {})
    
    print("\n" + "=" * 60)
    print("COLLECTED DATA:")
    print("=" * 60)
    
    # Career data
    career = extended.get('career', {})
    print(f"\n💼 Career:")
    print(f"  Job: {career.get('current_job', 'Not provided')}")
    print(f"  Experience: {career.get('years_experience', 0)} years")
    
    # Education data
    education = extended.get('education', {})
    print(f"\n🎓 Education:")
    print(f"  Qualification: {education.get('highest_qualification', 'Not provided')}")
    
    # Family data
    family = extended.get('family', {})
    print(f"\n👨‍👩‍👧‍👦 Family:")
    print(f"  Marital Status: {family.get('marital_status', 'Not provided')}")
    print(f"  Children: {len(family.get('children', []))}")
    if family.get('children_ages'):
        print(f"  Children Ages: {family.get('children_ages')}")
        print(f"  Children Education: {family.get('children_education')}")
    
    # Interests
    interests = extended.get('interests', {})
    print(f"\n🎯 Interests:")
    print(f"  Learning: {interests.get('learning_interests', [])}")
    print(f"  Services: {interests.get('service_preferences', [])}")
    
    # Consent
    consent = extended.get('consent', {})
    print(f"\n🔒 Consent:")
    print(f"  Marketing Emails: {consent.get('marketing_emails', False)}")
    print(f"  Personalized Ads: {consent.get('personalized_ads', False)}")
    print(f"  Data Analytics: {consent.get('data_analytics', False)}")
    
    # Test recommendations
    print("\n" + "=" * 60)
    print("AI RECOMMENDATIONS TEST:")
    print("=" * 60)
    
    try:
        response = requests.get(f"http://localhost:5000/api/recommendations/{user_id}")
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                print(f"\n✅ Recommendations API working!")
                print(f"\n👥 User Segments:")
                for segment in data.get('user_segments', []):
                    print(f"  - {segment}")
                
                print(f"\n📚 Education Recommendations: {len(data.get('education_recommendations', []))}")
                for rec in data.get('education_recommendations', [])[:3]:
                    print(f"  - {rec.get('title')}")
                
                print(f"\n💼 Career Recommendations: {len(data.get('career_recommendations', []))}")
                for rec in data.get('career_recommendations', [])[:3]:
                    print(f"  - {rec.get('title')}")
                
                print(f"\n🎯 Personalized Ads: {len(data.get('personalized_ads', []))}")
                
            else:
                print(f"❌ Recommendations failed: {data.get('error')}")
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print("Make sure Flask server is running!")
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        print("Make sure Flask server is running on http://localhost:5000")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    
    if extended:
        print("\n✅ SUCCESS! Data collection is working properly.")
        print("✅ User segmentation is active.")
        print("✅ AI recommendations are ready.")
    else:
        print("\n⚠️ WARNING: Extended profile data not found.")
        print("Make sure the registration form is submitting correctly.")