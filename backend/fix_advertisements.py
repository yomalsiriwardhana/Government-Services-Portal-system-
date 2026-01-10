"""
Fix Advertisement Database - Copy Products to Advertisements Collection
This script copies products from 'products' collection to 'advertisements' collection
with proper field validation to fix the NoneType errors
"""

from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'government_portal'

print("🔌 Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

products_collection = db.products
advertisements_collection = db.advertisements

print("✅ Connected to database")
print("=" * 60)

# Step 1: Clear old advertisements
print("\n🗑️  Clearing old advertisements...")
result = advertisements_collection.delete_many({})
print(f"✅ Deleted {result.deleted_count} old advertisements")

# Step 2: Get all products
print("\n📦 Fetching products...")
products = list(products_collection.find({}))
print(f"✅ Found {len(products)} products")

if len(products) == 0:
    print("\n❌ ERROR: No products found!")
    print("❌ Please run: python seed_products_enhanced.py first")
    exit(1)

# Step 3: Convert products to advertisements format
print("\n🔄 Converting products to advertisements...")
converted_count = 0
error_count = 0

for product in products:
    try:
        # Create advertisement document with proper validation
        ad_doc = {
            '_id': product.get('_id'),
            'title': product.get('title', 'Untitled Product'),
            'description': product.get('description', ''),
            'image_url': product.get('image_url', ''),
            'link_url': product.get('link_url', ''),
            'category': product.get('category', 'General'),
            'subcategory': product.get('subcategory', ''),
            'brand': product.get('brand', ''),
            'price': product.get('price', 0),
            'stock': product.get('stock', 0),
            'featured': product.get('featured', False),
            
            # Targeting criteria (required for scoring)
            'target_age_min': product.get('target_age_min', 18),
            'target_age_max': product.get('target_age_max', 65),
            'target_locations': product.get('target_locations', []),
            'target_jobs': product.get('target_jobs', []),
            'target_categories': product.get('target_categories', []),
            
            # Keywords (required for behavior matching)
            'keywords': product.get('keywords', []),
            
            # Ad management fields
            'is_active': True,
            'budget': product.get('price', 0) * 0.1,  # 10% of price as budget
            'bid_amount': max(5.0, product.get('price', 0) * 0.001),  # 0.1% of price
            
            # Performance tracking
            'impressions': 0,
            'clicks': 0,
            'conversions': 0,
            'total_spent': 0.0,
            
            # Timestamps
            'created_at': product.get('created_at', datetime.utcnow()),
            'updated_at': datetime.utcnow()
        }
        
        # Validate critical fields
        if not ad_doc['title']:
            ad_doc['title'] = 'Product'
        if not ad_doc['description']:
            ad_doc['description'] = 'No description available'
        if not ad_doc['category']:
            ad_doc['category'] = 'General'
        
        # Ensure keywords is a list
        if not isinstance(ad_doc['keywords'], list):
            ad_doc['keywords'] = []
        
        # Ensure target fields are lists
        if not isinstance(ad_doc['target_locations'], list):
            ad_doc['target_locations'] = []
        if not isinstance(ad_doc['target_jobs'], list):
            ad_doc['target_jobs'] = []
        if not isinstance(ad_doc['target_categories'], list):
            ad_doc['target_categories'] = []
        
        # Insert into advertisements collection
        advertisements_collection.insert_one(ad_doc)
        converted_count += 1
        print(f"✅ Converted: {ad_doc['title']}")
        
    except Exception as e:
        error_count += 1
        print(f"❌ Error converting product: {e}")

print("\n" + "=" * 60)
print(f"✨ Conversion complete!")
print(f"   ✅ Successfully converted: {converted_count} products")
print(f"   ❌ Errors: {error_count}")

# Step 4: Verify
print("\n🔍 Verifying advertisements...")
ad_count = advertisements_collection.count_documents({})
print(f"✅ Total advertisements in database: {ad_count}")

# Show sample
print("\n📋 Sample advertisement:")
sample = advertisements_collection.find_one({})
if sample:
    print(f"   Title: {sample.get('title')}")
    print(f"   Category: {sample.get('category')}")
    print(f"   Keywords: {sample.get('keywords')}")
    print(f"   Target Age: {sample.get('target_age_min')}-{sample.get('target_age_max')}")
    print(f"   Target Jobs: {sample.get('target_jobs')}")

print("\n🎉 Database fix completed successfully!")
print("=" * 60)
print("\n✅ Now restart your Flask server and try searching again!")
print("   The NoneType errors should be gone!")