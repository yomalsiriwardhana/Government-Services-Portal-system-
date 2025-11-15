"""
Ad Matching Engine - MongoDB Version
Matches products/ads to users based on AI categories and search patterns
"""

from datetime import datetime, timedelta
from bson import ObjectId
import random

class AdMatcher:
    def __init__(self, db):
        """
        Initialize ad matcher with MongoDB database
        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.products_col = db["products"]
        self.ads_col = db["ads"]
        self.ad_clicks_col = db["ad_clicks"]
        self.ad_views_col = db["ad_views"]
        self.users_col = db["users"]
        self.search_patterns_col = db["user_search_patterns"]
        
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes for ad collections"""
        try:
            # Index on product categories and status
            self.products_col.create_index([("category", 1), ("status", 1)])
            self.products_col.create_index("target_categories")
            
            # Index on ad clicks
            self.ad_clicks_col.create_index([("user_id", 1), ("timestamp", -1)])
            self.ad_clicks_col.create_index("product_id")
            
            # Index on ad views
            self.ad_views_col.create_index([("user_id", 1), ("timestamp", -1)])
            
            print("✅ Ad matcher indexes created")
        except Exception as e:
            print(f"⚠️ Ad index creation warning: {e}")
    
    def get_personalized_ads(self, user_id, limit=5, position='sidebar'):
        """
        Get personalized ads for a user based on their profile and behavior
        
        Args:
            user_id: User's ID
            limit: Number of ads to return
            position: Ad position (sidebar, banner, etc.)
        
        Returns:
            List of matched ads with relevance scores
        """
        try:
            # Get user data
            user = self.users_col.find_one({"_id": ObjectId(user_id)})
            if not user:
                return self._get_default_ads(limit)
            
            # Get user's AI categories
            ai_categories_data = user.get("ai_categories", {})
            if isinstance(ai_categories_data, dict):
                user_categories = set(ai_categories_data.get("categories", []))
            elif isinstance(ai_categories_data, list):
                user_categories = set(ai_categories_data)
            else:
                user_categories = set()
            
            # Get user's search patterns
            search_patterns = self.search_patterns_col.find_one({"user_id": user_id})
            interest_scores = {}
            if search_patterns:
                interest_scores = search_patterns.get("interest_scores", {})
            
            # Get user's age and location for additional targeting
            user_age = user.get("age")
            user_location = user.get("location")
            
            # Get all active products/ads
            active_products = list(self.products_col.find({
                "status": "approved",
                "$or": [
                    {"stock": {"$gt": 0}},
                    {"stock": {"$exists": False}}
                ]
            }))
            
            # Score each product
            scored_products = []
            for product in active_products:
                score = self._calculate_relevance_score(
                    product=product,
                    user_categories=user_categories,
                    interest_scores=interest_scores,
                    user_age=user_age,
                    user_location=user_location,
                    user_id=user_id
                )
                
                if score > 0:
                    product['relevance_score'] = score
                    scored_products.append(product)
            
            # Sort by relevance score
            scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Get top ads
            top_ads = scored_products[:limit]
            
            # Track ad views
            self._track_ad_views(user_id, [str(ad['_id']) for ad in top_ads])
            
            # Format ads for frontend
            formatted_ads = []
            for ad in top_ads:
                formatted_ads.append({
                    'product_id': str(ad['_id']),
                    'title': ad.get('title'),
                    'description': ad.get('description'),
                    'price': ad.get('price'),
                    'category': ad.get('category'),
                    'image_url': ad.get('image_url', '/static/placeholder.jpg'),
                    'relevance_score': ad['relevance_score'],
                    'link': f"/product/{ad['_id']}"
                })
            
            return formatted_ads
            
        except Exception as e:
            print(f"Error getting personalized ads: {e}")
            import traceback
            traceback.print_exc()
            return self._get_default_ads(limit)
    
    def _calculate_relevance_score(self, product, user_categories, interest_scores, 
                                   user_age, user_location, user_id):
        """Calculate how relevant a product is to a user"""
        score = 0
        
        # 1. Category matching (highest weight)
        product_targets = set(product.get('target_categories', []))
        category_matches = len(user_categories & product_targets)
        score += category_matches * 10  # 10 points per matching category
        
        # 2. Interest matching based on search patterns
        product_category = product.get('category', '').lower()
        
        # Map product categories to interest areas
        category_interest_map = {
            'books': 'education',
            'past_papers': 'education',
            'study_guides': 'education',
            'courses': 'education',
            'electronics': 'technology',
            'computers': 'technology',
            'phones': 'technology',
            'vehicles': 'transport',
            'cars': 'transport',
            'bikes': 'transport',
            'property': 'property',
            'land': 'property',
            'houses': 'property'
        }
        
        related_interest = category_interest_map.get(product_category)
        if related_interest and interest_scores.get(related_interest, 0) > 0:
            score += interest_scores[related_interest] * 2  # 2 points per search
        
        # 3. Age-based relevance
        if user_age and 'age_range' in product:
            age_range = product['age_range']
            if isinstance(age_range, dict):
                min_age = age_range.get('min', 0)
                max_age = age_range.get('max', 100)
                if min_age <= user_age <= max_age:
                    score += 5
        
        # 4. Location-based relevance
        if user_location and 'target_locations' in product:
            target_locations = product.get('target_locations', [])
            if user_location in target_locations or 'all' in target_locations:
                score += 3
        
        # 5. Recency boost (newer products get slight boost)
        created_at = product.get('created_at')
        if created_at:
            days_old = (datetime.utcnow() - created_at).days
            if days_old < 7:
                score += 5  # New product boost
            elif days_old < 30:
                score += 2
        
        # 6. Click-through rate boost (popular products)
        product_id = str(product['_id'])
        clicks = self.ad_clicks_col.count_documents({"product_id": product_id})
        views = self.ad_views_col.count_documents({"product_id": product_id})
        
        if views > 10:  # Only consider if enough data
            ctr = clicks / views if views > 0 else 0
            score += int(ctr * 10)  # Up to 10 points for high CTR
        
        # 7. Avoid recently shown ads (diversity)
        recent_views = self.ad_views_col.count_documents({
            "user_id": user_id,
            "product_id": product_id,
            "timestamp": {"$gte": datetime.utcnow() - timedelta(hours=24)}
        })
        
        if recent_views > 0:
            score -= recent_views * 5  # Penalty for repetition
        
        return max(score, 0)  # Ensure non-negative
    
    def _get_default_ads(self, limit=5):
        """Get default ads when personalization not available"""
        try:
            # Get top performing products
            pipeline = [
                {"$match": {"status": "approved"}},
                {"$lookup": {
                    "from": "ad_clicks",
                    "localField": "_id",
                    "foreignField": "product_id",
                    "as": "clicks"
                }},
                {"$addFields": {"click_count": {"$size": "$clicks"}}},
                {"$sort": {"click_count": -1}},
                {"$limit": limit * 2}  # Get more to randomize
            ]
            
            products = list(self.products_col.aggregate(pipeline))
            
            # Randomize a bit
            random.shuffle(products)
            products = products[:limit]
            
            formatted_ads = []
            for product in products:
                formatted_ads.append({
                    'product_id': str(product['_id']),
                    'title': product.get('title'),
                    'description': product.get('description'),
                    'price': product.get('price'),
                    'category': product.get('category'),
                    'image_url': product.get('image_url', '/static/placeholder.jpg'),
                    'relevance_score': 0,
                    'link': f"/product/{product['_id']}"
                })
            
            return formatted_ads
            
        except Exception as e:
            print(f"Error getting default ads: {e}")
            return []
    
    def track_ad_click(self, user_id, product_id, source='sidebar'):
        """Track when user clicks on an ad"""
        try:
            click_doc = {
                "user_id": user_id,
                "product_id": product_id,
                "source": source,
                "timestamp": datetime.utcnow()
            }
            
            self.ad_clicks_col.insert_one(click_doc)
            
            # Update product click count
            self.products_col.update_one(
                {"_id": ObjectId(product_id)},
                {"$inc": {"clicks": 1}}
            )
            
            print(f"👆 Ad click tracked: Product {product_id} by user {user_id}")
            return True
            
        except Exception as e:
            print(f"Error tracking ad click: {e}")
            return False
    
    def _track_ad_views(self, user_id, product_ids):
        """Track when ads are viewed by user"""
        try:
            view_docs = []
            timestamp = datetime.utcnow()
            
            for product_id in product_ids:
                view_docs.append({
                    "user_id": user_id,
                    "product_id": product_id,
                    "timestamp": timestamp
                })
            
            if view_docs:
                self.ad_views_col.insert_many(view_docs)
                
                # Update product view counts
                for product_id in product_ids:
                    self.products_col.update_one(
                        {"_id": ObjectId(product_id)},
                        {"$inc": {"views": 1}}
                    )
            
        except Exception as e:
            print(f"Error tracking ad views: {e}")
    
    def get_ad_performance(self, product_id):
        """Get performance metrics for a specific ad/product"""
        try:
            product_id_str = str(product_id)
            
            # Get click and view counts
            clicks = self.ad_clicks_col.count_documents({"product_id": product_id_str})
            views = self.ad_views_col.count_documents({"product_id": product_id_str})
            
            # Calculate CTR
            ctr = (clicks / views * 100) if views > 0 else 0
            
            # Get unique users who clicked
            unique_clickers = len(self.ad_clicks_col.distinct("user_id", {"product_id": product_id_str}))
            
            # Get click timestamps for trend analysis
            recent_clicks = self.ad_clicks_col.count_documents({
                "product_id": product_id_str,
                "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
            })
            
            return {
                "product_id": product_id_str,
                "total_views": views,
                "total_clicks": clicks,
                "unique_clickers": unique_clickers,
                "ctr": round(ctr, 2),
                "recent_clicks_7d": recent_clicks
            }
            
        except Exception as e:
            print(f"Error getting ad performance: {e}")
            return None
    
    def get_top_performing_ads(self, limit=10):
        """Get top performing ads by CTR"""
        try:
            pipeline = [
                {"$match": {"status": "approved"}},
                {"$lookup": {
                    "from": "ad_clicks",
                    "localField": "_id",
                    "foreignField": "product_id",
                    "as": "clicks"
                }},
                {"$lookup": {
                    "from": "ad_views",
                    "localField": "_id",
                    "foreignField": "product_id",
                    "as": "views"
                }},
                {"$addFields": {
                    "click_count": {"$size": "$clicks"},
                    "view_count": {"$size": "$views"},
                    "ctr": {
                        "$cond": [
                            {"$gt": [{"$size": "$views"}, 0]},
                            {"$multiply": [
                                {"$divide": [{"$size": "$clicks"}, {"$size": "$views"}]},
                                100
                            ]},
                            0
                        ]
                    }
                }},
                {"$match": {"view_count": {"$gte": 10}}},  # Only products with enough data
                {"$sort": {"ctr": -1}},
                {"$limit": limit}
            ]
            
            top_ads = list(self.products_col.aggregate(pipeline))
            
            result = []
            for ad in top_ads:
                result.append({
                    "product_id": str(ad['_id']),
                    "title": ad.get('title'),
                    "category": ad.get('category'),
                    "views": ad['view_count'],
                    "clicks": ad['click_count'],
                    "ctr": round(ad['ctr'], 2)
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting top performing ads: {e}")
            return []