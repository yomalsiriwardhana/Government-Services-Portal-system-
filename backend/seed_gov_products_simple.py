"""
Insert government-context products (no emojis for Windows compatibility)
"""
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal
products = db.products

# Travel products for passport searches
travel_products = [
    {
        'title': 'International Flight Tickets - Economy Class',
        'description': 'Affordable international air tickets. Multiple destinations.',
        'price': 125000,
        'category': 'Travel',
        'stock': 200,
        'featured': True,
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['international_travel', 'going_abroad'],
        'best_for_user_types': ['tech_professional', 'teacher', 'student'],
        'trigger_scenarios': ['passport_search', 'visa_search'],
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Work Visa Assistance Service',
        'description': 'Complete work visa application support.',
        'price': 75000,
        'category': 'Travel',
        'stock': 100,
        'featured': True,
        'related_government_services': ['passport', 'immigration', 'emigration'],
        'solves_user_needs': ['foreign_employment', 'work_abroad'],
        'best_for_user_types': ['tech_professional'],
        'trigger_scenarios': ['passport_search', 'immigration_search'],
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Student Visa Processing Service',
        'description': 'Student visa help for UK, USA, Australia, Canada.',
        'price': 65000,
        'category': 'Travel',
        'stock': 150,
        'featured': True,
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['foreign_education', 'university_abroad'],
        'best_for_user_types': ['student', 'parent'],
        'trigger_scenarios': ['passport_search', 'visa_search'],
        'created_at': datetime.utcnow()
    },
    {
        'title': 'International Travel Insurance - 1 Year',
        'description': 'Comprehensive travel insurance. Medical coverage included.',
        'price': 35000,
        'category': 'Travel',
        'stock': 500,
        'featured': True,
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['international_travel', 'safety_abroad'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['passport_search', 'visa_search'],
        'created_at': datetime.utcnow()
    }
]

# Vehicle products for driving license searches
vehicle_products = [
    {
        'title': 'Toyota Aqua 2019 - Hybrid Car',
        'description': 'Well-maintained Toyota Aqua. Excellent fuel economy.',
        'price': 4800000,
        'category': 'Vehicles',
        'stock': 3,
        'featured': True,
        'related_government_services': ['driving_license', 'vehicle_registration'],
        'solves_user_needs': ['transportation', 'vehicle_ownership'],
        'best_for_user_types': ['teacher', 'tech_professional'],
        'trigger_scenarios': ['driving_license_search'],
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Professional Driving School - Full Course',
        'description': 'Complete driving course. Pass guarantee.',
        'price': 45000,
        'category': 'Education',
        'stock': 200,
        'featured': True,
        'related_government_services': ['driving_license', 'learner_permit'],
        'solves_user_needs': ['driving_education', 'license_preparation'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['driving_license_search'],
        'created_at': datetime.utcnow()
    }
]

# Education products for O/L searches
education_products = [
    {
        'title': 'O/L Past Paper Complete Set 2020-2024',
        'description': 'Complete 5-year O/L past papers with answers.',
        'price': 8500,
        'category': 'Education',
        'stock': 500,
        'featured': True,
        'related_government_services': ['o/l_results', 'o/l_exam', 'examination'],
        'solves_user_needs': ['exam_preparation', 'child_education'],
        'best_for_user_types': ['parent', 'student', 'teacher'],
        'trigger_scenarios': ['ol_search', 'exam_results_search'],
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Private Tuition Classes - Grade 11 O/L',
        'description': 'Professional O/L tuition. Small batches.',
        'price': 15000,
        'category': 'Education',
        'stock': 100,
        'featured': True,
        'related_government_services': ['o/l_results', 'o/l_exam'],
        'solves_user_needs': ['exam_preparation', 'academic_improvement'],
        'best_for_user_types': ['parent', 'student'],
        'trigger_scenarios': ['ol_search'],
        'created_at': datetime.utcnow()
    }
]

all_products = travel_products + vehicle_products + education_products

print("Inserting government-context products...")
print(f"Total: {len(all_products)} products")

# Check if already exist
existing = products.count_documents({
    'title': {'$in': [p['title'] for p in all_products]}
})

if existing > 0:
    print(f"WARNING: {existing} products already exist. Deleting them first...")
    products.delete_many({
        'title': {'$in': [p['title'] for p in all_products]}
    })

# Insert
result = products.insert_many(all_products)
print(f"SUCCESS: Inserted {len(result.inserted_ids)} products")

# Verify
travel_count = products.count_documents({'related_government_services': {'$in': ['passport']}})
vehicle_count = products.count_documents({'related_government_services': {'$in': ['driving_license']}})
education_count = products.count_documents({'related_government_services': {'$in': ['o/l_results']}})

print(f"\nVerification:")
print(f"  Travel (passport): {travel_count}")
print(f"  Vehicle (driving_license): {vehicle_count}")
print(f"  Education (o/l_results): {education_count}")
print(f"\nDONE!")
