"""
Tag Products for Government Service Search Matching

This script tags existing products with:
1. `related_government_services` - for search-intent matching
2. `target_jobs` - for profession-based default ads

Run after seeding products to enable context-aware advertisements.
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

# ============================================
# CATEGORY TO GOVERNMENT SERVICE MAPPINGS
# ============================================

CATEGORY_TO_GOV_SERVICES = {
    # Travel & Immigration related
    'Air Tickets': ['passport', 'immigration', 'travel'],
    'Travel': ['passport', 'immigration', 'travel', 'visa'],
    'Travel Insurance': ['passport', 'immigration', 'travel'],
    'Visa Services': ['passport', 'immigration', 'visa'],
    'Travel Accessories': ['passport', 'travel'],
    'International': ['passport', 'immigration'],
    'Flight': ['passport', 'travel'],
    'Flights': ['passport', 'travel'],
    
    # Education & Examination related
    'Education': ['o/l results', 'a/l results', 'education', 'examination'],
    'Past Papers': ['o/l results', 'a/l results', 'examination'],
    'Tuition': ['o/l results', 'a/l results', 'education'],
    'Tuition Classes': ['o/l results', 'a/l results', 'education'],
    'Study Materials': ['o/l results', 'a/l results', 'education'],
    'Books': ['o/l results', 'a/l results', 'education'],
    'Educational': ['o/l results', 'a/l results', 'education'],
    'Courses': ['education', 'career', 'professional'],
    'Online Courses': ['education', 'career'],
    'Degree': ['a/l results', 'education', 'career'],
    'Professional Development': ['education', 'career'],
    
    # Vehicle & Driving related
    'Cars': ['driving license', 'driving', 'vehicle'],
    'Car': ['driving license', 'driving', 'vehicle'],
    'Vehicles': ['driving license', 'driving', 'vehicle'],
    'Vehicle': ['driving license', 'driving', 'vehicle'],
    'Automobiles': ['driving license', 'vehicle'],
    'Driving School': ['driving license', 'driving'],
    'Driving Schools': ['driving license', 'driving'],
    'Car Insurance': ['driving license', 'vehicle', 'insurance'],
    'Vehicle Loans': ['driving license', 'vehicle'],
    'Motorbike': ['driving license', 'vehicle'],
    'Motorcycle': ['driving license', 'vehicle'],
    
    # Baby & Family related
    'Baby Products': ['birth certificate', 'baby', 'family'],
    'Baby': ['birth certificate', 'baby'],
    'Parenting': ['birth certificate', 'family'],
    'Child': ['birth certificate', 'family', 'education'],
    'Children': ['birth certificate', 'family', 'education'],
    
    # Wedding & Marriage related
    'Wedding': ['marriage certificate', 'wedding'],
    'Wedding Services': ['marriage certificate', 'wedding'],
    'Wedding Photography': ['marriage certificate', 'wedding'],
    'Marriage': ['marriage certificate'],
    
    # Property & Land related
    'Property': ['land registration', 'property'],
    'Land': ['land registration', 'property'],
    'Real Estate': ['land registration', 'property'],
    'Home': ['land registration', 'property'],
    'Construction': ['land registration', 'property'],
    'Legal Services': ['land registration', 'property', 'legal'],
    
    # Technology
    'Electronics': ['technology'],
    'Computers': ['technology'],
    'Laptops': ['technology', 'education'],
    'Software': ['technology', 'education'],
    'Tech': ['technology'],
    
    # Health related
    'Health': ['health certificate', 'medical', 'health'],
    'Medical': ['health certificate', 'medical'],
    'Insurance': ['insurance', 'health'],
    'Health Insurance': ['health certificate', 'insurance'],
    
    # Employment related
    'Career': ['employment', 'job', 'career'],
    'Jobs': ['employment', 'job'],
    'Employment': ['employment', 'job'],
    'Resume': ['employment', 'job', 'career'],
}

# ============================================
# CATEGORY TO TARGET JOBS MAPPINGS
# ============================================

CATEGORY_TO_TARGET_JOBS = {
    # Education products for teachers
    'Education': ['teacher', 'lecturer', 'professor', 'educator'],
    'Past Papers': ['teacher', 'parent', 'student'],
    'Tuition': ['teacher', 'parent', 'student'],
    'Study Materials': ['teacher', 'student', 'parent'],
    'Books': ['teacher', 'student', 'all'],
    'Degree': ['all'],
    'Courses': ['all'],
    'Professional Development': ['teacher', 'all'],
    
    # Tech products for engineers
    'Electronics': ['software engineer', 'developer', 'it professional', 'tech'],
    'Computers': ['software engineer', 'developer', 'it professional'],
    'Laptops': ['software engineer', 'developer', 'student', 'teacher'],
    'Software': ['software engineer', 'developer'],
    'Tech': ['software engineer', 'developer', 'it professional'],
    
    # Vehicle products - general
    'Cars': ['all'],
    'Vehicles': ['all'],
    'Driving School': ['student', 'young adult', 'all'],
    
    # Travel - all professions
    'Air Tickets': ['all'],
    'Travel': ['all'],
    'Travel Insurance': ['all'],
    
    # Property - professionals
    'Property': ['business owner', 'professional', 'all'],
    'Real Estate': ['business owner', 'professional', 'all'],
    
    # Baby - parents
    'Baby Products': ['parent', 'all'],
    'Parenting': ['parent', 'all'],
}

def tag_products():
    """Tag all products with government services and target jobs"""
    
    # Tag both collections
    for collection_name in ['products', 'advertisements']:
        collection = db[collection_name]
        items = list(collection.find({}))
        print(f"\n📦 Found {len(items)} items in {collection_name} to tag")
        
        updated_count = 0
        category_stats = {}
        
        for item in items:
            item_id = item['_id']
            title = item.get('title', '').lower()
            category = item.get('category', '')
            description = item.get('description', '').lower()
            
            # Collect all matching government services
            gov_services = set()
            target_jobs = set()
            
            # Match by category
            for cat_key, services in CATEGORY_TO_GOV_SERVICES.items():
                if cat_key.lower() in category.lower() or cat_key.lower() in title:
                    gov_services.update(services)
            
            for cat_key, jobs in CATEGORY_TO_TARGET_JOBS.items():
                if cat_key.lower() in category.lower() or cat_key.lower() in title:
                    target_jobs.update(jobs)
            
            # Match by keywords in title/description
            keyword_matches = {
                'passport': ['passport', 'visa', 'travel abroad', 'flight', 'international', 'air ticket', 'airline'],
                'driving license': ['driving', 'car ', 'vehicle', 'automobile', 'motor', 'license'],
                'o/l results': ['o/l', 'ordinary level', 'grade 11', 'past paper', 'tuition', 'exam prep'],
                'a/l results': ['a/l', 'advanced level', 'grade 13', 'university'],
                'education': ['course', 'training', 'program', 'learn', 'study', 'class', 'education', 'degree', 'mba'],
                'birth certificate': ['baby', 'infant', 'newborn', 'parenting'],
                'marriage certificate': ['wedding', 'marriage', 'bridal'],
                'land registration': ['property', 'land', 'real estate', 'deed', 'apartment', 'house'],
                'health certificate': ['health', 'medical', 'vaccination', 'checkup', 'gym', 'fitness'],
                'employment': ['job', 'career', 'resume', 'interview'],
            }
            
            for service, keywords in keyword_matches.items():
                for keyword in keywords:
                    if keyword in title or keyword in description:
                        gov_services.add(service)
                        break
            
            # If no services found, try to infer from category
            if not gov_services:
                category_lower = category.lower()
                if 'education' in category_lower:
                    gov_services.add('education')
                    gov_services.add('o/l results')
                elif 'transport' in category_lower:
                    gov_services.add('driving license')
                    gov_services.add('vehicle')
                elif 'health' in category_lower:
                    gov_services.add('health certificate')
                elif 'housing' in category_lower:
                    gov_services.add('land registration')
                    gov_services.add('property')
                elif 'technology' in category_lower or 'tech' in category_lower:
                    gov_services.add('technology')
            
            # Update item if we found matches
            if gov_services or target_jobs:
                update_data = {
                    'related_government_services': list(gov_services) if gov_services else [],
                    'target_jobs': list(target_jobs) if target_jobs else ['all'],
                    'updated_at': datetime.utcnow()
                }
                
                collection.update_one(
                    {'_id': item_id},
                    {'$set': update_data}
                )
                updated_count += 1
                
                # Track stats by category
                if category not in category_stats:
                    category_stats[category] = {'count': 0, 'services': set()}
                category_stats[category]['count'] += 1
                category_stats[category]['services'].update(gov_services)
                
                print(f"  ✓ {item.get('title', 'N/A')[:40]}: {list(gov_services)[:3]}")
        
        print(f"\n✅ Updated {updated_count} items in {collection_name} with government service tags")
        
        # Print summary by category
        print(f"\n📊 Tags by Category in {collection_name}:")
        for cat, stats in sorted(category_stats.items()):
            print(f"   {cat}: {stats['count']} items → {list(stats['services'])[:3]}")
    
    return updated_count

def verify_tagging():
    """Verify products are tagged correctly"""
    
    print("\n🔍 Verification:")
    
    # Check passport-related products
    passport_products = list(db.products.find({
        'related_government_services': {'$in': ['passport', 'immigration', 'travel']}
    }))
    print(f"   • Passport/Travel products: {len(passport_products)}")
    
    # Check driving-related products
    driving_products = list(db.products.find({
        'related_government_services': {'$in': ['driving license', 'driving', 'vehicle']}
    }))
    print(f"   • Driving/Vehicle products: {len(driving_products)}")
    
    # Check education-related products
    education_products = list(db.products.find({
        'related_government_services': {'$in': ['o/l results', 'a/l results', 'education']}
    }))
    print(f"   • Education products: {len(education_products)}")
    
    # Check teacher-targeted products
    teacher_products = list(db.products.find({
        'target_jobs': {'$in': ['teacher', 'lecturer', 'educator']}
    }))
    print(f"   • Teacher-targeted products: {len(teacher_products)}")
    
    # Total tagged
    tagged_products = db.products.count_documents({
        'related_government_services': {'$exists': True, '$ne': []}
    })
    total_products = db.products.count_documents({})
    print(f"\n   📈 Total tagged: {tagged_products}/{total_products} products")

if __name__ == "__main__":
    print("=" * 60)
    print("🏷️  TAGGING PRODUCTS FOR GOVERNMENT SERVICE MATCHING")
    print("=" * 60)
    
    tag_products()
    verify_tagging()
    
    print("\n" + "=" * 60)
    print("✅ Product tagging completed!")
    print("=" * 60)
