from datetime import datetime, timedelta
from bson import ObjectId

class UserProfile:
    """
    User Profile model for storing behavioral data and interest profiles
    Builds comprehensive user profiles from activities
    """
    
    def __init__(self, db):
        """Initialize with MongoDB database connection"""
        self.collection = db.user_profiles
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        try:
            self.collection.create_index([('user_id', 1)], unique=True)
            self.collection.create_index([('last_updated', -1)])
            print("✓ UserProfile indexes created")
        except Exception as e:
            print(f"Index creation note: {e}")
    
    def create_or_get(self, user_id):
        """
        Create a new profile or get existing one
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User profile data
        """
        profile = self.collection.find_one({'user_id': user_id})
        
        if not profile:
            # Create new profile
            profile_data = {
                'user_id': user_id,
                'interest_scores': {},  # e.g., {"Education": 0.8, "Technology": 0.6}
                'recent_searches': [],  # Last 20 searches
                'recent_clicks': [],  # Last 20 clicks
                'browsing_patterns': {
                    'peak_hours': [],  # Hours when user is most active
                    'active_days': [],  # Days of week user is active
                    'session_count': 0,
                    'avg_session_duration': 0
                },
                'detected_life_events': [],  # e.g., ["job_search", "marriage_planning"]
                'category_engagement': {},  # Time spent per category
                'search_keywords': {},  # Frequency of search keywords
                'total_searches': 0,
                'total_clicks': 0,
                'total_service_views': 0,
                'created_at': datetime.utcnow(),
                'last_updated': datetime.utcnow()
            }
            
            result = self.collection.insert_one(profile_data)
            profile_data['_id'] = result.inserted_id
            return profile_data
        
        return profile
    
    def get_by_user_id(self, user_id):
        """Get profile by user ID"""
        return self.collection.find_one({'user_id': user_id})
    
    def update_interest_scores(self, user_id, category, engagement_value=1):
        """
        Update interest scores based on user engagement
        Uses exponential moving average to keep scores current
        
        Args:
            user_id (str): User ID
            category (str): Category (Education, Technology, etc.)
            engagement_value (float): Engagement weight (1-5)
        """
        profile = self.create_or_get(user_id)
        
        current_scores = profile.get('interest_scores', {})
        
        # Calculate new score using weighted average
        alpha = 0.3  # Learning rate
        current_score = current_scores.get(category, 0)
        new_score = alpha * engagement_value + (1 - alpha) * current_score
        
        # Normalize to 0-1 range
        new_score = min(new_score, 1.0)
        
        current_scores[category] = round(new_score, 3)
        
        # Update database
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'interest_scores': current_scores,
                    'last_updated': datetime.utcnow()
                }
            }
        )
    
    def add_recent_search(self, user_id, search_query, category=None):
        """
        Add a search to recent searches (keep last 20)
        
        Args:
            user_id (str): User ID
            search_query (str): Search text
            category (str): Category of search
        """
        search_entry = {
            'query': search_query,
            'category': category,
            'timestamp': datetime.utcnow()
        }
        
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$push': {
                    'recent_searches': {
                        '$each': [search_entry],
                        '$slice': -20  # Keep only last 20
                    }
                },
                '$inc': {'total_searches': 1},
                '$set': {'last_updated': datetime.utcnow()}
            }
        )
        
        # Update interest score for this category
        if category:
            self.update_interest_scores(user_id, category, 0.5)
    
    def add_recent_click(self, user_id, item_type, item_id, category=None):
        """
        Add a click to recent clicks (keep last 20)
        
        Args:
            user_id (str): User ID
            item_type (str): 'service', 'product', 'ad'
            item_id (str): ID of clicked item
            category (str): Category of item
        """
        click_entry = {
            'type': item_type,
            'item_id': item_id,
            'category': category,
            'timestamp': datetime.utcnow()
        }
        
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$push': {
                    'recent_clicks': {
                        '$each': [click_entry],
                        '$slice': -20  # Keep only last 20
                    }
                },
                '$inc': {'total_clicks': 1},
                '$set': {'last_updated': datetime.utcnow()}
            }
        )
        
        # Update interest score for this category (higher weight for clicks)
        if category:
            self.update_interest_scores(user_id, category, 1.0)
    
    def detect_life_events(self, user_id):
        """
        Detect potential life events from search patterns
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: Detected life events
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return []
        
        recent_searches = profile.get('recent_searches', [])
        detected_events = []
        
        # Get recent search queries (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_queries = [
            s['query'].lower() 
            for s in recent_searches 
            if s.get('timestamp', datetime.utcnow()) > thirty_days_ago
        ]
        
        # Join all queries
        all_queries = ' '.join(recent_queries)
        
        # Life event patterns
        event_patterns = {
            'job_search': ['job', 'employment', 'career', 'resume', 'interview', 'hiring'],
            'marriage_planning': ['marriage', 'wedding', 'engagement', 'certificate'],
            'new_baby': ['birth', 'baby', 'maternity', 'paternity', 'newborn'],
            'education': ['university', 'college', 'degree', 'admission', 'course', 'exam'],
            'property_search': ['house', 'property', 'land', 'real estate', 'rent', 'mortgage'],
            'vehicle_purchase': ['vehicle', 'car', 'bike', 'license', 'registration'],
            'business_start': ['business', 'startup', 'company', 'registration', 'entrepreneur'],
            'travel_planning': ['passport', 'visa', 'travel', 'immigration'],
            'health_concern': ['health', 'hospital', 'medical', 'doctor', 'treatment']
        }
        
        for event, keywords in event_patterns.items():
            match_count = sum(1 for keyword in keywords if keyword in all_queries)
            # If 3+ related keywords found, likely a life event
            if match_count >= 3:
                detected_events.append(event)
        
        # Update profile with detected events
        self.collection.update_one(
            {'user_id': user_id},
            {'$set': {'detected_life_events': detected_events}}
        )
        
        return detected_events
    
    def update_search_keywords(self, user_id, keywords):
        """
        Update frequency count of search keywords
        
        Args:
            user_id (str): User ID
            keywords (list): List of keywords from search
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return
        
        keyword_freq = profile.get('search_keywords', {})
        
        for keyword in keywords:
            keyword = keyword.lower().strip()
            if len(keyword) > 2:  # Only meaningful keywords
                keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        # Keep only top 50 keywords
        if len(keyword_freq) > 50:
            sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)
            keyword_freq = dict(sorted_keywords[:50])
        
        self.collection.update_one(
            {'user_id': user_id},
            {'$set': {'search_keywords': keyword_freq}}
        )
    
    def get_top_interests(self, user_id, limit=5):
        """
        Get user's top interests by score
        
        Args:
            user_id (str): User ID
            limit (int): Number of top interests to return
            
        Returns:
            list: Top interests with scores
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return []
        
        interest_scores = profile.get('interest_scores', {})
        
        # Sort by score
        sorted_interests = sorted(
            interest_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_interests[:limit]
    
    def get_interest_profile_percentage(self, user_id):
        """
        Get interest profile as percentages
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Interest percentages
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return {}
        
        interest_scores = profile.get('interest_scores', {})
        
        # Calculate total score
        total_score = sum(interest_scores.values())
        
        if total_score == 0:
            return {}
        
        # Convert to percentages
        percentages = {}
        for category, score in interest_scores.items():
            percentages[category] = round((score / total_score) * 100, 1)
        
        return percentages
    
    def increment_service_views(self, user_id):
        """Increment total service views counter"""
        self.collection.update_one(
            {'user_id': user_id},
            {
                '$inc': {'total_service_views': 1},
                '$set': {'last_updated': datetime.utcnow()}
            }
        )
    
    def get_engagement_level(self, user_id):
        """
        Calculate user engagement level
        
        Args:
            user_id (str): User ID
            
        Returns:
            str: 'high', 'medium', or 'low'
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return 'new'
        
        total_activity = (
            profile.get('total_searches', 0) +
            profile.get('total_clicks', 0) +
            profile.get('total_service_views', 0)
        )
        
        if total_activity > 50:
            return 'high'
        elif total_activity > 20:
            return 'medium'
        elif total_activity > 5:
            return 'low'
        else:
            return 'new'
    
    def get_profile_summary(self, user_id):
        """
        Get comprehensive profile summary
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: Profile summary
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return None
        
        return {
            'user_id': user_id,
            'top_interests': self.get_top_interests(user_id, 5),
            'interest_percentages': self.get_interest_profile_percentage(user_id),
            'detected_life_events': profile.get('detected_life_events', []),
            'engagement_level': self.get_engagement_level(user_id),
            'total_searches': profile.get('total_searches', 0),
            'total_clicks': profile.get('total_clicks', 0),
            'total_service_views': profile.get('total_service_views', 0),
            'recent_searches': profile.get('recent_searches', [])[-5:],  # Last 5
            'last_updated': profile.get('last_updated')
        }