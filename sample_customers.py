from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["citizen_portal"]
users_col = db["users"]

# Clear existing sample data
users_col.delete_many({"sample_data": True})

# Sample customer data
sample_customers = []

print("🔄 Generating sample customers...")
print("=" * 60)

# =============================================================================
# 1. Government employees without degrees (target for degree programs)
# =============================================================================
print("\n📋 Creating 15 government employees...")
for i in range(15):
    age = random.randint(35, 45)
    children_count = random.randint(1, 3)
    children_ages = [random.randint(5, 20) for _ in range(children_count)]
    
    customer = {
        "sample_data": True,
        "email": f"gov_employee_{i+1}@example.com",
        "name": f"Government Employee {i+1}",
        "phone": f"077{random.randint(1000000, 9999999)}",
        "age": age,
        "location": random.choice(["Colombo", "Kandy", "Gampaha", "Kalutara", "Galle"]),
        "interests": random.sample(["Education", "Business", "Technology", "Health"], k=2),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365)),
        "last_login": datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
        "is_active": True,
        "profile_completed": True,
        "engagement_count": random.randint(5, 50),
        "extended_profile": {
            "family": {
                "marital_status": "married",
                "children": [f"Child {j+1}" for j in range(children_count)],
                "children_ages": children_ages,
                "children_education": [random.choice(["primary", "secondary", "ol", "al", "tuition"]) for _ in range(children_count)],
                "dependents": children_count
            },
            "education": {
                "highest_qualification": random.choice(["ol", "al", "diploma"]),
                "institution": "Local School/College",
                "year_graduated": 2000 + random.randint(0, 10),
                "field_of_study": "General"
            },
            "career": {
                "current_job": f"Government {random.choice(['Clerk', 'Officer', 'Administrator', 'Supervisor'])}",
                "years_experience": age - 22,
                "skills": ["administration", "management", "public_service"],
                "career_goals": ["degree_completion", "promotion", "skill_development"]
            },
            "interests": {
                "hobbies": ["reading", "family_time", "community_service"],
                "learning_interests": ["degree_programs", "professional_courses", "language_courses"],
                "service_preferences": ["education", "career_development", "family_services"]
            },
            "consent": {
                "marketing_emails": True,
                "personalized_ads": True,
                "data_analytics": True
            }
        }
    }
    sample_customers.append(customer)

print(f"✅ Created {len(sample_customers)} government employees")

# =============================================================================
# 2. Young professionals (target for career development)
# =============================================================================
print("📋 Creating 15 young professionals...")
for i in range(15):
    age = random.randint(25, 35)
    has_children = random.random() > 0.7
    
    customer = {
        "sample_data": True,
        "email": f"young_pro_{i+1}@example.com",
        "name": f"Young Professional {i+1}",
        "phone": f"076{random.randint(1000000, 9999999)}",
        "age": age,
        "location": random.choice(["Colombo", "Kandy", "Negombo", "Moratuwa"]),
        "interests": random.sample(["Technology", "Business", "Education", "Employment"], k=2),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365)),
        "last_login": datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
        "is_active": True,
        "profile_completed": True,
        "engagement_count": random.randint(10, 60),
        "extended_profile": {
            "family": {
                "marital_status": random.choice(["single", "married"]),
                "children": ["Child 1"] if has_children else [],
                "children_ages": [random.randint(1, 5)] if has_children else [],
                "children_education": [] if not has_children else ["daycare"],
                "dependents": 1 if has_children else 0
            },
            "education": {
                "highest_qualification": random.choice(["degree", "diploma", "al"]),
                "institution": random.choice(["Local University", "Private Institute", "Government School"]),
                "year_graduated": 2015 + random.randint(0, 8),
                "field_of_study": random.choice(["IT", "Business", "Engineering", "Arts"])
            },
            "career": {
                "current_job": f"{random.choice(['IT', 'Marketing', 'Sales', 'Finance'])} {random.choice(['Executive', 'Officer', 'Associate'])}",
                "years_experience": age - 22,
                "skills": ["communication", "technical_skills", "teamwork"],
                "career_goals": ["overseas_opportunities", "higher_education", "skill_development"]
            },
            "interests": {
                "hobbies": ["technology", "travel", "learning", "socializing"],
                "learning_interests": ["ielts", "overseas_jobs", "professional_certifications"],
                "service_preferences": ["career_services", "education", "travel"]
            },
            "consent": {
                "marketing_emails": True,
                "personalized_ads": True,
                "data_analytics": True
            }
        }
    }
    sample_customers.append(customer)

print(f"✅ Created {len(sample_customers) - 15} young professionals")

# =============================================================================
# 3. Parents with school-going children (target for education services)
# =============================================================================
print("📋 Creating 20 parents with school-age children...")
for i in range(20):
    age = random.randint(40, 55)
    children_count = random.randint(1, 4)
    children_ages = [random.randint(5, 18) for _ in range(children_count)]
    
    customer = {
        "sample_data": True,
        "email": f"parent_{i+1}@example.com",
        "name": f"Parent {i+1}",
        "phone": f"075{random.randint(1000000, 9999999)}",
        "age": age,
        "location": random.choice(["Colombo", "Kandy", "Kurunegala", "Ratnapura", "Badulla"]),
        "interests": random.sample(["Education", "Health", "Business", "Housing"], k=2),
        "created_at": datetime.utcnow() - timedelta(days=random.randint(1, 365)),
        "last_login": datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
        "is_active": True,
        "profile_completed": True,
        "engagement_count": random.randint(15, 80),
        "extended_profile": {
            "family": {
                "marital_status": "married",
                "children": [f"Child {j+1}" for j in range(children_count)],
                "children_ages": children_ages,
                "children_education": [random.choice(["primary", "secondary", "ol_prep", "al_prep", "tuition"]) for _ in range(children_count)],
                "dependents": children_count
            },
            "education": {
                "highest_qualification": random.choice(["ol", "al", "degree", "diploma"]),
                "institution": "Various",
                "year_graduated": 1990 + random.randint(0, 15),
                "field_of_study": "General"
            },
            "career": {
                "current_job": random.choice(["Business Owner", "Teacher", "Government Officer", "Private Employee", "Professional"]),
                "years_experience": age - 25,
                "skills": ["management", "communication", "problem_solving"],
                "career_goals": ["children_education", "financial_security", "retirement_planning"]
            },
            "interests": {
                "hobbies": ["family_activities", "community_events", "reading"],
                "learning_interests": ["children_education", "exam_preparation", "extracurricular"],
                "service_preferences": ["education_services", "family_products", "financial_services"]
            },
            "consent": {
                "marketing_emails": True,
                "personalized_ads": True,
                "data_analytics": True
            }
        }
    }
    sample_customers.append(customer)

print(f"✅ Created {len(sample_customers) - 30} parents")

# Insert all sample customers
print("\n" + "=" * 60)
print("💾 Inserting customers into database...")

if sample_customers:
    result = users_col.insert_many(sample_customers)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} sample customers")
else:
    print("❌ No customers to insert")

print("\n" + "=" * 60)
print("📊 SUMMARY")
print("=" * 60)
print(f"Total sample customers created: {len(sample_customers)}")
print(f"Total users in database: {users_col.count_documents({})}")
print(f"Sample users in database: {users_col.count_documents({'sample_data': True})}")

# Show breakdown
print("\n📈 Customer Breakdown:")
print(f"   Government Employees: 15")
print(f"   Young Professionals: 15")
print(f"   Parents: 20")

# Show some sample segments
print("\n👥 Sample User Segments Available:")
segments = [
    "government_employee", "needs_qualification", "mid_career_family",
    "early_career", "young_adult", "parent", 
    "primary_school_parent", "secondary_school_parent", "university_age_parent"
]
for segment in segments:
    print(f"   - {segment}")

print("\n" + "=" * 60)
print("✅ Sample customer data generation complete!")
print("=" * 60)
print("\n💡 TIP: Refresh your admin dashboard to see the updated metrics!")
print("💡 TIP: Test recommendations with: http://localhost:5000/api/recommendations/<user_id>")