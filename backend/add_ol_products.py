"""
Add O/L specific products and update advertisement tags for context-aware ads
"""

from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

print("=" * 60)
print("Adding O/L Specific Products for Context-Aware Ads")
print("=" * 60)

# New O/L specific products to add
ol_products = [
    {
        'title': 'O/L Past Papers Collection 2024',
        'description': 'Complete collection of O/L past papers from 2015-2023 with model answers for all subjects.',
        'category': 'Education',
        'price': 2500,
        'image_url': 'https://example.com/images/ol-papers.jpg',
        'related_government_services': ['o/l results', 'education', 'examination'],
        'target_jobs': ['teacher', 'parent', 'student', 'all'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Premium O/L Tuition Classes - All Subjects',
        'description': 'Expert teachers for Mathematics, Science, English, and all O/L subjects. Online and offline classes.',
        'category': 'Education',
        'price': 15000,
        'image_url': 'https://example.com/images/tuition-class.jpg',
        'related_government_services': ['o/l results', 'education', 'examination'],
        'target_jobs': ['teacher', 'parent', 'student', 'all'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'title': 'Education Materials Kit for O/L Students',
        'description': 'Complete study kit with textbooks, revision guides, and practice tests for O/L examinations.',
        'category': 'Education',
        'price': 8500,
        'image_url': 'https://example.com/images/study-kit.jpg',
        'related_government_services': ['o/l results', 'education', 'examination'],
        'target_jobs': ['teacher', 'parent', 'student', 'all'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
    {
        'title': 'A/L Combined Maths Tuition - Online',
        'description': 'Expert coaching for A/L Combined Mathematics. One-on-one and group sessions available.',
        'category': 'Education',
        'price': 20000,
        'image_url': 'https://example.com/images/al-maths.jpg',
        'related_government_services': ['a/l results', 'education', 'examination'],
        'target_jobs': ['teacher', 'parent', 'student', 'all'],
        'is_active': True,
        'created_at': datetime.utcnow()
    },
]

# Add products to database
for product in ol_products:
    # Check if already exists
    existing = db.products.find_one({'title': product['title']})
    if not existing:
        db.products.insert_one(product)
        print(f"✅ Added: {product['title']}")
    else:
        # Update with tags
        db.products.update_one(
            {'_id': existing['_id']},
            {'$set': {
                'related_government_services': product['related_government_services'],
                'target_jobs': product['target_jobs']
            }}
        )
        print(f"📝 Updated: {product['title']}")

# Also update existing O/L & A/L Exam Preparation Classes ad
db.advertisements.update_many(
    {'title': {'$regex': 'O/L|A/L|Exam', '$options': 'i'}},
    {'$set': {
        'related_government_services': ['o/l results', 'a/l results', 'education', 'examination'],
        'target_jobs': ['teacher', 'parent', 'student', 'all']
    }}
)
print("\n📝 Updated existing O/L/A/L ads with proper tags")

# Verify
print("\n" + "=" * 60)
print("Verification:")
print("=" * 60)
print(f"\nProducts with 'o/l results' tag: {db.products.count_documents({'related_government_services': 'o/l results'})}")
print(f"Ads with 'o/l results' tag: {db.advertisements.count_documents({'related_government_services': 'o/l results'})}")

# Show tagged products
print("\nProducts tagged with o/l results:")
for p in db.products.find({'related_government_services': 'o/l results'}):
    print(f"  - {p.get('title', 'N/A')}")
