from pymongo import MongoClient
from datetime import datetime
from config import Config

# Connect to MongoDB
client = MongoClient(Config.MONGO_URI)
db = client.government_portal

# Clear existing announcements
db.announcements.delete_many({})
print("Cleared existing announcements")

# Sample announcements
announcements = [
    {
        'title': 'New Online Service Portal Launched',
        'content': 'We are excited to announce the launch of our new online service portal. Citizens can now apply for various government services from the comfort of their homes.',
        'type': 'general',
        'priority': 'high',
        'status': 'active',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Public Holiday Notice',
        'content': 'All government offices will be closed on December 25th for the Christmas holiday. Emergency services will remain operational.',
        'type': 'notice',
        'priority': 'normal',
        'status': 'active',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'Tax Filing Deadline Extended',
        'content': 'The deadline for annual tax filing has been extended to January 31st, 2026. Please ensure all documents are submitted before the new deadline.',
        'type': 'important',
        'priority': 'high',
        'status': 'active',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'New Driver\'s License Requirements',
        'content': 'Starting next month, all new driver\'s license applicants must complete an online safety course before their road test.',
        'type': 'update',
        'priority': 'normal',
        'status': 'active',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    },
    {
        'title': 'COVID-19 Vaccination Drive',
        'content': 'Free COVID-19 vaccination boosters are now available at all district health centers. Walk-ins are welcome.',
        'type': 'health',
        'priority': 'high',
        'status': 'active',
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }
]

# Insert announcements
result = db.announcements.insert_many(announcements)
print(f"✅ Inserted {len(result.inserted_ids)} announcements")

# Display inserted announcements
print("\nInserted Announcements:")
for announcement in announcements:
    print(f"  - {announcement['title']}")

print("\n✅ Announcement seeding completed!")

client.close()