"""
Search Tracking & Analysis Module - MongoDB Version
Tracks user searches and builds interest profiles for personalized recommendations
"""

from datetime import datetime, timedelta
from collections import Counter
import json
from bson import ObjectId

class SearchTracker:
    def __init__(self, db):
        """
        Initialize search tracker with MongoDB database
        Args:
            db: MongoDB database instance (e.g., client["citizen_portal"])
        """
        self.db = db
        self.search_history_col = db["search_history"]
        self.search_patterns_col = db["user_search_patterns"]
        self.users_col = db["users"]
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for search collections"""
        try:
            # Index on user_id and timestamp for search history
            self.search_history_col.create_index([("user_id", 1), ("timestamp", -1)])
            self.search_history_col.create_index("timestamp")
            
            # Index on user_id for search patterns
            self.search_patterns_col.create_index("user_id", unique=True)
            
            print("✅ Search tracker indexes created")
        except Exception as e:
            print(f"⚠️ Index creation warning: {e}")
    
    def track_search(self, user_id, query, category=None, results_count=0, session_id=None):
        """Track a user search"""
        timestamp = datetime.utcnow()
        
        # Record search in search_history collection
        search_doc = {
            "user_id": user_id,
            "query": query.lower(),
            "category": category,
            "timestamp": timestamp,
            "results_count": results_count,
            "clicked_result": None,
            "session_id": session_id
        }
        
        result = self.search_history_col.insert_one(search_doc)
        search_id = str(result.inserted_id)
        
        # Update search patterns
        self._update_search_patterns(user_id)
        
        # Re-categorize user based on search behavior
        self._recategorize_user(user_id)
        
        return search_id
    
    def track_click(self, search_id, clicked_result):
        """Track when user clicks on a search result"""
        try:
            self.search_history_col.update_one(
                {"_id": ObjectId(search_id)},
                {"$set": {"clicked_result": clicked_result}}
            )
        except Exception as e:
            print(f"Error tracking click: {e}")
    
    def _update_search_patterns(self, user_id):
        """Analyze and update user's search patterns"""
        
        # Get recent searches (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        searches = list(self.search_history_col.find({
            "user_id": user_id,
            "timestamp": {"$gte": thirty_days_ago}
        }).sort("timestamp", -1))
        
        if not searches:
            return
        
        # Extract keywords from queries
        all_keywords = []
        categories = []
        
        for search in searches:
            query = search.get("query", "")
            category = search.get("category")
            
            # Split query into keywords
            keywords = [word.strip() for word in query.lower().split() if len(word.strip()) > 2]
            all_keywords.extend(keywords)
            
            if category:
                categories.append(category)
        
        # Count top keywords
        keyword_counts = Counter(all_keywords)
        top_keywords = dict(keyword_counts.most_common(20))
        
        # Count top categories
        category_counts = Counter(categories)
        top_categories = dict(category_counts.most_common(10))
        
        # Calculate interest scores based on keywords
        interest_scores = self._calculate_interest_scores(top_keywords, top_categories)
        
        # Calculate search frequency
        search_frequency = self._calculate_search_frequency(len(searches), 30)
        
        # Update or insert patterns
        self.search_patterns_col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "user_id": user_id,
                    "search_count": len(searches),
                    "top_keywords": top_keywords,
                    "top_categories": top_categories,
                    "interest_scores": interest_scores,
                    "last_updated": datetime.utcnow(),
                    "search_frequency": search_frequency
                }
            },
            upsert=True
        )
    
    def _calculate_interest_scores(self, keywords, categories):
        """Calculate interest scores based on search patterns"""
        
        interest_scores = {}
        
        # Education-related keywords
        education_keywords = ['school', 'education', 'course', 'class', 'study', 'exam', 'test', 
                             'book', 'paper', 'university', 'college', 'teacher', 'student',
                             'o/l', 'a/l', 'grade', 'tuition', 'scholarship', 'admission']
        
        # Health-related keywords
        health_keywords = ['health', 'hospital', 'doctor', 'clinic', 'medical', 'medicine',
                          'treatment', 'disease', 'vaccine', 'appointment', 'surgery']
        
        # Business-related keywords
        business_keywords = ['business', 'register', 'company', 'tax', 'license', 'permit',
                            'trade', 'enterprise', 'startup', 'vat', 'commercial']
        
        # Employment-related keywords
        employment_keywords = ['job', 'work', 'employment', 'career', 'salary', 'position',
                              'hiring', 'vacancy', 'resume', 'interview', 'training']
        
        # Technology-related keywords
        tech_keywords = ['computer', 'software', 'internet', 'online', 'digital', 'app',
                        'website', 'tech', 'electronic', 'mobile', 'phone', 'laptop']
        
        # Transport-related keywords
        transport_keywords = ['vehicle', 'car', 'license', 'driving', 'transport', 'road',
                             'traffic', 'motor', 'registration', 'bike', 'bus']
        
        # Property-related keywords
        property_keywords = ['land', 'house', 'property', 'deed', 'building', 'real estate',
                            'rent', 'buy', 'apartment', 'home', 'construction']
        
        # Immigration-related keywords
        immigration_keywords = ['passport', 'visa', 'travel', 'immigration', 'embassy',
                               'foreign', 'abroad', 'migration', 'citizen']
        
        # Calculate scores
        keyword_list = list(keywords.keys())
        
        interest_scores['education'] = self._keyword_match_score(keyword_list, education_keywords)
        interest_scores['health'] = self._keyword_match_score(keyword_list, health_keywords)
        interest_scores['business'] = self._keyword_match_score(keyword_list, business_keywords)
        interest_scores['employment'] = self._keyword_match_score(keyword_list, employment_keywords)
        interest_scores['technology'] = self._keyword_match_score(keyword_list, tech_keywords)
        interest_scores['transport'] = self._keyword_match_score(keyword_list, transport_keywords)
        interest_scores['property'] = self._keyword_match_score(keyword_list, property_keywords)
        interest_scores['immigration'] = self._keyword_match_score(keyword_list, immigration_keywords)
        
        return interest_scores
    
    def _keyword_match_score(self, user_keywords, category_keywords):
        """Calculate how many user keywords match a category"""
        matches = sum(1 for kw in user_keywords if kw in category_keywords)
        return matches
    
    def _calculate_search_frequency(self, search_count, days):
        """Calculate search frequency category"""
        searches_per_day = search_count / days
        
        if searches_per_day >= 5:
            return 'very_active'
        elif searches_per_day >= 2:
            return 'active'
        elif searches_per_day >= 0.5:
            return 'moderate'
        else:
            return 'occasional'
    
    def _recategorize_user(self, user_id):
        """Re-categorize user based on search behavior"""
        
        # Get search patterns
        patterns = self.search_patterns_col.find_one({"user_id": user_id})
        
        if not patterns:
            return
        
        interest_scores = patterns.get("interest_scores", {})
        search_frequency = patterns.get("search_frequency", "occasional")
        
        # Get existing categories
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return
        
        # Get existing AI categories (handle both dict and list formats)
        ai_categories_data = user.get("ai_categories", {})
        
        if isinstance(ai_categories_data, dict):
            existing_categories = ai_categories_data.get("categories", [])
        elif isinstance(ai_categories_data, list):
            existing_categories = ai_categories_data
        else:
            existing_categories = []
        
        # Add new behavioral categories
        new_categories = set(existing_categories)
        
        # Add search-based categories
        if interest_scores.get('education', 0) >= 5:
            new_categories.add('education_seeker')
            new_categories.add('course_buyer')
        
        if interest_scores.get('technology', 0) >= 3:
            new_categories.add('tech_enthusiast')
            new_categories.add('electronics_buyer')
        
        if interest_scores.get('business', 0) >= 3:
            new_categories.add('business_owner')
            new_categories.add('entrepreneur')
        
        if interest_scores.get('employment', 0) >= 3:
            new_categories.add('job_seeker')
            new_categories.add('career_focused')
        
        if interest_scores.get('property', 0) >= 3:
            new_categories.add('property_seeker')
            new_categories.add('property_investor')
        
        if interest_scores.get('health', 0) >= 3:
            new_categories.add('health_focused')
        
        if interest_scores.get('immigration', 0) >= 3:
            new_categories.add('travel_seeker')
            new_categories.add('passport_applicant')
        
        # Add frequency-based categories
        if search_frequency in ['active', 'very_active']:
            new_categories.add('power_user')
            new_categories.add('engaged_user')
        
        # Update user categories
        # Keep the existing format (dict or list)
        if isinstance(ai_categories_data, dict):
            ai_categories_data['categories'] = list(new_categories)
            ai_categories_data['last_recategorized'] = datetime.utcnow()
            update_value = ai_categories_data
        else:
            update_value = list(new_categories)
        
        self.users_col.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"ai_categories": update_value}}
        )
        
        print(f"✅ User {user_id} re-categorized. New categories: {list(new_categories)}")
    
    def get_user_search_history(self, user_id, limit=20):
        """Get user's recent search history"""
        searches = list(self.search_history_col.find({
            "user_id": user_id
        }).sort("timestamp", -1).limit(limit))
        
        result = []
        for search in searches:
            result.append({
                'query': search.get('query'),
                'category': search.get('category'),
                'timestamp': search.get('timestamp').isoformat() if search.get('timestamp') else None,
                'results_count': search.get('results_count'),
                'clicked_result': search.get('clicked_result')
            })
        
        return result
    
    def get_user_search_patterns(self, user_id):
        """Get user's search patterns and interests"""
        patterns = self.search_patterns_col.find_one({"user_id": user_id})
        
        if not patterns:
            return None
        
        return {
            'search_count': patterns.get('search_count', 0),
            'top_keywords': patterns.get('top_keywords', {}),
            'top_categories': patterns.get('top_categories', {}),
            'interest_scores': patterns.get('interest_scores', {}),
            'last_updated': patterns.get('last_updated').isoformat() if patterns.get('last_updated') else None,
            'search_frequency': patterns.get('search_frequency', 'occasional')
        }
    
    def get_trending_searches(self, days=7, limit=10):
        """Get trending searches across all users"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Aggregate pipeline to count search queries
        pipeline = [
            {"$match": {"timestamp": {"$gte": cutoff_date}}},
            {"$group": {
                "_id": "$query",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": limit}
        ]
        
        results = list(self.search_history_col.aggregate(pipeline))
        
        trending = []
        for result in results:
            trending.append({
                'query': result['_id'],
                'count': result['count']
            })
        
        return trending
    
    def get_popular_categories(self, days=7):
        """Get most searched categories"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Aggregate pipeline to count categories
        pipeline = [
            {"$match": {
                "timestamp": {"$gte": cutoff_date},
                "category": {"$ne": None}
            }},
            {"$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        
        results = list(self.search_history_col.aggregate(pipeline))
        
        categories = {}
        for result in results:
            categories[result['_id']] = result['count']
        
        return categories