from datetime import datetime, timedelta
from bson import ObjectId

class UserActivity:
    """
    User Activity model for tracking all user actions
    Stores detailed logs of searches, clicks, and views
    """
    
    def __init__(self, db):
        """Initialize with MongoDB database connection"""
        self.collection = db.user_activities
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        try:
            self.collection.create_index([('user_id', 1), ('timestamp', -1)])
            self.collection.create_index([('activity_type', 1)])
            self.collection.create_index([('timestamp', -1)])
            print("✓ UserActivity indexes created")
        except Exception as e:
            print(f"Index creation note: {e}")
    
    def log_activity(self, user_id, activity_type, activity_data):
        """
        Log any user activity
        
        Args:
            user_id (str): User ID
            activity_type (str): 'search', 'click', 'view', 'ad_click'
            activity_data (dict): Additional activity data
            
        Returns:
            str: Activity ID
        """
        activity = {
            'user_id': user_id,
            'activity_type': activity_type,
            'timestamp': datetime.utcnow(),
            **activity_data  # Merge additional data
        }
        
        result = self.collection.insert_one(activity)
        return str(result.inserted_id)
    
    def log_search(self, user_id, query, category=None, results_count=0):
        """
        Log a search activity
        
        Args:
            user_id (str): User ID
            query (str): Search query
            category (str): Detected category
            results_count (int): Number of results returned
        """
        return self.log_activity(user_id, 'search', {
            'query': query,
            'category': category,
            'results_count': results_count
        })
    
    def log_service_view(self, user_id, service_id, service_name, category):
        """
        Log when user views a service
        
        Args:
            user_id (str): User ID
            service_id (str): Service ID
            service_name (str): Service name
            category (str): Service category
        """
        return self.log_activity(user_id, 'service_view', {
            'service_id': service_id,
            'service_name': service_name,
            'category': category
        })
    
    def log_product_view(self, user_id, product_id, product_name, category):
        """
        Log when user views a product
        
        Args:
            user_id (str): User ID
            product_id (str): Product ID
            product_name (str): Product name
            category (str): Product category
        """
        return self.log_activity(user_id, 'product_view', {
            'product_id': product_id,
            'product_name': product_name,
            'category': category
        })
    
    def log_ad_impression(self, user_id, ad_id, ad_title, position):
        """
        Log when user sees an ad (impression)
        
        Args:
            user_id (str): User ID
            ad_id (str): Advertisement ID
            ad_title (str): Ad title
            position (int): Ad position (1, 2, 3...)
        """
        return self.log_activity(user_id, 'ad_impression', {
            'ad_id': ad_id,
            'ad_title': ad_title,
            'position': position
        })
    
    def log_ad_click(self, user_id, ad_id, ad_title, ad_category):
        """
        Log when user clicks an ad
        
        Args:
            user_id (str): User ID
            ad_id (str): Advertisement ID
            ad_title (str): Ad title
            ad_category (str): Ad category
        """
        return self.log_activity(user_id, 'ad_click', {
            'ad_id': ad_id,
            'ad_title': ad_title,
            'ad_category': ad_category
        })
    
    def get_user_activities(self, user_id, activity_type=None, days=30, limit=100):
        """
        Get user's activities
        
        Args:
            user_id (str): User ID
            activity_type (str): Filter by type (optional)
            days (int): Number of days to look back
            limit (int): Maximum results
            
        Returns:
            list: User activities
        """
        query = {'user_id': user_id}
        
        # Filter by activity type if specified
        if activity_type:
            query['activity_type'] = activity_type
        
        # Filter by date range
        if days:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            query['timestamp'] = {'$gte': cutoff_date}
        
        activities = list(self.collection.find(query).sort('timestamp', -1).limit(limit))
        
        # Convert ObjectId to string
        for activity in activities:
            activity['_id'] = str(activity['_id'])
        
        return activities
    
    def get_search_history(self, user_id, days=30, limit=50):
        """
        Get user's search history
        
        Args:
            user_id (str): User ID
            days (int): Days to look back
            limit (int): Maximum results
            
        Returns:
            list: Search activities
        """
        return self.get_user_activities(user_id, 'search', days, limit)
    
    def get_activity_stats(self, user_id, days=30):
        """
        Get activity statistics for a user
        
        Args:
            user_id (str): User ID
            days (int): Days to look back
            
        Returns:
            dict: Activity statistics
        """
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
                    '_id': '$activity_type',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        # Convert to dict
        stats = {item['_id']: item['count'] for item in results}
        
        return {
            'total_searches': stats.get('search', 0),
            'total_service_views': stats.get('service_view', 0),
            'total_product_views': stats.get('product_view', 0),
            'total_ad_impressions': stats.get('ad_impression', 0),
            'total_ad_clicks': stats.get('ad_click', 0),
            'period_days': days
        }
    
    def get_popular_searches(self, days=7, limit=10):
        """
        Get most popular searches across all users
        
        Args:
            days (int): Days to look back
            limit (int): Number of results
            
        Returns:
            list: Popular search queries
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'activity_type': 'search',
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': '$query',
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}},
            {'$limit': limit}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        return [
            {'query': item['_id'], 'count': item['count']}
            for item in results
        ]
    
    def get_category_breakdown(self, user_id, days=30):
        """
        Get breakdown of user activity by category
        
        Args:
            user_id (str): User ID
            days (int): Days to look back
            
        Returns:
            dict: Category engagement
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'timestamp': {'$gte': cutoff_date},
                    'category': {'$exists': True}
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
        
        results = list(self.collection.aggregate(pipeline))
        
        return {item['_id']: item['count'] for item in results}
    
    def delete_old_activities(self, days=90):
        """
        Delete activities older than specified days (data cleanup)
        
        Args:
            days (int): Keep activities from last N days
            
        Returns:
            int: Number of deleted activities
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        result = self.collection.delete_many({
            'timestamp': {'$lt': cutoff_date}
        })
        
        return result.deleted_count