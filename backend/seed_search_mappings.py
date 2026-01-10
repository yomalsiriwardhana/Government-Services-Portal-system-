"""
Seed script for government search to product mappings
This connects government service searches to commercial products
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

def clear_existing_mappings():
    """Clear existing mappings"""
    result = db.search_to_product_mappings.delete_many({})
    print(f"✅ Cleared {result.deleted_count} existing mappings")

def seed_mappings():
    """Seed government search to product mappings"""
    
    mappings = [
        # ==========================================
        # PASSPORT & IMMIGRATION SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["passport", "immigration", "emigration", "travel document"],
            "search_category": "passport_immigration",
            "inferred_needs": ["international_travel", "going_abroad", "foreign_employment"],
            "product_categories": ["Air Tickets", "Travel Insurance", "Visa Services", "Travel Accessories", "Currency Exchange", "International SIM"],
            "target_user_profiles": {
                "tech_professional": {
                    "priority": 1,
                    "suggested_products": ["Laptop for Travel", "International Travel Insurance", "Work Visa Services"]
                },
                "teacher": {
                    "priority": 2,
                    "suggested_products": ["Educational Travel Programs", "Travel Insurance", "Air Tickets"]
                },
                "student": {
                    "priority": 1,
                    "suggested_products": ["Student Visa Services", "Budget Air Tickets", "Student Travel Insurance"]
                },
                "business_owner": {
                    "priority": 1,
                    "suggested_products": ["Business Class Tickets", "Corporate Travel Insurance", "Business Visa Services"]
                }
            },
            "life_event_indicators": ["planning_travel", "going_abroad", "job_change_abroad"],
            "confidence_weight": 0.95,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # O/L EXAMINATION SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["o/l results", "o/l exam", "ordinary level", "grade 11", "ol exam", "ol results"],
            "search_category": "ol_examination",
            "inferred_needs": ["exam_preparation", "child_education", "student_support", "academic_improvement"],
            "product_categories": ["Past Papers", "Tuition Classes", "Study Materials", "Educational Apps", "Books"],
            "target_user_profiles": {
                "teacher": {
                    "priority": 1,
                    "suggested_products": ["Degree Programs", "Professional Development Courses", "Teaching Materials", "Educational Technology"]
                },
                "parent": {
                    "priority": 1,
                    "suggested_products": ["O/L Past Papers", "Tuition Classes", "Study Guides", "Online Learning Platforms"]
                },
                "tech_professional": {
                    "priority": 2,
                    "suggested_products": ["O/L Past Papers", "Tuition Classes", "Educational Apps"],
                    "condition": "has_children"
                },
                "student": {
                    "priority": 1,
                    "suggested_products": ["Past Papers", "Study Materials", "Online Courses", "Reference Books"]
                }
            },
            "life_event_indicators": ["child_education_focus", "exam_preparation"],
            "confidence_weight": 0.90,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # A/L EXAMINATION SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["a/l results", "a/l exam", "advanced level", "grade 13", "al exam", "al results"],
            "search_category": "al_examination",
            "inferred_needs": ["university_preparation", "higher_education", "career_planning"],
            "product_categories": ["Past Papers", "Tuition Classes", "University Guides", "Career Counseling", "Study Materials"],
            "target_user_profiles": {
                "teacher": {
                    "priority": 1,
                    "suggested_products": ["Master's Degree Programs", "PhD Programs", "Professional Certifications"]
                },
                "parent": {
                    "priority": 1,
                    "suggested_products": ["A/L Past Papers", "Tuition Classes", "University Application Services"]
                },
                "student": {
                    "priority": 1,
                    "suggested_products": ["A/L Past Papers", "Revision Courses", "University Guides"]
                }
            },
            "life_event_indicators": ["university_planning", "career_preparation"],
            "confidence_weight": 0.90,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # DRIVING LICENSE SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["driving license", "licence", "learner permit", "driving test", "motor traffic"],
            "search_category": "driving_license",
            "inferred_needs": ["vehicle_purchase", "transportation", "mobility"],
            "product_categories": ["Cars for Sale", "Driving Schools", "Car Insurance", "Driving Theory Books", "Vehicle Loans"],
            "target_user_profiles": {
                "teacher": {
                    "priority": 1,
                    "suggested_products": ["Cars for Sale", "Driving Schools", "Car Insurance", "Degree Programs"]
                },
                "tech_professional": {
                    "priority": 1,
                    "suggested_products": ["Cars for Sale", "Car Insurance", "Vehicle Loans", "GPS Systems"]
                },
                "business_owner": {
                    "priority": 1,
                    "suggested_products": ["Commercial Vehicles", "Business Car Insurance", "Fleet Management"]
                },
                "student": {
                    "priority": 2,
                    "suggested_products": ["Driving Schools", "Driving Theory Books", "Budget Cars"]
                }
            },
            "life_event_indicators": ["vehicle_purchase_planning", "mobility_upgrade"],
            "confidence_weight": 0.85,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # BIRTH CERTIFICATE SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["birth certificate", "birth registration", "newborn", "baby registration"],
            "search_category": "birth_certificate",
            "inferred_needs": ["new_parent", "baby_care", "family_planning"],
            "product_categories": ["Baby Products", "Parenting Courses", "Child Insurance", "Educational Plans", "Baby Care Services"],
            "target_user_profiles": {
                "all": {
                    "priority": 1,
                    "suggested_products": ["Baby Products", "Parenting Books", "Child Insurance", "Educational Savings Plans"]
                }
            },
            "life_event_indicators": ["new_parent", "family_expansion"],
            "confidence_weight": 0.98,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # MARRIAGE CERTIFICATE SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["marriage certificate", "marriage registration", "wedding registration"],
            "search_category": "marriage_certificate",
            "inferred_needs": ["wedding_planning", "family_establishment", "legal_documentation"],
            "product_categories": ["Wedding Services", "Home Loans", "Insurance Plans", "Furniture", "Legal Services"],
            "target_user_profiles": {
                "all": {
                    "priority": 1,
                    "suggested_products": ["Wedding Photography", "Wedding Planners", "Home Loans", "Life Insurance"]
                }
            },
            "life_event_indicators": ["getting_married", "family_planning"],
            "confidence_weight": 0.95,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # LAND/PROPERTY REGISTRATION SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["land registration", "property deed", "land deed", "property registration", "land certificate"],
            "search_category": "property_land",
            "inferred_needs": ["property_purchase", "investment", "home_building"],
            "product_categories": ["Legal Services", "Survey Services", "Home Insurance", "Construction Materials", "Interior Design", "Architects"],
            "target_user_profiles": {
                "tech_professional": {
                    "priority": 1,
                    "suggested_products": ["Legal Services", "Smart Home Systems", "Home Insurance", "Interior Design"]
                },
                "business_owner": {
                    "priority": 1,
                    "suggested_products": ["Commercial Property Services", "Legal Consultation", "Business Insurance"]
                },
                "teacher": {
                    "priority": 2,
                    "suggested_products": ["Home Loans", "Legal Services", "Construction Materials"]
                }
            },
            "life_event_indicators": ["property_purchase", "home_building", "investment"],
            "confidence_weight": 0.92,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # NATIONAL ID SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["national id", "nic", "identity card", "national identity"],
            "search_category": "national_id",
            "inferred_needs": ["adult_transition", "legal_documentation", "official_processes"],
            "product_categories": ["Banking Services", "Insurance Plans", "Educational Courses", "Employment Services"],
            "target_user_profiles": {
                "student": {
                    "priority": 1,
                    "suggested_products": ["Bank Accounts", "Student Insurance", "Employment Services", "Career Guidance"]
                },
                "young_adult": {
                    "priority": 1,
                    "suggested_products": ["Banking Services", "Insurance Plans", "Career Courses"]
                }
            },
            "life_event_indicators": ["adult_transition", "independence"],
            "confidence_weight": 0.75,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # EMPLOYMENT/JOB SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["job vacancy", "government job", "employment", "career", "recruitment"],
            "search_category": "employment",
            "inferred_needs": ["job_seeking", "career_change", "skill_development"],
            "product_categories": ["Professional Courses", "Resume Services", "Career Counseling", "Interview Preparation", "Skills Training"],
            "target_user_profiles": {
                "student": {
                    "priority": 1,
                    "suggested_products": ["Career Guidance", "Skills Training", "Resume Writing", "Interview Coaching"]
                },
                "tech_professional": {
                    "priority": 1,
                    "suggested_products": ["Advanced Certifications", "Leadership Courses", "MBA Programs"]
                },
                "teacher": {
                    "priority": 1,
                    "suggested_products": ["Educational Certifications", "Master's Programs", "Teaching Diplomas"]
                }
            },
            "life_event_indicators": ["job_seeking", "career_transition"],
            "confidence_weight": 0.88,
            "created_at": datetime.utcnow()
        },
        
        # ==========================================
        # HEALTH/MEDICAL SEARCHES
        # ==========================================
        {
            "government_search_keywords": ["health certificate", "medical report", "vaccination", "health services"],
            "search_category": "health_medical",
            "inferred_needs": ["health_management", "medical_care", "wellness"],
            "product_categories": ["Health Insurance", "Fitness Equipment", "Medical Consultations", "Wellness Programs", "Nutrition Plans"],
            "target_user_profiles": {
                "all": {
                    "priority": 1,
                    "suggested_products": ["Health Insurance", "Fitness Memberships", "Medical Check-up Packages", "Wellness Apps"]
                }
            },
            "life_event_indicators": ["health_focus", "wellness_planning"],
            "confidence_weight": 0.80,
            "created_at": datetime.utcnow()
        }
    ]
    
    # Insert all mappings
    result = db.search_to_product_mappings.insert_many(mappings)
    print(f"✅ Inserted {len(result.inserted_ids)} search mappings")
    
    # Create indexes for faster queries
    db.search_to_product_mappings.create_index("government_search_keywords")
    db.search_to_product_mappings.create_index("search_category")
    print("✅ Created indexes on search_to_product_mappings collection")

if __name__ == "__main__":
    print("🌱 Seeding Government Search to Product Mappings...")
    print("=" * 60)
    
    clear_existing_mappings()
    seed_mappings()
    
    print("=" * 60)
    print("✅ Seeding completed successfully!")
    print(f"📊 Total mappings: {db.search_to_product_mappings.count_documents({})}")