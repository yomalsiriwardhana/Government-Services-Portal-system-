from datetime import datetime
from bson import ObjectId

class Product:
    """Product/Ad model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db.products
    
    def create(self, product_data):
        """Create a new product/ad"""
        product_data['created_at'] = datetime.utcnow()
        product_data['updated_at'] = datetime.utcnow()
        product_data['view_count'] = 0
        product_data['click_count'] = 0
        product_data['status'] = product_data.get('status', 'active')
        product_data['featured'] = product_data.get('featured', False)
        
        result = self.collection.insert_one(product_data)
        return str(result.inserted_id)
    
    def find_by_id(self, product_id):
        """Find product by ID"""
        return self.collection.find_one({'_id': ObjectId(product_id)})
    
    def find_all(self, status='active'):
        """Find all products"""
        query = {'status': status} if status else {}
        products = list(self.collection.find(query))
        for product in products:
            product['_id'] = str(product['_id'])
        return products
    
    def find_by_category(self, category, status='active'):
        """Find products by category"""
        query = {'category': category}
        if status:
            query['status'] = status
        
        products = list(self.collection.find(query))
        for product in products:
            product['_id'] = str(product['_id'])
        return products
    
    def update(self, product_id, update_data):
        """Update product data"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete(self, product_id):
        """Delete a product (soft delete - set status to inactive)"""
        result = self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {
                '$set': {
                    'status': 'inactive',
                    'updated_at': datetime.utcnow()
                }
            }
        )
        return result.modified_count > 0
    
    def increment_view_count(self, product_id):
        """Increment product view count"""
        self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$inc': {'view_count': 1}}
        )
    
    def increment_click_count(self, product_id):
        """Increment product click count"""
        self.collection.update_one(
            {'_id': ObjectId(product_id)},
            {'$inc': {'click_count': 1}}
        )
    
    def get_personalized_ads(self, user_categories, user_age=None, user_location=None, limit=5):
        """Get personalized ads based on user profile"""
        query = {'status': 'active'}
        
        # Find products that match user's AI categories
        if user_categories:
            query['target_categories'] = {'$in': user_categories}
        
        # Age filtering
        if user_age:
            query['$or'] = [
                {'target_age_min': {'$exists': False}},
                {
                    '$and': [
                        {'target_age_min': {'$lte': user_age}},
                        {'target_age_max': {'$gte': user_age}}
                    ]
                }
            ]
        
        # Location filtering
        if user_location:
            query['$or'] = [
                {'target_locations': {'$exists': False}},
                {'target_locations': {'$in': [user_location, 'All']}},
                {'target_locations': {'$size': 0}}
            ]
        
        # Prioritize featured products
        products = list(
            self.collection.find(query)
            .sort([('featured', -1), ('created_at', -1)])
            .limit(limit)
        )
        
        for product in products:
            product['_id'] = str(product['_id'])
            
            # Calculate relevance score
            relevance_score = self._calculate_relevance_score(
                product, user_categories, user_age, user_location
            )
            product['relevance_score'] = relevance_score
        
        # Sort by relevance score
        products.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return products
    
    def _calculate_relevance_score(self, product, user_categories, user_age, user_location):
        """Calculate relevance score for a product"""
        score = 0
        
        # Category match (20 points per matching category)
        if user_categories and 'target_categories' in product:
            matching_categories = set(user_categories) & set(product['target_categories'])
            score += len(matching_categories) * 20
        
        # Age match (5 points)
        if user_age and 'target_age_min' in product and 'target_age_max' in product:
            if product['target_age_min'] <= user_age <= product['target_age_max']:
                score += 5
        
        # Location match (10 points)
        if user_location and 'target_locations' in product:
            if user_location in product['target_locations'] or 'All' in product['target_locations']:
                score += 10
        
        # Featured bonus (15 points)
        if product.get('featured', False):
            score += 15
        
        # Click-through rate bonus (up to 10 points)
        if product.get('view_count', 0) > 0:
            ctr = (product.get('click_count', 0) / product['view_count']) * 100
            score += min(ctr, 10)
        
        return score
    
    def get_top_performing_ads(self, limit=10):
        """Get top performing ads by CTR"""
        products = list(self.collection.find({'status': 'active'}))
        
        # Calculate CTR for each product
        for product in products:
            views = product.get('view_count', 0)
            clicks = product.get('click_count', 0)
            product['ctr'] = (clicks / views * 100) if views > 0 else 0
            product['_id'] = str(product['_id'])
        
        # Sort by CTR
        products.sort(key=lambda x: x['ctr'], reverse=True)
        
        return products[:limit]
    
    def get_category_performance(self):
        """Get performance metrics by category"""
        pipeline = [
            {
                '$match': {'status': 'active'}
            },
            {
                '$group': {
                    '_id': '$category',
                    'total_ads': {'$sum': 1},
                    'total_views': {'$sum': '$view_count'},
                    'total_clicks': {'$sum': '$click_count'}
                }
            },
            {
                '$project': {
                    'category': '$_id',
                    'total_ads': 1,
                    'total_views': 1,
                    'total_clicks': 1,
                    'ctr': {
                        '$cond': [
                            {'$eq': ['$total_views', 0]},
                            0,
                            {'$multiply': [{'$divide': ['$total_clicks', '$total_views']}, 100]}
                        ]
                    }
                }
            },
            {'$sort': {'ctr': -1}}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result