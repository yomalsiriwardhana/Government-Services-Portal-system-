from datetime import datetime
from bson import ObjectId

class Advertisement:
    """
    Advertisement model for storing and managing advertisements in MongoDB
    Tracks ad performance, targeting criteria, and user interactions
    """
    
    def __init__(self, db):
        """Initialize with MongoDB database connection"""
        self.collection = db.advertisements
        # Create indexes for better query performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for efficient queries"""
        try:
            # Index for active ads
            self.collection.create_index([('is_active', 1)])
            # Index for category searches
            self.collection.create_index([('category', 1)])
            # Index for targeting queries
            self.collection.create_index([('target_age_min', 1), ('target_age_max', 1)])
            print("✓ Advertisement indexes created")
        except Exception as e:
            print(f"Index creation note: {e}")
    
    def create(self, ad_data):
        """
        Create a new advertisement
        
        Args:
            ad_data (dict): Advertisement information including:
                - title: Ad title
                - description: Ad description
                - image_url: Image URL for the ad
                - link_url: Where users go when they click
                - category: Ad category (Education, Technology, etc.)
                - target_age_min: Minimum target age
                - target_age_max: Maximum target age
                - target_locations: List of target locations
                - target_jobs: List of target job titles
                - target_categories: AI categories to target
                - budget: Ad budget
                - bid_amount: Cost per click
                
        Returns:
            str: ID of created advertisement
        """
        # Add timestamps
        ad_data['created_at'] = datetime.utcnow()
        ad_data['updated_at'] = datetime.utcnow()
        
        # Initialize performance metrics
        ad_data['impressions'] = 0  # How many times shown
        ad_data['clicks'] = 0  # How many times clicked
        ad_data['ctr'] = 0.0  # Click-through rate (clicks/impressions * 100)
        ad_data['total_spent'] = 0.0  # Total money spent
        ad_data['is_active'] = ad_data.get('is_active', True)
        
        # Insert into database
        result = self.collection.insert_one(ad_data)
        return str(result.inserted_id)
    
    def find_by_id(self, ad_id):
        """
        Find advertisement by ID
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            dict: Advertisement data or None
        """
        return self.collection.find_one({'_id': ObjectId(ad_id)})
    
    def get_all_active(self, limit=50):
        """
        Get all active advertisements
        
        Args:
            limit (int): Maximum number of ads to return
            
        Returns:
            list: List of active advertisements
        """
        ads = list(self.collection.find(
            {'is_active': True}
        ).limit(limit))
        
        # Convert ObjectId to string for JSON serialization
        for ad in ads:
            ad['_id'] = str(ad['_id'])
        
        return ads
    
    def get_by_category(self, category):
        """
        Get advertisements by category
        
        Args:
            category (str): Category name
            
        Returns:
            list: List of advertisements in that category
        """
        ads = list(self.collection.find({
            'category': category,
            'is_active': True
        }))
        
        for ad in ads:
            ad['_id'] = str(ad['_id'])
        
        return ads
    
    def record_impression(self, ad_id):
        """
        Record that an ad was shown to a user (impression)
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            bool: Success status
        """
        result = self.collection.update_one(
            {'_id': ObjectId(ad_id)},
            {
                '$inc': {'impressions': 1},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        # Recalculate CTR after impression
        self._update_ctr(ad_id)
        
        return result.modified_count > 0
    
    def record_click(self, ad_id, cost=None):
        """
        Record that a user clicked on an ad
        
        Args:
            ad_id (str): Advertisement ID
            cost (float): Cost of this click (bid amount)
            
        Returns:
            bool: Success status
        """
        update_data = {
            '$inc': {'clicks': 1},
            '$set': {'updated_at': datetime.utcnow()}
        }
        
        # Add to total spent if cost provided
        if cost is not None:
            update_data['$inc']['total_spent'] = cost
        
        result = self.collection.update_one(
            {'_id': ObjectId(ad_id)},
            update_data
        )
        
        # Recalculate CTR after click
        self._update_ctr(ad_id)
        
        return result.modified_count > 0
    
    def _update_ctr(self, ad_id):
        """
        Update Click-Through Rate (CTR) for an advertisement
        CTR = (clicks / impressions) * 100
        
        Args:
            ad_id (str): Advertisement ID
        """
        ad = self.collection.find_one({'_id': ObjectId(ad_id)})
        if ad and ad['impressions'] > 0:
            ctr = (ad['clicks'] / ad['impressions']) * 100
            self.collection.update_one(
                {'_id': ObjectId(ad_id)},
                {'$set': {'ctr': round(ctr, 2)}}
            )
    
    def update(self, ad_id, update_data):
        """
        Update advertisement data
        
        Args:
            ad_id (str): Advertisement ID
            update_data (dict): Fields to update
            
        Returns:
            bool: Success status
        """
        update_data['updated_at'] = datetime.utcnow()
        
        result = self.collection.update_one(
            {'_id': ObjectId(ad_id)},
            {'$set': update_data}
        )
        
        return result.modified_count > 0
    
    def deactivate(self, ad_id):
        """
        Deactivate an advertisement (stop showing it)
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            bool: Success status
        """
        return self.update(ad_id, {'is_active': False})
    
    def activate(self, ad_id):
        """
        Activate an advertisement (start showing it)
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            bool: Success status
        """
        return self.update(ad_id, {'is_active': True})
    
    def get_performance_stats(self, ad_id):
        """
        Get detailed performance statistics for an advertisement
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            dict: Performance statistics
        """
        ad = self.find_by_id(ad_id)
        if not ad:
            return None
        
        return {
            'ad_id': str(ad['_id']),
            'title': ad.get('title', 'Unknown'),
            'impressions': ad.get('impressions', 0),
            'clicks': ad.get('clicks', 0),
            'ctr': ad.get('ctr', 0.0),
            'total_spent': ad.get('total_spent', 0.0),
            'avg_cost_per_click': ad.get('total_spent', 0) / ad.get('clicks', 1),
            'is_active': ad.get('is_active', False)
        }
    
    def get_all_performance_stats(self):
        """
        Get performance statistics for all advertisements
        
        Returns:
            list: List of performance stats for each ad
        """
        ads = list(self.collection.find())
        stats = []
        
        for ad in ads:
            avg_cpc = ad.get('total_spent', 0) / ad.get('clicks', 1) if ad.get('clicks', 0) > 0 else 0
            
            stats.append({
                'ad_id': str(ad['_id']),
                'title': ad.get('title', 'Unknown'),
                'category': ad.get('category', 'Unknown'),
                'impressions': ad.get('impressions', 0),
                'clicks': ad.get('clicks', 0),
                'ctr': ad.get('ctr', 0.0),
                'total_spent': ad.get('total_spent', 0.0),
                'avg_cost_per_click': round(avg_cpc, 2),
                'is_active': ad.get('is_active', False),
                'created_at': ad.get('created_at')
            })
        
        # Sort by CTR (best performing first)
        stats.sort(key=lambda x: x['ctr'], reverse=True)
        
        return stats
    
    def get_top_performing(self, limit=10):
        """
        Get top performing advertisements by CTR
        
        Args:
            limit (int): Number of top ads to return
            
        Returns:
            list: Top performing advertisements
        """
        ads = list(self.collection.find(
            {'is_active': True, 'impressions': {'$gt': 10}}  # At least 10 impressions
        ).sort('ctr', -1).limit(limit))
        
        for ad in ads:
            ad['_id'] = str(ad['_id'])
        
        return ads
    
    def search_ads(self, filters):
        """
        Search advertisements with filters
        
        Args:
            filters (dict): Search filters (category, is_active, etc.)
            
        Returns:
            list: Matching advertisements
        """
        ads = list(self.collection.find(filters))
        
        for ad in ads:
            ad['_id'] = str(ad['_id'])
        
        return ads
    
    def delete(self, ad_id):
        """
        Delete an advertisement (use with caution)
        
        Args:
            ad_id (str): Advertisement ID
            
        Returns:
            bool: Success status
        """
        result = self.collection.delete_one({'_id': ObjectId(ad_id)})
        return result.deleted_count > 0
    
    def get_ads_by_targeting(self, user_profile):
        """
        Get advertisements that match user's profile
        Basic filtering before detailed scoring
        
        Args:
            user_profile (dict): User profile data
            
        Returns:
            list: Potentially relevant advertisements
        """
        query = {'is_active': True}
        
        # Age filtering
        if 'age' in user_profile:
            age = user_profile['age']
            query['$or'] = [
                {'target_age_min': {'$lte': age}, 'target_age_max': {'$gte': age}},
                {'target_age_min': None},  # No age targeting
                {'target_age_max': None}
            ]
        
        ads = list(self.collection.find(query))
        
        for ad in ads:
            ad['_id'] = str(ad['_id'])
        
        return ads
    
    def get_total_ad_spend(self):
        """
        Get total spending across all advertisements
        
        Returns:
            float: Total amount spent
        """
        pipeline = [
            {'$group': {'_id': None, 'total': {'$sum': '$total_spent'}}}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result[0]['total'] if result else 0.0
    
    def get_category_performance(self):
        """
        Get performance statistics grouped by category
        
        Returns:
            list: Category-wise performance data
        """
        pipeline = [
            {
                '$group': {
                    '_id': '$category',
                    'total_impressions': {'$sum': '$impressions'},
                    'total_clicks': {'$sum': '$clicks'},
                    'total_spent': {'$sum': '$total_spent'},
                    'ad_count': {'$sum': 1}
                }
            },
            {
                '$project': {
                    'category': '$_id',
                    'total_impressions': 1,
                    'total_clicks': 1,
                    'total_spent': 1,
                    'ad_count': 1,
                    'avg_ctr': {
                        '$cond': [
                            {'$gt': ['$total_impressions', 0]},
                            {'$multiply': [
                                {'$divide': ['$total_clicks', '$total_impressions']},
                                100
                            ]},
                            0
                        ]
                    }
                }
            },
            {'$sort': {'avg_ctr': -1}}
        ]
        
        return list(self.collection.aggregate(pipeline))