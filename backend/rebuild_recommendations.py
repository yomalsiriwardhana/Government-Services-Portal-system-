# Complete script to rebuild recommendations.py with ALL methods
import os

print("Reading existing file...")
with open('routes/recommendations.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract working sections
header_section = ''.join(lines[:77])  # Up to __init__ method
api_routes_section = ''.join(lines[289:])  # From first API route to end

# The COMPLETE class methods (all scoring methods + get_recommendations)
complete_class_methods = '''    
    def calculate_government_search_intent_score(self, product, user_id):
        """
        Calculate score based on government search intent (0-25 points)
        Matches product tags with user's government searches and inferred needs
        """
        score = 0
        
        analyzer = SearchAnalyzer(self.db)
        patterns = analyzer.get_user_search_patterns(user_id, days=30)
        
        government_searches = [
            s for s in patterns.get('recent_searches', []) 
            if s.get('is_government_search', False)
        ]
        
        if not government_searches:
            return 0
        
        product_gov_services = product.get('related_government_services', [])
        product_solves_needs = product.get('solves_user_needs', [])
        product_trigger_scenarios = product.get('trigger_scenarios', [])
        
        if not product_gov_services and not product_solves_needs:
            return 0
        
        all_inferred_needs = patterns.get('inferred_needs', [])
        
        if product_solves_needs and all_inferred_needs:
            matching_needs = set(product_solves_needs) & set(all_inferred_needs)
            if matching_needs:
                need_match_score = min(len(matching_needs) * 3, 10)
                score += need_match_score
        
        recent_search_categories = [s.get('search_category') for s in government_searches[:5]]
        
        for category in recent_search_categories:
            if category and any(category in trigger for trigger in product_trigger_scenarios):
                score += 5
                break
            elif category and any(keyword in category for keyword in product_gov_services):
                score += 3
        
        score = min(score, 10)
        
        most_recent_gov_search = government_searches[0] if government_searches else None
        
        if most_recent_gov_search:
            search_timestamp = most_recent_gov_search.get('timestamp')
            if search_timestamp:
                hours_ago = (datetime.utcnow() - search_timestamp).total_seconds() / 3600
                
                if hours_ago < 24:
                    score += 5
                elif hours_ago < 72:
                    score += 3
                elif hours_ago < 168:
                    score += 1
        
        return min(score, 25)
    
    def calculate_profile_match_score(self, ad, user, user_profile):
        """
        Calculate profile match score (0-25 points)
        Based on: age, location, job match
        """
        score = 0
        
        user_age = user.get('age')
        target_age_min = ad.get('target_age_min')
        target_age_max = ad.get('target_age_max')
        
        if user_age and target_age_min is not None and target_age_max is not None:
            if target_age_min <= user_age <= target_age_max:
                score += 10
            else:
                age_diff = min(
                    abs(user_age - target_age_min),
                    abs(user_age - target_age_max)
                )
                if age_diff <= 5:
                    score += max(0, 10 - (age_diff * 2))
        
        user_location = user.get('location') or ''
        user_location = user_location.lower() if user_location else ''
        
        target_locations = ad.get('target_locations') or []
        target_locations = [loc.lower() for loc in target_locations if loc]
        
        if target_locations:
            if user_location in target_locations or 'all' in target_locations:
                score += 8
        else:
            score += 8
        
        user_job = user.get('job', '') or ''
        user_job = user_job.lower() if user_job else ''
        
        target_jobs = ad.get('target_jobs') or []
        target_jobs = [job.lower() for job in target_jobs if job]
        
        if target_jobs:
            if user_job in target_jobs:
                score += 7
            elif user_job and any(job in user_job or user_job in job for job in target_jobs):
                score += 4
        else:
            score += 3
        
        return score
    
    def calculate_interest_match_score(self, ad, user_profile):
        """
        Calculate interest match score (0-30 points)
        Based on user's interest profile
        """
        score = 0
        
        ad_category = (ad.get('category') or '').lower()
        interest_scores = user_profile.get('interest_scores', {})
        
        for interest, interest_score in interest_scores.items():
            if interest.lower() == ad_category:
                score = interest_score * 30
                break
            elif interest.lower() in ad_category or ad_category in interest.lower():
                score = interest_score * 20
                break
        
        if score == 0 and interest_scores:
            top_interests = sorted(interest_scores.items(), key=lambda x: x[1], reverse=True)[:3]
            for interest, interest_score in top_interests:
                if interest.lower() in ad_category or ad_category in interest.lower():
                    score = interest_score * 15
                    break
        
        return round(score, 2)
    
    def calculate_behavior_match_score(self, ad, user_id, user_profile):
        """
        Calculate behavioral match score (0-25 points)
        Based on recent searches, clicks, and browsing patterns
        """
        score = 0
        
        ad_category = (ad.get('category') or '').lower()
        ad_title = (ad.get('title') or '').lower()
        ad_description = (ad.get('description') or '').lower()
        
        recent_searches = user_profile.get('recent_searches', [])[-10:]
        search_match_count = 0
        
        for search_entry in recent_searches:
            search_query = (search_entry.get('query') or '').lower()
            search_category = (search_entry.get('category') or '').lower()
            
            if search_category == ad_category:
                search_match_count += 1
            
            search_words = search_query.split()
            for word in search_words:
                if len(word) > 3 and (word in ad_title or word in ad_description):
                    search_match_count += 0.5
        
        score += min(search_match_count * 2, 12)
        
        recent_clicks = user_profile.get('recent_clicks', [])[-10:]
        click_match_count = 0
        
        for click_entry in recent_clicks:
            click_category = (click_entry.get('category') or '').lower()
            
            if click_category == ad_category:
                click_match_count += 1
        
        score += min(click_match_count * 2, 8)
        
        search_keywords = user_profile.get('search_keywords', {})
        keyword_match_score = 0
        
        for keyword, frequency in search_keywords.items():
            if keyword in ad_title or keyword in ad_description:
                keyword_match_score += min(frequency * 0.5, 2)
        
        score += min(keyword_match_score, 5)
        
        return round(score, 2)
    
    def calculate_life_event_match_score(self, ad, user_profile):
        """
        Calculate life event match score (0-20 points)
        Based on detected life events from user behavior
        """
        score = 0
        
        detected_events = user_profile.get('detected_life_events', [])
        ad_category = (ad.get('category') or '').lower()
        ad_title = (ad.get('title') or '').lower()
        ad_description = (ad.get('description') or '').lower()
        
        event_relevance = {
            'job_search': ['education', 'employment', 'course', 'training', 'career', 'resume', 'interview'],
            'marriage_planning': ['health', 'insurance', 'housing', 'property', 'financial', 'wedding', 'family'],
            'new_baby': ['health', 'insurance', 'medical', 'family', 'baby', 'maternity', 'pediatric'],
            'education': ['education', 'course', 'training', 'learning', 'school', 'university', 'exam'],
            'property_search': ['housing', 'property', 'land', 'real estate', 'mortgage', 'apartment', 'house'],
            'vehicle_purchase': ['transport', 'vehicle', 'car', 'bike', 'driving', 'insurance', 'loan'],
            'business_start': ['business', 'startup', 'company', 'entrepreneur', 'registration', 'finance', 'accounting'],
            'travel_planning': ['travel', 'immigration', 'passport', 'visa', 'tour', 'flight', 'hotel'],
            'health_concern': ['health', 'medical', 'insurance', 'hospital', 'doctor', 'checkup', 'wellness']
        }
        
        for event in detected_events:
            if event in event_relevance:
                relevant_keywords = event_relevance[event]
                
                for keyword in relevant_keywords:
                    if keyword in ad_category or keyword in ad_title or keyword in ad_description:
                        score += 5
                        break
        
        score = min(score, 20)
        
        return score
    
    def calculate_total_score(self, ad, user, user_profile, user_id):
        """
        Calculate total relevance score for an advertisement
        
        Scoring breakdown (125 points total, normalized to 100):
        - Profile Match: 20% (0-25 points)
        - Interest Match: 24% (0-30 points)
        - Behavior Match: 20% (0-25 points)
        - Life Event Match: 16% (0-20 points)
        - Government Search Intent: 20% (0-25 points)
        Total: 125 points (normalized to 100)
        """
        
        profile_score = self.calculate_profile_match_score(ad, user, user_profile)
        interest_score = self.calculate_interest_match_score(ad, user_profile)
        behavior_score = self.calculate_behavior_match_score(ad, user_id, user_profile)
        life_event_score = self.calculate_life_event_match_score(ad, user_profile)
        gov_search_score = self.calculate_government_search_intent_score(ad, user_id)
        
        total_raw = profile_score + interest_score + behavior_score + life_event_score + gov_search_score
        total_score = (total_raw / 125) * 100
        
        return {
            'total_score': round(total_score, 2),
            'profile_score': round(profile_score, 2),
            'interest_score': round(interest_score, 2),
            'behavior_score': round(behavior_score, 2),
            'life_event_score': round(life_event_score, 2),
            'government_search_intent_score': round(gov_search_score, 2)
        }
    
    def get_recommendations(self, user_id, limit=5):
        """
        Get personalized ad recommendations for a user
        
        Args:
            user_id (str): User ID
            limit (int): Number of recommendations to return
            
        Returns:
            list: Ranked list of recommended advertisements
        """
        
        user = self.user_model.find_by_id(user_id)
        if not user:
            return []
        
        user_profile = self.profile_model.create_or_get(user_id)
        
        analyzer = SearchAnalyzer(self.db)
        user_profile_type = analyzer._determine_user_profile_type(user)
        
        all_products = list(self.db.products.find({
            'is_active': {'$ne': False}
        }))
        
        if not all_products:
            all_ads = self.ad_model.get_all_active(limit=50)
            all_products = all_ads
        
        prioritized_products = []
        other_products = []
        
        for product in all_products:
            best_for_types = product.get('best_for_user_types', [])
            
            if user_profile_type in best_for_types or 'all' in best_for_types:
                prioritized_products.append(product)
            else:
                other_products.append(product)
        
        all_products = prioritized_products + other_products
        
        scored_products = []
        
        for product in all_products:
            try:
                scores = self.calculate_total_score(product, user, user_profile, user_id)
                
                product['relevance_score'] = scores['total_score']
                product['score_breakdown'] = {
                    'profile_match': scores['profile_score'],
                    'interest_match': scores['interest_score'],
                    'behavior_match': scores['behavior_score'],
                    'life_event_match': scores['life_event_score'],
                    'government_search_intent': scores['government_search_intent_score']
                }
                
                if scores['total_score'] > 5:
                    scored_products.append(product)
                
            except Exception as e:
                print(f"Error scoring product {product.get('_id')}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_products[:limit]

# ========================================
# API ENDPOINTS
# ========================================

@recommendations_bp.route('/recommendations', methods=['GET'])
@token_required
def get_personalized_ads(current_user_id):
    """
'''

# Build complete file
complete_file = header_section + complete_class_methods + api_routes_section

# Write to new file
output_path = 'routes/recommendations_COMPLETE.py'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(complete_file)

print(f"✅ Created complete file: {output_path}")
print(f"   Total size: {len(complete_file)} bytes")
print(f"   - Header: {len(header_section)} bytes")
print(f"   - Methods: {len(complete_class_methods)} bytes")
print(f"   - API Routes: {len(api_routes_section)} bytes")
print("\nNow replacing the corrupted file...")

# Back up corrupted file one more time
os.replace('routes/recommendations.py', 'routes/recommendations_corrupted.py.bak')
print("✅ Backed up corrupted file")

# Replace with complete file
os.replace(output_path, 'routes/recommendations.py')
print("✅ Replaced with complete working file!")
print("\nFile is ready. Testing syntax...")
