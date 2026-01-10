"""
Helper script to get user IDs for testing recommendations
"""

from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("\n" + "=" * 60)
print("📋 SAMPLE USER IDs FOR TESTING")
print("=" * 60)

# Get users by job type
job_types = ['teacher', 'engineer', 'doctor', 'student', 'business owner']

for job in job_types:
    # Find first user of this job type
    user = db.users.find_one({'job': {'$regex': job, '$options': 'i'}})
    
    if user:
        user_id = str(user['_id'])
        name = user.get('name', 'Unknown')
        age = user.get('age', '?')
        location = user.get('location', '?')
        
        print(f"\n{job.upper()}:")
        print(f"  Name: {name}")
        print(f"  Age: {age}, Location: {location}")
        print(f"  User ID: {user_id}")
        print(f"  Test URL: http://localhost:5000/api/recommendations/test/{user_id}?limit=5")

# Get sample advertisement IDs
print("\n" + "=" * 60)
print("📢 SAMPLE ADVERTISEMENT IDs")
print("=" * 60)

ads = db.advertisements.find().limit(5)

for ad in ads:
    ad_id = str(ad['_id'])
    title = ad.get('title', 'Unknown')
    category = ad.get('category', '?')
    
    print(f"\n{category} - {title}")
    print(f"  Ad ID: {ad_id}")

print("\n" + "=" * 60)
print("✅ Copy any User ID above and use it in your tests!")
print("=" * 60)
print()