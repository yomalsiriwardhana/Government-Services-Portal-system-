from datetime import datetime, timedelta
from bson import ObjectId

class AdClick:
    """
    Ad Click model for tracking advertisement clicks and conversions
    """
    
    def __init__(self, db):
        """Initialize with MongoDB database connection"""
        self.collection = db.ad_clicks
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        try:
            self.collection.create_index([('user_id', 1), ('timestamp', -1)])
            self.collection.create_index([('ad_id', 1), ('timestamp', -1)])
            self.collection.create_index([('timestamp', -1)])
            print("✓ AdClick indexes created")
        except Exception as e:
            print(f"Index creation note: {e}")
    
    def record_click(self, user_id, ad_id, ad_data):
        """
        Record an ad click
        
        Args:
            user_id (str): User ID who clicked
            ad_id (str): Advertisement ID
            ad_data (dict): Ad information (title, category, cost)
            
        Returns:
            str: Click record ID
        """
        click_data = {
            'user_id': user_id,
            'ad_id': ad_id,
            'ad_title': ad_data.get('title', 'Unknown'),
            'ad_category': ad_data.get('category', 'Unknown'),
            'cost': ad_data.get('bid_amount', 0),
            'timestamp': datetime.utcnow(),
            'converted': False  # Will be updated if user takes action
        }
        
        result = self.collection.insert_one(click_data)
        return str(result.inserted_id)
    
    def mark_conversion(self, click_id):
        """
        Mark a click as converted (user took desired action)
        
        Args:
            click_id (str): Click record ID
            
        Returns:
            bool: Success status
        """
        result = self.collection.update_one(
            {'_id': ObjectId(click_id)},
            {
                '$set': {
                    'converted': True,
                    'conversion_time': datetime.utcnow()
                }
            }
        )
        
        return result.modified_count > 0
    
    def get_user_clicks(self, user_id, days=30):
        """
        Get all clicks by a user
        
        Args:
            user_id (str): User ID
            days (int): Days to look back
            
        Returns:
            list: Click records
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        clicks = list(self.collection.find({
            'user_id': user_id,
            'timestamp': {'$gte': cutoff_date}
        }).sort('timestamp', -1))
        
        for click in clicks:
            click['_id'] = str(click['_id'])
        
        return clicks
    
    def get_ad_clicks(self, ad_id, days=30):
        """
        Get all clicks for an advertisement
        
        Args:
            ad_id (str): Advertisement ID
            days (int): Days to look back
            
        Returns:
            list: Click records
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        clicks = list(self.collection.find({
            'ad_id': ad_id,
            'timestamp': {'$gte': cutoff_date}
        }).sort('timestamp', -1))
        
        for click in clicks:
            click['_id'] = str(click['_id'])
        
        return clicks
    
    def get_click_stats(self, ad_id, days=30):
        """
        Get click statistics for an advertisement
        
        Args:
            ad_id (str): Advertisement ID
            days (int): Days to look back
            
        Returns:
            dict: Click statistics
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'ad_id': ad_id,
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': None,
                    'total_clicks': {'$sum': 1},
                    'total_cost': {'$sum': '$cost'},
                    'conversions': {
                        '$sum': {'$cond': ['$converted', 1, 0]}
                    }
                }
            }
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        if results:
            stats = results[0]
            conversion_rate = (stats['conversions'] / stats['total_clicks'] * 100) if stats['total_clicks'] > 0 else 0
            
            return {
                'total_clicks': stats['total_clicks'],
                'total_cost': stats['total_cost'],
                'conversions': stats['conversions'],
                'conversion_rate': round(conversion_rate, 2),
                'avg_cost_per_click': stats['total_cost'] / stats['total_clicks'] if stats['total_clicks'] > 0 else 0
            }
        
        return {
            'total_clicks': 0,
            'total_cost': 0,
            'conversions': 0,
            'conversion_rate': 0,
            'avg_cost_per_click': 0
        }
    
    def get_user_click_stats(self, user_id, days=30):
        """
        Get click statistics for a user
        
        Args:
            user_id (str): User ID
            days (int): Days to look back
            
        Returns:
            dict: User click statistics
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
                    '_id': '$ad_category',
                    'click_count': {'$sum': 1}
                }
            },
            {'$sort': {'click_count': -1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        category_clicks = {item['_id']: item['click_count'] for item in results}
        
        return {
            'total_ad_clicks': sum(category_clicks.values()),
            'category_breakdown': category_clicks,
            'most_clicked_category': results[0]['_id'] if results else None
        }
    
    def get_daily_clicks(self, days=7):
        """
        Get daily click counts (for charts)
        
        Args:
            days (int): Number of days
            
        Returns:
            list: Daily click data
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {
                '$match': {
                    'timestamp': {'$gte': cutoff_date}
                }
            },
            {
                '$group': {
                    '_id': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$timestamp'
                        }
                    },
                    'clicks': {'$sum': 1},
                    'cost': {'$sum': '$cost'}
                }
            },
            {'$sort': {'_id': 1}}
        ]
        
        results = list(self.collection.aggregate(pipeline))
        
        return [
            {
                'date': item['_id'],
                'clicks': item['clicks'],
                'cost': item['cost']
            }
            for item in results
        ]