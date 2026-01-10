from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

# Check for passport/travel products
passport_products = list(db.products.find({
    'related_government_services': {'$in': ['passport', 'immigration', 'visa']}
}))

print(f"✅ Total passport/travel products: {len(passport_products)}")
print("\n📦 Passport-Related Products:")
print("=" * 70)

for i, product in enumerate(passport_products[:10], 1):
    print(f"\n{i}. {product['title']}")
    print(f"   Category: {product.get('category', 'N/A')}")
    print(f"   Price: Rs. {product.get('price', 0):,}")
    print(f"   Services: {', '.join(product.get('related_government_services', []))}")
    print(f"   Best for: {', '.join(product.get('best_for_user_types', []))}")

# Also check Travel category
travel_category = list(db.products.find({'category': 'Travel'}))
print(f"\n\n📋 Products in 'Travel' category: {len(travel_category)}")

# Check all products count
all_products = db.products.count_documents({})
print(f"\n📊 Total products in database: {all_products}")

# Show sample product details
if passport_products:
    print("\n\n🔍 SAMPLE PASSPORT PRODUCT DETAILS:")
    print("=" * 70)
    sample = passport_products[0]
    print(f"Title: {sample['title']}")
    print(f"Category: {sample.get('category')}")
    print(f"Price: Rs. {sample.get('price'):,}")
    print(f"Description: {sample.get('description', '')[:100]}...")
    print(f"\nGovernment Services Tags:")
    for service in sample.get('related_government_services', []):
        print(f"  ✓ {service}")
    print(f"\nSolves User Needs:")
    for need in sample.get('solves_user_needs', []):
        print(f"  ✓ {need}")
    print(f"\nBest For User Types:")
    for user_type in sample.get('best_for_user_types', []):
        print(f"  ✓ {user_type}")
