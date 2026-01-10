"""
Update existing products with government service relation tags
This allows products to be matched with government searches
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

def update_products_with_tags():
    """Add government service relation tags to products"""
    
    print("🔄 Updating products with government service tags...")
    
    # ==========================================
    # TRAVEL & IMMIGRATION RELATED PRODUCTS
    # ==========================================
    
    # Air Tickets
    db.products.update_many(
        {"category": {"$regex": "travel|ticket|flight", "$options": "i"}},
        {"$set": {
            "related_government_services": ["passport", "immigration", "visa", "emigration"],
            "solves_user_needs": ["international_travel", "going_abroad", "foreign_employment"],
            "best_for_user_types": ["tech_professional", "business_owner", "student", "teacher"],
            "trigger_scenarios": ["passport_search", "visa_search", "immigration_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated travel/flight products")
    
    # Travel Insurance
    db.products.update_many(
        {"name": {"$regex": "insurance.*travel|travel.*insurance", "$options": "i"}},
        {"$set": {
            "related_government_services": ["passport", "immigration", "visa"],
            "solves_user_needs": ["international_travel", "safety_abroad"],
            "best_for_user_types": ["all"],
            "trigger_scenarios": ["passport_search", "visa_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated travel insurance products")
    
    # ==========================================
    # EDUCATION RELATED PRODUCTS
    # ==========================================
    
    # Courses/Degrees
    db.products.update_many(
        {"category": {"$regex": "course|education|degree|learning", "$options": "i"}},
        {"$set": {
            "related_government_services": ["o/l_results", "a/l_results", "examination", "university"],
            "solves_user_needs": ["skill_development", "career_advancement", "professional_growth"],
            "best_for_user_types": ["teacher", "tech_professional", "student", "young_adult"],
            "trigger_scenarios": ["ol_search", "al_search", "exam_search", "education_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated course/degree products")
    
    # Past Papers & Study Materials
    db.products.update_many(
        {"$or": [
            {"name": {"$regex": "past paper|study|revision|guide", "$options": "i"}},
            {"description": {"$regex": "o/l|a/l|exam|study", "$options": "i"}}
        ]},
        {"$set": {
            "related_government_services": ["o/l_results", "a/l_results", "examination"],
            "solves_user_needs": ["exam_preparation", "child_education", "academic_improvement"],
            "best_for_user_types": ["parent", "student", "teacher"],
            "trigger_scenarios": ["ol_search", "al_search", "exam_results_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated past papers/study materials")
    
    # Books
    db.products.update_many(
        {"category": {"$regex": "book|stationery", "$options": "i"}},
        {"$set": {
            "related_government_services": ["o/l_results", "a/l_results", "education"],
            "solves_user_needs": ["learning", "knowledge", "exam_preparation"],
            "best_for_user_types": ["student", "teacher", "parent"],
            "trigger_scenarios": ["ol_search", "al_search", "education_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated book products")
    
    # ==========================================
    # VEHICLE & DRIVING RELATED PRODUCTS
    # ==========================================
    
    # Cars/Vehicles
    db.products.update_many(
        {"$or": [
            {"category": {"$regex": "vehicle|car|automobile", "$options": "i"}},
            {"name": {"$regex": "car|vehicle|bike|motorcycle", "$options": "i"}}
        ]},
        {"$set": {
            "related_government_services": ["driving_license", "vehicle_registration", "motor_traffic"],
            "solves_user_needs": ["transportation", "mobility", "vehicle_ownership"],
            "best_for_user_types": ["tech_professional", "business_owner", "teacher"],
            "trigger_scenarios": ["driving_license_search", "vehicle_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated vehicle products")
    
    # Driving Schools/Theory Books
    db.products.update_many(
        {"name": {"$regex": "driving|driver|highway code", "$options": "i"}},
        {"$set": {
            "related_government_services": ["driving_license", "learner_permit"],
            "solves_user_needs": ["driving_education", "license_preparation"],
            "best_for_user_types": ["student", "young_adult", "all"],
            "trigger_scenarios": ["driving_license_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated driving education products")
    
    # ==========================================
    # TECHNOLOGY & ELECTRONICS
    # ==========================================
    
    # Laptops
    db.products.update_many(
        {"name": {"$regex": "laptop|computer|notebook", "$options": "i"}},
        {"$set": {
            "related_government_services": ["passport", "immigration", "o/l_results", "a/l_results"],
            "solves_user_needs": ["work_abroad", "education", "professional_work", "learning"],
            "best_for_user_types": ["tech_professional", "student", "teacher", "business_owner"],
            "trigger_scenarios": ["passport_search", "education_search", "job_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated laptop products")
    
    # Electronics General
    db.products.update_many(
        {"category": {"$regex": "electronic|gadget|device", "$options": "i"}},
        {"$set": {
            "related_government_services": ["o/l_results", "a/l_results", "passport"],
            "solves_user_needs": ["education", "travel", "work"],
            "best_for_user_types": ["tech_professional", "student", "young_adult"],
            "trigger_scenarios": ["education_search", "passport_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated electronics products")
    
    # ==========================================
    # INSURANCE & FINANCIAL PRODUCTS
    # ==========================================
    
    # Insurance Products
    db.products.update_many(
        {"name": {"$regex": "insurance", "$options": "i"}},
        {"$set": {
            "related_government_services": ["birth_certificate", "marriage_certificate", "driving_license", "property_registration"],
            "solves_user_needs": ["financial_security", "family_protection", "asset_protection"],
            "best_for_user_types": ["all"],
            "trigger_scenarios": ["birth_certificate_search", "marriage_search", "property_search", "vehicle_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated insurance products")
    
    # ==========================================
    # PROPERTY & LEGAL SERVICES
    # ==========================================
    
    # Legal Services
    db.products.update_many(
        {"name": {"$regex": "legal|lawyer|attorney", "$options": "i"}},
        {"$set": {
            "related_government_services": ["property_registration", "land_registration", "marriage_certificate"],
            "solves_user_needs": ["legal_documentation", "property_purchase", "legal_protection"],
            "best_for_user_types": ["business_owner", "property_buyer", "all"],
            "trigger_scenarios": ["property_search", "land_search", "marriage_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated legal service products")
    
    # ==========================================
    # BABY & FAMILY PRODUCTS
    # ==========================================
    
    # Baby Products
    db.products.update_many(
        {"name": {"$regex": "baby|infant|child|parenting", "$options": "i"}},
        {"$set": {
            "related_government_services": ["birth_certificate", "baby_registration"],
            "solves_user_needs": ["new_parent", "baby_care", "family_planning"],
            "best_for_user_types": ["parent", "new_parent"],
            "trigger_scenarios": ["birth_certificate_search"],
            "updated_at": datetime.utcnow()
        }}
    )
    print("✅ Updated baby products")
    
    print("\n" + "="*60)
    
    # Show statistics
    total_products = db.products.count_documents({})
    tagged_products = db.products.count_documents({"related_government_services": {"$exists": True}})
    
    print(f"📊 Total products in database: {total_products}")
    print(f"✅ Products with government tags: {tagged_products}")
    print(f"📈 Tag coverage: {(tagged_products/total_products*100):.1f}%")

def show_sample_tagged_products():
    """Show some examples of tagged products"""
    print("\n" + "="*60)
    print("📋 Sample Tagged Products:")
    print("="*60)
    
    samples = db.products.find(
        {"related_government_services": {"$exists": True}},
        {"name": 1, "category": 1, "related_government_services": 1, "trigger_scenarios": 1}
    ).limit(5)
    
    for i, product in enumerate(samples, 1):
        print(f"\n{i}. {product.get('name', 'N/A')}")
        print(f"   Category: {product.get('category', 'N/A')}")
        print(f"   Related Services: {', '.join(product.get('related_government_services', []))}")
        print(f"   Triggers: {', '.join(product.get('trigger_scenarios', []))}")

if __name__ == "__main__":
    print("🏷️  Tagging Products with Government Service Relations")
    print("="*60)
    
    update_products_with_tags()
    show_sample_tagged_products()
    
    print("\n" + "="*60)
    print("✅ Product tagging completed successfully!")
    print("="*60)