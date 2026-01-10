"""
Enhanced Search Analyzer with Government Search Intent Detection
Analyzes user searches to understand their real needs beyond the search query
"""

from datetime import datetime, timedelta
from bson import ObjectId

class SearchAnalyzer:
    """Analyzes search patterns and detects user intent"""
    
    def __init__(self, db):
        self.db = db
        self.search_history_collection = db.search_history
        self.user_collection = db.users
        self.mappings_collection = db.search_to_product_mappings
    
    def analyze_search_query(self, user_id, search_query):
        """
        Analyze a search query to detect if it's government-related
        and infer the user's real commercial needs
        """
        search_query_lower = search_query.lower().strip()
        
        # Get user profile for context
        user = self.user_collection.find_one({'_id': ObjectId(user_id)})
        
        # Detect government search intent
        government_intent = self._detect_government_intent(search_query_lower, user)
        
        if government_intent:
            # This is a government search - extract commercial needs
            return {
                'is_government_search': True,
                'search_category': government_intent['category'],
                'inferred_needs': government_intent['needs'],
                'recommended_product_categories': government_intent['product_categories'],
                'life_event_indicators': government_intent['life_events'],
                'confidence_score': government_intent['confidence'],
                'user_context': self._get_user_context(user)
            }
        else:
            # Regular product search
            return {
                'is_government_search': False,
                'search_category': 'direct_product_search',
                'inferred_needs': [],
                'recommended_product_categories': [],
                'life_event_indicators': [],
                'confidence_score': 0.5,
                'user_context': self._get_user_context(user)
            }
    
    def _detect_government_intent(self, search_query, user):
        """
        Detect if search is government-related and what the user really needs
        """
        # Find matching government search mappings
        mappings = self.mappings_collection.find({})
        
        best_match = None
        highest_match_score = 0
        
        for mapping in mappings:
            keywords = mapping.get('government_search_keywords', [])
            
            # Check if any keyword matches the search query
            match_count = 0
            for keyword in keywords:
                if keyword.lower() in search_query:
                    match_count += 1
            
            # Calculate match score
            if match_count > 0:
                match_score = match_count / len(keywords)
                
                if match_score > highest_match_score:
                    highest_match_score = match_score
                    best_match = mapping
        
        # If we found a match with confidence > 0.3
        if best_match and highest_match_score > 0.3:
            # Get user-specific recommendations based on profile
            user_profile_type = self._determine_user_profile_type(user)
            
            # Get targeted products for this user type
            target_profiles = best_match.get('target_user_profiles', {})
            user_specific_data = target_profiles.get(user_profile_type, target_profiles.get('all', {}))
            
            return {
                'category': best_match.get('search_category'),
                'needs': best_match.get('inferred_needs', []),
                'product_categories': best_match.get('product_categories', []),
                'life_events': best_match.get('life_event_indicators', []),
                'confidence': best_match.get('confidence_weight', 0.5) * highest_match_score,
                'user_specific_suggestions': user_specific_data.get('suggested_products', []),
                'priority': user_specific_data.get('priority', 2)
            }
        
        return None
    
    def _determine_user_profile_type(self, user):
        """
        Determine user's profile type based on job, age, and family status
        """
        if not user:
            return 'all'
        
        job = (user.get('job') or '').lower()
        age = user.get('age', 0)
        children = user.get('children', [])
        ai_categories = user.get('ai_categories', [])
        
        # Check for specific professions first
        if 'teacher' in job or 'lecturer' in job or 'professor' in job:
            return 'teacher'
        
        if any(word in job for word in ['software', 'developer', 'engineer', 'programmer', 'it', 'tech']):
            return 'tech_professional'
        
        if 'business' in job or 'entrepreneur' in job or 'owner' in job or 'ceo' in job:
            return 'business_owner'
        
        if 'student' in job or 'student' in ai_categories:
            return 'student'
        
        # Check if they're a parent
        if children and len(children) > 0:
            return 'parent'
        
        # Age-based categorization
        if 18 <= age <= 24:
            return 'young_adult'
        
        # Default
        return 'all'
    
    def _get_user_context(self, user):
        """
        Get user context for better recommendations
        """
        if not user:
            return {}
        
        return {
            'profession': user.get('job'),
            'age': user.get('age'),
            'location': user.get('location'),
            'has_children': len(user.get('children', [])) > 0,
            'ai_categories': user.get('ai_categories', []),
            'experience_years': user.get('experience_years', 0)
        }
    
    def track_search(self, user_id, search_query, search_type, results_count, intent_analysis):
        """
        Track search in history with intent analysis
        """
        search_record = {
            'user_id': ObjectId(user_id),
            'query': search_query,
            'search_type': search_type,
            'results_count': results_count,
            'timestamp': datetime.utcnow(),
            'is_government_search': intent_analysis.get('is_government_search', False),
            'search_category': intent_analysis.get('search_category'),
            'inferred_needs': intent_analysis.get('inferred_needs', []),
            'confidence_score': intent_analysis.get('confidence_score', 0),
            'clicked_results': []
        }
        
        result = self.search_history_collection.insert_one(search_record)
        
        # Update user's search count
        self.user_collection.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$inc': {'total_searches': 1},
                '$set': {'last_active': datetime.utcnow()}
            }
        )
        
        return str(result.inserted_id)
    
    def get_user_search_patterns(self, user_id, days=30):
        """
        Get user's search patterns over the last N days
        """
        since_date = datetime.utcnow() - timedelta(days=days)
        
        searches = list(self.search_history_collection.find({
            'user_id': ObjectId(user_id),
            'timestamp': {'$gte': since_date}
        }).sort('timestamp', -1))
        
        # Analyze patterns
        total_searches = len(searches)
        government_searches = [s for s in searches if s.get('is_government_search', False)]
        product_searches = [s for s in searches if not s.get('is_government_search', False)]
        
        # Collect all inferred needs
        all_inferred_needs = []
        for search in government_searches:
            all_inferred_needs.extend(search.get('inferred_needs', []))
        
        # Count category frequencies
        category_counts = {}
        for search in searches:
            category = search.get('search_category')
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_searches': total_searches,
            'government_searches_count': len(government_searches),
            'product_searches_count': len(product_searches),
            'inferred_needs': list(set(all_inferred_needs)),  # Unique needs
            'category_distribution': category_counts,
            'recent_searches': searches[:10]  # Last 10 searches
        }
    
    def detect_life_events(self, user_id, days=30):
        """
        Detect major life events based on search patterns
        """
        patterns = self.get_user_search_patterns(user_id, days)
        
        life_events = []
        
        # Check for specific life event patterns
        government_searches = [s for s in patterns['recent_searches'] if s.get('is_government_search')]
        
        # Count searches by category
        category_counts = {}
        for search in government_searches:
            category = search.get('search_category')
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Detect life events based on search frequency
        total_gov_searches = len(government_searches)
        
        if total_gov_searches > 0:
            # Passport/Immigration = Planning to travel/go abroad
            if category_counts.get('passport_immigration', 0) >= 2:
                confidence = min(category_counts.get('passport_immigration', 0) / total_gov_searches, 1.0)
                life_events.append({
                    'event_type': 'planning_travel_abroad',
                    'detected_at': datetime.utcnow(),
                    'confidence_score': confidence,
                    'evidence': f"{category_counts.get('passport_immigration')} passport/immigration searches"
                })
            
            # O/L or A/L searches = Child education focus or professional development
            ol_al_count = category_counts.get('ol_examination', 0) + category_counts.get('al_examination', 0)
            if ol_al_count >= 2:
                confidence = min(ol_al_count / total_gov_searches, 1.0)
                
                # Check user type to determine event type
                user = self.user_collection.find_one({'_id': ObjectId(user_id)})
                user_type = self._determine_user_profile_type(user)
                
                if user_type in ['parent', 'tech_professional'] and user.get('children'):
                    event_type = 'child_education_focus'
                elif user_type == 'teacher':
                    event_type = 'professional_development_interest'
                else:
                    event_type = 'education_interest'
                
                life_events.append({
                    'event_type': event_type,
                    'detected_at': datetime.utcnow(),
                    'confidence_score': confidence,
                    'evidence': f"{ol_al_count} examination-related searches"
                })
            
            # Driving license = Vehicle purchase planning
            if category_counts.get('driving_license', 0) >= 2:
                confidence = min(category_counts.get('driving_license', 0) / total_gov_searches, 1.0)
                life_events.append({
                    'event_type': 'vehicle_purchase_planning',
                    'detected_at': datetime.utcnow(),
                    'confidence_score': confidence,
                    'evidence': f"{category_counts.get('driving_license')} driving license searches"
                })
            
            # Birth certificate = New parent
            if category_counts.get('birth_certificate', 0) >= 1:
                life_events.append({
                    'event_type': 'new_parent',
                    'detected_at': datetime.utcnow(),
                    'confidence_score': 0.95,
                    'evidence': "Birth certificate search"
                })
            
            # Marriage certificate = Getting married
            if category_counts.get('marriage_certificate', 0) >= 1:
                life_events.append({
                    'event_type': 'getting_married',
                    'detected_at': datetime.utcnow(),
                    'confidence_score': 0.95,
                    'evidence': "Marriage certificate search"
                })
            
            # Property/Land = Property purchase
            if category_counts.get('property_land', 0) >= 2:
                confidence = min(category_counts.get('property_land', 0) / total_gov_searches, 1.0)
                life_events.append({
                    'event_type': 'property_purchase_planning',
                    'detected_at': datetime.utcnow(),
                    'confidence_score': confidence,
                    'evidence': f"{category_counts.get('property_land')} property-related searches"
                })
        
        return life_events
    
    def get_recommended_products_based_on_searches(self, user_id, limit=10):
        """
        Get product recommendations based on user's search history
        """
        patterns = self.get_user_search_patterns(user_id, days=30)
        
        # Collect all inferred needs
        inferred_needs = patterns.get('inferred_needs', [])
        
        if not inferred_needs:
            return []
        
        # Find products that solve these needs
        products = list(self.db.products.find({
            'solves_user_needs': {'$in': inferred_needs}
        }).limit(limit))
        
        return products