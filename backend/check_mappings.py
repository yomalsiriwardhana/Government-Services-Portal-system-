from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.government_portal

mappings = list(db.search_intent_mappings.find({}))

print(f"Total mappings in database: {len(mappings)}\n")

if len(mappings) == 0:
    print("NO MAPPINGS FOUND - This is the problem!")
    print("The SearchAnalyzer needs mapping data to detect government searches")
else:
    print("Mappings found:")
    for m in mappings[:10]:
        category = m.get('search_category', 'Unknown')
        keywords = m.get('government_search_keywords', [])
        print(f"\n{category}:")
        print(f"  Keywords: {keywords[:5]}")
        print(f"  Needs: {m.get('inferred_needs', [])}")
