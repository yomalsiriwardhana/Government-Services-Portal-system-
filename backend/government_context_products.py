"""
Government Context-Aware Products Seeding Script
Adds products specifically designed for government service searches combined with user roles
"""

from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'government_portal'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
products_collection = db.products

print("🔌 Connecting to MongoDB...")
print("✅ Connected to database")
print("=" * 60)

# ========================================
# GOVERNMENT CONTEXT-AWARE PRODUCTS
# ========================================

government_products = [
    # ==========================================
    # EDUCATION PRODUCTS - O/L & A/L Related
    # ==========================================
    {
        'title': 'O/L Past Paper Complete Set 2020-2024',
        'description': 'Complete 5-year collection of O/L past papers for all subjects with detailed answers. Perfect for exam preparation.',
        'price': 8500,
        'category': 'Education',
        'subcategory': 'Past Papers',
        'brand': 'Edu Publishers',
        'image_url': 'https://example.com/images/ol-papers.jpg',
        'link_url': 'https://example.com/products/ol-papers',
        'stock': 500,
        'featured': True,
        'target_age_min': 14,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo', 'Matara'],
        'target_jobs': ['parent', 'teacher', 'engineer', 'student'],
        'target_categories': ['parent', 'student', 'education'],
        'keywords': ['o/l', 'past papers', 'exam', 'study', 'education', 'results'],
        
        # Government context tags
        'related_government_services': ['o/l_results', 'o/l_exam', 'examination'],
        'solves_user_needs': ['exam_preparation', 'child_education', 'academic_improvement'],
        'best_for_user_types': ['parent', 'student', 'tech_professional'],
        'trigger_scenarios': ['ol_search', 'exam_results_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'A/L Past Paper Bundle - Physical Science',
        'description': 'A/L past papers for Physics, Chemistry, Combined Maths (2018-2024). Includes marking schemes.',
        'price': 6500,
        'category': 'Education',
        'subcategory': 'Past Papers',
        'brand': 'Edu Publishers',
        'image_url': 'https://example.com/images/al-papers.jpg',
        'link_url': 'https://example.com/products/al-papers',
        'stock': 350,
        'featured': True,
        'target_age_min': 16,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['parent', 'teacher', 'student'],
        'target_categories': ['parent', 'student', 'education'],
        'keywords': ['a/l', 'past papers', 'exam', 'advanced level', 'science'],
        
        'related_government_services': ['a/l_results', 'a/l_exam', 'examination'],
        'solves_user_needs': ['exam_preparation', 'university_preparation', 'higher_education'],
        'best_for_user_types': ['parent', 'student', 'tech_professional'],
        'trigger_scenarios': ['al_search', 'exam_results_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Private Tuition Classes - Grade 11 O/L',
        'description': 'Professional O/L tuition for all subjects. Small batches, experienced teachers. Weekend and weekday options.',
        'price': 15000,
        'category': 'Education',
        'subcategory': 'Tuition',
        'brand': 'Elite Tuition Center',
        'image_url': 'https://example.com/images/tuition.jpg',
        'link_url': 'https://example.com/services/tuition',
        'stock': 100,
        'featured': True,
        'target_age_min': 14,
        'target_age_max': 17,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['parent', 'student'],
        'target_categories': ['parent', 'student', 'education'],
        'keywords': ['tuition', 'classes', 'o/l', 'education', 'exam preparation'],
        
        'related_government_services': ['o/l_results', 'o/l_exam', 'examination'],
        'solves_user_needs': ['exam_preparation', 'child_education', 'academic_improvement'],
        'best_for_user_types': ['parent', 'tech_professional', 'student'],
        'trigger_scenarios': ['ol_search', 'exam_results_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Online Learning Platform Subscription - 1 Year',
        'description': 'Complete online education platform. Video lessons, practice tests, live classes for O/L and A/L students.',
        'price': 12000,
        'category': 'Education',
        'subcategory': 'Online Learning',
        'brand': 'EduOnline',
        'image_url': 'https://example.com/images/online-learning.jpg',
        'link_url': 'https://example.com/services/online-learning',
        'stock': 1000,
        'featured': True,
        'target_age_min': 13,
        'target_age_max': 19,
        'target_locations': ['All'],
        'target_jobs': ['parent', 'student'],
        'target_categories': ['parent', 'student', 'education'],
        'keywords': ['online', 'learning', 'education', 'video', 'classes', 'o/l', 'a/l'],
        
        'related_government_services': ['o/l_results', 'a/l_results', 'examination'],
        'solves_user_needs': ['exam_preparation', 'child_education', 'learning'],
        'best_for_user_types': ['parent', 'student', 'tech_professional'],
        'trigger_scenarios': ['ol_search', 'al_search', 'exam_results_search'],
        
        'created_at': datetime.utcnow()
    },
    
    # ==========================================
    # PROFESSIONAL DEVELOPMENT - For Teachers
    # ==========================================
    {
        'title': 'Bachelor of Education Degree Program',
        'description': 'Complete B.Ed degree program. Part-time, weekend classes. Accredited by UGC. Perfect for working teachers.',
        'price': 350000,
        'category': 'Education',
        'subcategory': 'Degree Programs',
        'brand': 'National Institute of Education',
        'image_url': 'https://example.com/images/bed-degree.jpg',
        'link_url': 'https://example.com/programs/bed',
        'stock': 50,
        'featured': True,
        'target_age_min': 25,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['teacher', 'lecturer'],
        'target_categories': ['teacher', 'education', 'professional_development'],
        'keywords': ['degree', 'education', 'teacher', 'bachelor', 'professional'],
        
        'related_government_services': ['o/l_results', 'a/l_results', 'examination', 'education'],
        'solves_user_needs': ['professional_development', 'career_advancement', 'skill_development'],
        'best_for_user_types': ['teacher'],
        'trigger_scenarios': ['ol_search', 'al_search', 'education_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Master of Education (M.Ed) Program',
        'description': 'Advanced M.Ed program. Research-based, part-time study. Career advancement for educators.',
        'price': 450000,
        'category': 'Education',
        'subcategory': 'Degree Programs',
        'brand': 'University of Colombo',
        'image_url': 'https://example.com/images/med-degree.jpg',
        'link_url': 'https://example.com/programs/med',
        'stock': 30,
        'featured': True,
        'target_age_min': 28,
        'target_age_max': 60,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['teacher', 'lecturer', 'principal'],
        'target_categories': ['teacher', 'education', 'professional_development'],
        'keywords': ['masters', 'education', 'teacher', 'degree', 'professional'],
        
        'related_government_services': ['o/l_results', 'a/l_results', 'examination'],
        'solves_user_needs': ['professional_development', 'career_advancement', 'academic_excellence'],
        'best_for_user_types': ['teacher'],
        'trigger_scenarios': ['ol_search', 'al_search', 'education_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Educational Technology Course for Teachers',
        'description': 'Learn modern teaching methods, digital tools, classroom management. 3-month certification program.',
        'price': 55000,
        'category': 'Education',
        'subcategory': 'Professional Courses',
        'brand': 'TeachTech Academy',
        'image_url': 'https://example.com/images/edtech.jpg',
        'link_url': 'https://example.com/courses/edtech',
        'stock': 80,
        'featured': False,
        'target_age_min': 25,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['teacher', 'lecturer'],
        'target_categories': ['teacher', 'education', 'course_buyer'],
        'keywords': ['teaching', 'technology', 'education', 'course', 'digital'],
        
        'related_government_services': ['o/l_results', 'a/l_results', 'examination'],
        'solves_user_needs': ['professional_development', 'skill_development', 'teaching_improvement'],
        'best_for_user_types': ['teacher'],
        'trigger_scenarios': ['ol_search', 'al_search', 'education_search'],
        
        'created_at': datetime.utcnow()
    },
    
    # ==========================================
    # TRAVEL & IMMIGRATION - Passport Related
    # ==========================================
    {
        'title': 'International Flight Tickets - Economy Class',
        'description': 'Affordable international air tickets. Multiple destinations. Easy booking, flexible dates.',
        'price': 125000,
        'category': 'Travel',
        'subcategory': 'Air Tickets',
        'brand': 'SkyTravel',
        'image_url': 'https://example.com/images/flight-tickets.jpg',
        'link_url': 'https://example.com/travel/tickets',
        'stock': 200,
        'featured': True,
        'target_age_min': 20,
        'target_age_max': 65,
        'target_locations': ['All'],
        'target_jobs': ['all'],
        'target_categories': ['travel', 'all'],
        'keywords': ['flight', 'tickets', 'travel', 'international', 'abroad'],
        
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['international_travel', 'going_abroad', 'foreign_employment'],
        'best_for_user_types': ['tech_professional', 'teacher', 'student', 'business_owner'],
        'trigger_scenarios': ['passport_search', 'visa_search', 'immigration_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Work Visa Assistance Service',
        'description': 'Complete work visa application support. Documentation, application submission, consultation.',
        'price': 75000,
        'category': 'Travel',
        'subcategory': 'Visa Services',
        'brand': 'GlobalVisa Consultants',
        'image_url': 'https://example.com/images/visa-service.jpg',
        'link_url': 'https://example.com/services/visa',
        'stock': 100,
        'featured': True,
        'target_age_min': 22,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['software engineer', 'engineer', 'doctor', 'nurse'],
        'target_categories': ['tech_professional', 'professional'],
        'keywords': ['visa', 'work permit', 'immigration', 'abroad', 'foreign'],
        
        'related_government_services': ['passport', 'immigration', 'emigration'],
        'solves_user_needs': ['foreign_employment', 'going_abroad', 'work_abroad'],
        'best_for_user_types': ['tech_professional', 'business_owner'],
        'trigger_scenarios': ['passport_search', 'immigration_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Student Visa Processing Service',
        'description': 'Student visa application help for UK, USA, Australia, Canada. Complete guidance and documentation.',
        'price': 65000,
        'category': 'Travel',
        'subcategory': 'Visa Services',
        'brand': 'EduVisa Services',
        'image_url': 'https://example.com/images/student-visa.jpg',
        'link_url': 'https://example.com/services/student-visa',
        'stock': 150,
        'featured': True,
        'target_age_min': 18,
        'target_age_max': 30,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['student'],
        'target_categories': ['student', 'young_adult'],
        'keywords': ['student visa', 'study abroad', 'university', 'foreign education'],
        
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['foreign_education', 'going_abroad', 'university_abroad'],
        'best_for_user_types': ['student', 'parent'],
        'trigger_scenarios': ['passport_search', 'visa_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'International Travel Insurance - 1 Year',
        'description': 'Comprehensive travel insurance. Medical coverage, trip cancellation, lost baggage protection.',
        'price': 35000,
        'category': 'Travel',
        'subcategory': 'Insurance',
        'brand': 'SafeTravel Insurance',
        'image_url': 'https://example.com/images/travel-insurance.jpg',
        'link_url': 'https://example.com/products/travel-insurance',
        'stock': 500,
        'featured': False,
        'target_age_min': 18,
        'target_age_max': 70,
        'target_locations': ['All'],
        'target_jobs': ['all'],
        'target_categories': ['travel', 'all'],
        'keywords': ['insurance', 'travel', 'international', 'medical', 'coverage'],
        
        'related_government_services': ['passport', 'immigration', 'visa'],
        'solves_user_needs': ['international_travel', 'safety_abroad', 'protection'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['passport_search', 'visa_search'],
        
        'created_at': datetime.utcnow()
    },
    
    # ==========================================
    # VEHICLE & DRIVING - License Related
    # ==========================================
    {
        'title': 'Toyota Aqua 2019 - Hybrid Car',
        'description': 'Well-maintained Toyota Aqua 2019. Low mileage, excellent fuel economy. Perfect for city driving.',
        'price': 4800000,
        'category': 'Vehicles',
        'subcategory': 'Cars',
        'brand': 'Toyota',
        'image_url': 'https://example.com/images/aqua-2019.jpg',
        'link_url': 'https://example.com/vehicles/aqua-2019',
        'stock': 3,
        'featured': True,
        'target_age_min': 25,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['teacher', 'engineer', 'doctor', 'business owner'],
        'target_categories': ['vehicle_buyer', 'mid_career_family'],
        'keywords': ['car', 'toyota', 'aqua', 'hybrid', 'vehicle', 'auto'],
        
        'related_government_services': ['driving_license', 'vehicle_registration'],
        'solves_user_needs': ['transportation', 'mobility', 'vehicle_ownership'],
        'best_for_user_types': ['teacher', 'tech_professional', 'business_owner'],
        'trigger_scenarios': ['driving_license_search', 'vehicle_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Suzuki Alto 2020 - Budget Car',
        'description': 'Affordable Suzuki Alto 2020. Perfect first car, low maintenance, excellent condition.',
        'price': 2950000,
        'category': 'Vehicles',
        'subcategory': 'Cars',
        'brand': 'Suzuki',
        'image_url': 'https://example.com/images/alto-2020.jpg',
        'link_url': 'https://example.com/vehicles/alto-2020',
        'stock': 5,
        'featured': True,
        'target_age_min': 22,
        'target_age_max': 45,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['teacher', 'engineer', 'student'],
        'target_categories': ['vehicle_buyer', 'young_adult', 'early_career'],
        'keywords': ['car', 'suzuki', 'alto', 'budget', 'affordable', 'vehicle'],
        
        'related_government_services': ['driving_license', 'vehicle_registration'],
        'solves_user_needs': ['transportation', 'mobility', 'first_car'],
        'best_for_user_types': ['teacher', 'student', 'tech_professional'],
        'trigger_scenarios': ['driving_license_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Honda Fit 2017 - Family Car',
        'description': 'Spacious Honda Fit 2017. Great family car, well maintained, low mileage.',
        'price': 4200000,
        'category': 'Vehicles',
        'subcategory': 'Cars',
        'brand': 'Honda',
        'image_url': 'https://example.com/images/fit-2017.jpg',
        'link_url': 'https://example.com/vehicles/fit-2017',
        'stock': 2,
        'featured': False,
        'target_age_min': 28,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['teacher', 'engineer', 'manager'],
        'target_categories': ['vehicle_buyer', 'mid_career_family'],
        'keywords': ['car', 'honda', 'fit', 'family', 'vehicle'],
        
        'related_government_services': ['driving_license', 'vehicle_registration'],
        'solves_user_needs': ['transportation', 'family_mobility', 'vehicle_ownership'],
        'best_for_user_types': ['teacher', 'tech_professional', 'parent'],
        'trigger_scenarios': ['driving_license_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Professional Driving School - Full Course',
        'description': 'Complete driving course. Theory and practical lessons. Experienced instructors. Pass guarantee.',
        'price': 45000,
        'category': 'Education',
        'subcategory': 'Driving',
        'brand': 'Safe Drive Academy',
        'image_url': 'https://example.com/images/driving-school.jpg',
        'link_url': 'https://example.com/services/driving-school',
        'stock': 200,
        'featured': True,
        'target_age_min': 18,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['student', 'teacher', 'engineer'],
        'target_categories': ['all'],
        'keywords': ['driving', 'school', 'license', 'lessons', 'course'],
        
        'related_government_services': ['driving_license', 'learner_permit'],
        'solves_user_needs': ['driving_education', 'license_preparation', 'mobility'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['driving_license_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Car Insurance - Comprehensive Coverage',
        'description': 'Full car insurance with accident coverage, third-party liability, theft protection.',
        'price': 75000,
        'category': 'Insurance',
        'subcategory': 'Vehicle Insurance',
        'brand': 'AutoCover Insurance',
        'image_url': 'https://example.com/images/car-insurance.jpg',
        'link_url': 'https://example.com/products/car-insurance',
        'stock': 1000,
        'featured': False,
        'target_age_min': 22,
        'target_age_max': 65,
        'target_locations': ['All'],
        'target_jobs': ['all'],
        'target_categories': ['vehicle_buyer', 'all'],
        'keywords': ['insurance', 'car', 'vehicle', 'coverage', 'protection'],
        
        'related_government_services': ['driving_license', 'vehicle_registration'],
        'solves_user_needs': ['vehicle_protection', 'financial_security', 'legal_compliance'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['driving_license_search', 'vehicle_search'],
        
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Highway Code & Theory Test Book',
        'description': 'Complete driving theory guide. Highway code, road signs, practice tests. Updated 2024 edition.',
        'price': 1500,
        'category': 'Education',
        'subcategory': 'Books',
        'brand': 'MotorTraffic Publications',
        'image_url': 'https://example.com/images/highway-code.jpg',
        'link_url': 'https://example.com/products/highway-code',
        'stock': 800,
        'featured': False,
        'target_age_min': 18,
        'target_age_max': 50,
        'target_locations': ['All'],
        'target_jobs': ['student', 'all'],
        'target_categories': ['student', 'young_adult', 'all'],
        'keywords': ['driving', 'theory', 'book', 'highway code', 'test', 'license'],
        
        'related_government_services': ['driving_license', 'learner_permit'],
        'solves_user_needs': ['driving_education', 'license_preparation', 'theory_test'],
        'best_for_user_types': ['all'],
        'trigger_scenarios': ['driving_license_search'],
        
        'created_at': datetime.utcnow()
    },
]

def seed_government_products():
    """Seed government context-aware products"""
    print(f"\n📦 Adding {len(government_products)} government context-aware products...")
    
    # Insert products
    result = products_collection.insert_many(government_products)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} products")
    
    return result.inserted_ids

def show_summary():
    """Show summary of seeded products"""
    print("\n" + "=" * 60)
    print("📊 SUMMARY OF GOVERNMENT CONTEXT PRODUCTS")
    print("=" * 60)
    
    # Count by category
    categories = {}
    for product in government_products:
        category = product.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
    
    print("\n📁 Products by Category:")
    for category, count in categories.items():
        print(f"   • {category}: {count} products")
    
    # Count by user type targeting
    user_types = {}
    for product in government_products:
        for user_type in product.get('best_for_user_types', []):
            user_types[user_type] = user_types.get(user_type, 0) + 1
    
    print("\n👤 Products by User Type:")
    for user_type, count in sorted(user_types.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {user_type}: {count} products")
    
    # Count by government service
    services = {}
    for product in government_products:
        for service in product.get('related_government_services', []):
            services[service] = services.get(service, 0) + 1
    
    print("\n🏛️ Products by Government Service:")
    for service, count in sorted(services.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {service}: {count} products")
    
    # Total products in database
    total_in_db = products_collection.count_documents({})
    gov_products_in_db = products_collection.count_documents({
        'related_government_services': {'$exists': True}
    })
    
    print("\n" + "=" * 60)
    print(f"📊 Total products in database: {total_in_db}")
    print(f"🏛️ Government-tagged products: {gov_products_in_db}")
    print("=" * 60)

def show_sample_products():
    """Show sample products by scenario"""
    print("\n" + "=" * 60)
    print("📋 SAMPLE PRODUCTS BY SCENARIO")
    print("=" * 60)
    
    scenarios = [
        ("O/L Search (Teacher)", {"trigger_scenarios": "ol_search", "best_for_user_types": "teacher"}),
        ("O/L Search (Parent/Engineer)", {"trigger_scenarios": "ol_search", "best_for_user_types": {"$in": ["parent", "tech_professional"]}}),
        ("Passport Search (Tech Professional)", {"trigger_scenarios": "passport_search", "best_for_user_types": "tech_professional"}),
        ("Driving License (Teacher)", {"trigger_scenarios": "driving_license_search", "best_for_user_types": {"$in": ["teacher", "all"]}}),
    ]
    
    for scenario_name, query in scenarios:
        print(f"\n🎯 {scenario_name}:")
        samples = products_collection.find(query, {"title": 1, "price": 1}).limit(3)
        for i, product in enumerate(samples, 1):
            price_formatted = f"Rs. {product['price']:,}"
            print(f"   {i}. {product['title']} - {price_formatted}")

if __name__ == "__main__":
    print("🌱 Seeding Government Context-Aware Products")
    print("=" * 60)
    
    # Check if products already exist
    existing_count = products_collection.count_documents({
        'title': {'$in': [p['title'] for p in government_products]}
    })
    
    if existing_count > 0:
        print(f"\n⚠️  Warning: {existing_count} products with similar titles already exist")
        print("Proceeding with insertion anyway...")
    
    # Seed products
    inserted_ids = seed_government_products()
    
    # Show summary
    show_summary()
    show_sample_products()
    
    print("\n✅ Government context products seeded successfully!")
    print("=" * 60)
