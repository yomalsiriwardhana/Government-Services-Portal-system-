from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]

# Collections
services_col = db["services"]
categories_col = db["categories"]
officers_col = db["officers"]
ads_col = db["ads"]

# Clear new collections only (keep existing services!)
categories_col.delete_many({})
officers_col.delete_many({})
ads_col.delete_many({})

# Seed Categories
categories = [
    {
        "id": "cat_it",
        "name": {
            "en": "IT & Digital",
            "si": "තොරතුරු තාක්ෂණ",
            "ta": "தகவல் தொழில்நுட்பம்"
        },
        "ministry_ids": ["ministry_it"]
    },
    {
        "id": "cat_education",
        "name": {
            "en": "Education",
            "si": "අධ්‍යාපන",
            "ta": "கல்வி"
        },
        "ministry_ids": ["ministry_education"]
    },
    {
        "id": "cat_health",
        "name": {
            "en": "Health",
            "si": "සෞඛ්‍ය",
            "ta": "சுகாதாரம்"
        },
        "ministry_ids": ["ministry_health"]
    },
    {
        "id": "cat_transport",
        "name": {
            "en": "Transport",
            "si": "ප්‍රවාහන",
            "ta": "போக்குவரத்து"
        },
        "ministry_ids": ["ministry_transport"]
    },
    {
        "id": "cat_public",
        "name": {
            "en": "Public Administration",
            "si": "පොදු පරිපාලන",
            "ta": "பொது நிர்வாகம்"
        },
        "ministry_ids": ["ministry_public"]
    }
]

categories_col.insert_many(categories)
print(f"✅ Inserted {len(categories)} categories")

# Seed Officers
officers = [
    {
        "id": "off_it_01",
        "name": "Ms. Nayana Perera",
        "role": "Director - Digital Services",
        "ministry_id": "ministry_it",
        "contact": {
            "email": "nayana@it.gov.lk",
            "phone": "071-1234567"
        }
    },
    {
        "id": "off_edu_01",
        "name": "Mr. Ruwan Silva",
        "role": "Assistant Secretary - Education",
        "ministry_id": "ministry_education",
        "contact": {
            "email": "ruwan@edu.gov.lk",
            "phone": "071-7654321"
        }
    }
]

officers_col.insert_many(officers)
print(f"✅ Inserted {len(officers)} officers")

# Seed Ads/Announcements
ads = [
    {
        "id": "ad_courses_01",
        "title": "Free Digital Skills Course",
        "body": "Enroll now for government digital skills training. Limited seats available!",
        "link": "https://example.gov.lk/courses",
        "start": None,
        "end": None,
        "image": "/static/img/course-card.png"
    },
    {
        "id": "ad_exams_01",
        "title": "Exam Results Portal",
        "body": "Check your latest exam results online",
        "link": "https://exam.gov.lk/results",
        "start": None,
        "end": None,
        "image": None
    },
    {
        "id": "ad_health_01",
        "title": "Health Services Update",
        "body": "New clinic registration process now available",
        "link": "#",
        "start": None,
        "end": None,
        "image": None
    }
]

ads_col.insert_many(ads)
print(f"✅ Inserted {len(ads)} ads")

# Update existing services to add category field
services_col.update_one({"id": "ministry_it"}, {"$set": {"category": "cat_it"}})
services_col.update_one({"id": "ministry_education"}, {"$set": {"category": "cat_education"}})
services_col.update_one({"id": "ministry_health"}, {"$set": {"category": "cat_health"}})
services_col.update_one({"id": "ministry_transport"}, {"$set": {"category": "cat_transport"}})

print("✅ Updated services with categories")
print("\n🎉 Seed v2 complete! New collections ready.")