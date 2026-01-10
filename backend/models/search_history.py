from datetime import datetime, timedelta
from bson import ObjectId

class SearchHistory:
    """Search History model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db.search_history
    
    def create(self, search_data):
        """Record a new search"""
        search_data['timestamp'] = datetime.utcnow()
        result = self.collection.insert_one(search_data)
        return str(result.inserted_id)
    
    def find_by_user(self, user_id, days=30, limit=100):
        """Get user's search history"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        searches = list(
            self.collection.find({
                'user_id': user_id,
                'timestamp': {'$gte': cutoff_date}
            })
            .sort('timestamp', -1)
            .limit(limit)
        )
        
        for search in searches:
            search['_id'] = str(search['_id'])
        
        return searches
    
    def get_user_search_stats(self, user_id, days=30):
        """Get user's search statistics"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Total searches
        total_searches = self.collection.count_documents({
            'user_id': user_id,
            'timestamp': {'$gte': cutoff_date}
        })
        
        # Top categories
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': 5}
        ]
        
        top_categories = list(self.collection.aggregate(pipeline))
        
        # Top keywords
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$project': {
                    'keywords': {
                        '$split': [{'$toLower': '$query'}, ' ']
                    }
                }
            },
            {'$unwind': '$keywords'},
            {
                '$group': {
                    '_id': '$keywords',
                    'count': {'$sum': 1}
                }
            },
            {
                '$match': {
                    '_id': {'$nin': ['', 'the', 'a', 'an', 'and', 'or', 'for', 'to', 'of', 'in']}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        
        top_keywords = list(self.collection.aggregate(pipeline))
        
        # Activity level
        activity_level = self._calculate_activity_level(total_searches)
        
        return {
            'total_searches': total_searches,
            'top_categories': top_categories,
            'top_keywords': top_keywords,
            'activity_level': activity_level
        }
    
    def _calculate_activity_level(self, search_count):
        """Calculate user activity level"""
        if search_count == 0:
            return 'INACTIVE'
        elif search_count < 5:
            return 'LOW'
        elif search_count < 15:
            return 'MODERATE'
        elif search_count < 30:
            return 'ACTIVE'
        else:
            return 'VERY ACTIVE'
    
    def get_interest_profile(self, user_id, days=30):
        """Calculate user's interest profile based on searches"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        category_counts = list(self.collection.aggregate(pipeline))
        
        # Calculate total searches
        total = sum(item['count'] for item in category_counts)
        
        # Calculate percentages
        interest_profile = {}
        for item in category_counts:
            category = item['_id']
            if category:
                percentage = (item['count'] / total * 100) if total > 0 else 0
                interest_profile[category] = round(percentage, 1)
        
        return interest_profile
    
    def get_search_patterns(self, user_id, days=30):
        """Analyze user's search patterns"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all searches
        searches = list(self.collection.find({
            'user_id': user_id,
            'timestamp': {'$gte': cutoff_date}
        }))
        
        if not searches:
            return {}
        
        # Analyze patterns
        patterns = {
            'total_searches': len(searches),
            'unique_queries': len(set(s['query'].lower() for s in searches)),
            'avg_results_per_search': sum(s.get('results_count', 0) for s in searches) / len(searches),
            'click_through_rate': sum(1 for s in searches if s.get('clicked_service')) / len(searches) * 100,
            'most_searched_query': self._get_most_searched_query(searches),
            'search_frequency': self._calculate_search_frequency(searches, days)
        }
        
        return patterns
    
    def _get_most_searched_query(self, searches):
        """Get the most searched query"""
        from collections import Counter
        queries = [s['query'].lower() for s in searches]
        if queries:
            most_common = Counter(queries).most_common(1)
            return most_common[0][0] if most_common else None
        return None
    
    def _calculate_search_frequency(self, searches, days):
        """Calculate average searches per day"""
        if not searches or days == 0:
            return 0
        return len(searches) / days
    
    def get_trending_searches(self, days=7, limit=10):
        """Get trending searches across all users"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': {'$toLower': '$query'},
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': limit}
        ]
        
        trending = list(self.collection.aggregate(pipeline))
        
        return [
            {'query': item['_id'], 'count': item['count']}
            for item in trending
        ]
    
    def get_popular_categories(self, days=30):
        """Get popular search categories"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': cutoff_date},
                    'category': {'$exists': True, '$ne': None}
                }
            },
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}}
        ]
        
        categories = list(self.collection.aggregate(pipeline))
        
        return {
            item['_id']: item['count']
            for item in categories
        }