import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Test MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
print(f"Attempting to connect to: {MONGO_URI}")

try:
    client = MongoClient(MONGO_URI)
    # Test the connection
    client.admin.command('ping')
    print("✅ MongoDB connection successful!")
    
    # Check database and collections
    db = client["citizen_portal"]
    services_col = db["services"]
    engagements_col = db["engagements"]
    admins_col = db["admins"]
    
    # Count documents
    services_count = services_col.count_documents({})
    engagements_count = engagements_col.count_documents({})
    admins_count = admins_col.count_documents({})
    
    print(f"📊 Services collection has {services_count} documents")
    print(f"👥 Engagements collection has {engagements_count} documents")
    print(f"🔑 Admins collection has {admins_count} documents")
    
    if services_count == 0:
        print("❌ Services database is empty - need to run seed_data.py")
    else:
        # Show first service
        first_service = services_col.find_one()
        print(f"📋 First service: {first_service.get('name', {}).get('en', 'Unknown')}")
    
    if engagements_count > 0:
        # Show latest engagement
        latest = engagements_col.find_one(sort=[("timestamp", -1)])
        print(f"🔄 Latest engagement: {latest.get('question_clicked', 'Unknown')} by age {latest.get('age', 'N/A')}")
    else:
        print("❌ No engagement data - admin dashboard will be empty")
        
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nPossible solutions:")
    print("1. Check your MONGO_URI in .env file")
    print("2. Verify password and cluster URL")
    print("3. Check network access settings in Atlas")
    print("4. Ensure IP address is whitelisted")