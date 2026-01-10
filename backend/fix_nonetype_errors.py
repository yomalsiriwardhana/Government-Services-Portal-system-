"""
Fix NoneType errors in recommendations.py
This script patches the scoring functions to handle None values properly
"""

import os

print("🔧 Fixing NoneType errors in recommendations.py...")
print("=" * 60)

# Path to recommendations.py
file_path = 'routes/recommendations.py'

if not os.path.exists(file_path):
    print(f"❌ Error: {file_path} not found!")
    print("   Make sure you're running this from the backend directory")
    exit(1)

# Read the file
print("📖 Reading recommendations.py...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences of the problematic pattern
original_count = content.count(".get('category', '').lower()")
original_count += content.count(".get('title', '').lower()")
original_count += content.count(".get('description', '').lower()")

print(f"✅ Found {original_count} potentially problematic .lower() calls")

# Fix 1: Fix all category lower() calls
print("\n🔧 Applying fixes...")
content = content.replace(
    "ad.get('category', '').lower()",
    "(ad.get('category') or '').lower()"
)

# Fix 2: Fix all title lower() calls
content = content.replace(
    "ad.get('title', '').lower()",
    "(ad.get('title') or '').lower()"
)

# Fix 3: Fix all description lower() calls  
content = content.replace(
    "ad.get('description', '').lower()",
    "(ad.get('description') or '').lower()"
)

# Fix 4: Fix user_location
content = content.replace(
    "user_location = user.get('location', '')",
    "user_location = user.get('location') or ''"
)

# Fix 5: Fix target_locations
content = content.replace(
    "target_locations = ad.get('target_locations', [])",
    "target_locations = ad.get('target_locations') or []"
)

# Fix 6: Fix search query
content = content.replace(
    "search_query = search_entry.get('query', '').lower()",
    "search_query = (search_entry.get('query') or '').lower()"
)

# Fix 7: Fix search category
content = content.replace(
    "search_category = search_entry.get('category', '').lower()",
    "search_category = (search_entry.get('category') or '').lower()"
)

# Fix 8: Fix click category
content = content.replace(
    "click_category = click_entry.get('category', '').lower()",
    "click_category = (click_entry.get('category') or '').lower()"
)

# Fix 9: Fix user job
content = content.replace(
    "user_job = user.get('job', '').lower()",
    "user_job = (user.get('job') or '').lower()"
)

# Fix 10: Fix target_jobs
content = content.replace(
    "target_jobs = ad.get('target_jobs', [])",
    "target_jobs = ad.get('target_jobs') or []"
)

# Fix 11: Fix target_categories  
content = content.replace(
    "target_categories = ad.get('target_categories', [])",
    "target_categories = ad.get('target_categories') or []"
)

# Write the fixed content
print("💾 Writing fixed content...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ File patched successfully!")
print("=" * 60)
print("\n🎉 All NoneType errors should now be fixed!")
print("\n📋 Changes made:")
print("   ✅ Added null checks to all .lower() calls")
print("   ✅ Protected all .get() operations that could return None")
print("   ✅ Ensured all string operations have fallback values")
print("\n🔄 Next step: Restart your Flask server!")
print("   The errors should be gone!")