"""
Patch search.py to fix the /track endpoint
"""

# Read the file
with open('routes/search.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new /track endpoint code
new_track_endpoint = '''@search_bp.route('/track', methods=['POST'])
@token_required
def track_search_activity(current_user_id):
    """
    Track search activity - saves search to database for recommendation engine
    
    Request body:
        {
            "query": "passport",
            "search_type": "government_service" (optional)
        }
    """
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        search_type = data.get('search_type', 'general')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'query is required'
            }), 400
        
        db = current_app.db
        analyzer = SearchAnalyzer(db)
        
        # Analyze the search query to detect government intent
        intent_analysis = analyzer.analyze_search_query(current_user_id, query)
        
        # Track the search with intent analysis
        search_id = analyzer.track_search(
            user_id=current_user_id,
            search_query=query,
            search_type=search_type,
            results_count=0,
            intent_analysis=intent_analysis
        )
        
        print(f"✅ Search tracked: '{query}' by user {current_user_id}")
        print(f"   Government search: {intent_analysis.get('is_government_search')}")
        print(f"   Category: {intent_analysis.get('search_category')}")
        
        return jsonify({
            'success': True,
            'message': 'Search tracked successfully',
            'search_id': search_id,
            'is_government_search': intent_analysis.get('is_government_search'),
            'search_category': intent_analysis.get('search_category')
        })
        
    except Exception as e:
        print(f"Error tracking search: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500'''

# Find and replace the old /track endpoint
import re

# Pattern to find the /track endpoint (from @search_bp.route('/track') to the end of the function)
pattern = r"@search_bp\.route\('/track', methods=\['POST'\]\)\s*@token_required\s*def track_search_activity\(current_user_id\):.*?(?=\n@search_bp\.route|$)"

# Replace
new_content = re.sub(pattern, new_track_endpoint, content, flags=re.DOTALL)

# Write back
with open('routes/search.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ search.py patched successfully!")
print("   /track endpoint now accepts 'query' parameter")
print("   and properly saves searches to database")
