"""
Sample Product Creator
Run this script to add sample products/ads to your database for testing
"""

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["citizen_portal"]
products_col = db["products"]

# Sample products
sample_products = [
    {
        "title": "O/L Past Papers 2024 - All Subjects",
        "description": "Complete collection of O/L past papers with answers. Perfect for exam preparation.",
        "category": "education",
        "price": 1500.00,
        "image_url": None,
        "link": "https://example.com/ol-papers",
        "target_categories": ["student", "education_seeker", "secondary_school_parent", "ol_prep_parent"],
        "target_age_min": 14,
        "target_age_max": 18,
        "target_locations": [],
        "interests": ["Education"],
        "status": "active",
        "featured": True,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Python Programming Course - Beginner to Advanced",
        "description": "Learn Python from scratch. Includes video lessons, exercises, and certificate.",
        "category": "courses",
        "price": 9999.00,
        "image_url": None,
        "link": "https://example.com/python-course",
        "target_categories": ["tech_enthusiast", "course_buyer", "job_seeker", "early_career"],
        "target_age_min": 18,
        "target_age_max": 35,
        "target_locations": [],
        "interests": ["Technology", "Education"],
        "status": "active",
        "featured": True,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Dell Laptop - i5 11th Gen, 8GB RAM, 512GB SSD",
        "description": "Brand new laptop perfect for students and professionals. Fast performance guaranteed.",
        "category": "electronics",
        "price": 125000.00,
        "image_url": None,
        "link": "https://example.com/dell-laptop",
        "target_categories": ["tech_enthusiast", "electronics_buyer", "student", "professional"],
        "target_age_min": 18,
        "target_age_max": 45,
        "target_locations": ["Colombo", "Gampaha", "Kandy"],
        "interests": ["Technology"],
        "status": "active",
        "featured": False,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Driver's License Preparation Package",
        "description": "Complete guide to passing your driving test. Includes practice questions and tips.",
        "category": "education",
        "price": 2500.00,
        "image_url": None,
        "link": "https://example.com/driving-license",
        "target_categories": ["young_adult", "early_career"],
        "target_age_min": 18,
        "target_age_max": 30,
        "target_locations": [],
        "interests": ["Transport"],
        "status": "active",
        "featured": False,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "English Speaking Course - IELTS Preparation",
        "description": "Improve your English speaking skills. Expert trainers, flexible schedules.",
        "category": "courses",
        "price": 15000.00,
        "image_url": None,
        "link": "https://example.com/english-course",
        "target_categories": ["education_seeker", "course_buyer", "job_seeker", "travel_seeker"],
        "target_age_min": 16,
        "target_age_max": 40,
        "target_locations": [],
        "interests": ["Education", "Immigration"],
        "status": "active",
        "featured": True,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Land for Sale - 10 Perches in Gampaha",
        "description": "Prime location land for sale. Perfect for building your dream home.",
        "category": "property",
        "price": 4500000.00,
        "image_url": None,
        "link": "https://example.com/land-sale",
        "target_categories": ["property_seeker", "property_investor", "mid_career_family", "established_professional"],
        "target_age_min": 30,
        "target_age_max": 60,
        "target_locations": ["Gampaha", "Colombo", "Kalutara"],
        "interests": ["Housing"],
        "status": "active",
        "featured": False,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Scholarship Application Guide 2025",
        "description": "Step-by-step guide to applying for scholarships. Increase your chances of success.",
        "category": "education",
        "price": 999.00,
        "image_url": None,
        "link": "https://example.com/scholarship-guide",
        "target_categories": ["student", "university_age_parent", "education_seeker"],
        "target_age_min": 16,
        "target_age_max": 25,
        "target_locations": [],
        "interests": ["Education"],
        "status": "active",
        "featured": False,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    },
    {
        "title": "Passport Application Assistance Service",
        "description": "Expert help with passport applications. Fast processing, no hassle.",
        "category": "services",
        "price": 5000.00,
        "image_url": None,
        "link": "https://example.com/passport-service",
        "target_categories": ["travel_seeker", "passport_applicant"],
        "target_age_min": 18,
        "target_age_max": 65,
        "target_locations": ["Colombo"],
        "interests": ["Immigration"],
        "status": "active",
        "featured": True,
        "views": 0,
        "clicks": 0,
        "created_at": datetime.utcnow()
    }
]

def add_sample_products():
    """Add sample products to database"""
    try:
        # Clear existing products (optional - comment out if you want to keep existing products)
        # products_col.delete_many({})
        # print("🗑️ Cleared existing products")
        
        # Insert sample products
        result = products_col.insert_many(sample_products)
        
        print(f"✅ Added {len(result.inserted_ids)} sample products!")
        print("\nSample Products:")
        print("=" * 60)
        
        for i, product in enumerate(sample_products, 1):
            print(f"{i}. {product['title']}")
            print(f"   Category: {product['category']}")
            print(f"   Price: Rs. {product['price']:,.2f}")
            print(f"   Target: {', '.join(product['target_categories'][:3])}")
            print()
        
        print("=" * 60)
        print("\n🎉 You can now test the personalized ad system!")
        print("📊 Login and visit your dashboard to see personalized ads")
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")

if __name__ == "__main__":
    print("🚀 Adding sample products to database...")
    print()
    add_sample_products()