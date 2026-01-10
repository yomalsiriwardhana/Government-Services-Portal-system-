class AdMatcher:
    """
    Advanced ad matching algorithm for personalized recommendations
    Scores ads based on multiple factors and returns best matches
    """
    
    def __init__(self, db):
        self.db = db
    
    def calculate_relevance_score(self, product, user_profile, user_interests):
        """
        Calculate relevance score for a product/ad
        Score is based on multiple weighted factors
        """
        score = 0
        
        # Extract user data
        user_categories = user_profile.get('ai_categories', [])
        user_age = user_profile.get('age')
        user_location = user_profile.get('location')
        user_job = user_profile.get('job', '').lower()
        user_education = user_profile.get('education', '').lower()
        
        # Extract product targeting
        target_categories = product.get('target_categories', [])
        target_age_min = product.get('target_age_min')
        target_age_max = product.get('target_age_max')
        target_locations = product.get('target_locations', [])
        product_category = product.get('category', '').lower()
        
        # 1. AI Category Match (0-40 points)
        # Most important factor - 20 points per matching category
        if user_categories and target_categories:
            matching_categories = set(user_categories) & set(target_categories)
            category_score = len(matching_categories) * 20
            score += min(category_score, 40)  # Cap at 40 points
        
        # 2. Interest Match (0-20 points)
        # Based on user's search interest profile
        if user_interests and product_category:
            for interest, percentage in user_interests.items():
                if interest.lower() in product_category or product_category in interest.lower():
                    # Higher interest percentage = higher score
                    interest_score = (percentage / 100) * 20
                    score += interest_score
                    break
        
        # 3. Age Match (0-10 points)
        if user_age and target_age_min is not None and target_age_max is not None:
            if target_age_min <= user_age <= target_age_max:
                score += 10
            else:
                # Partial score if close to age range
                age_diff = min(
                    abs(user_age - target_age_min),
                    abs(user_age - target_age_max)
                )
                if age_diff <= 5:
                    score += max(0, 10 - age_diff)
        
        # 4. Location Match (0-10 points)
        if user_location and target_locations:
            if user_location in target_locations or 'All' in target_locations or len(target_locations) == 0:
                score += 10
        
        # 5. Job Relevance (0-10 points)
        # Check if product is relevant to user's job
        job_keywords = {
            'education': ['book', 'course', 'study', 'exam', 'school'],
            'student': ['book', 'course', 'study', 'exam', 'laptop', 'computer'],
            'tech': ['laptop', 'computer', 'software', 'course', 'technology'],
            'business': ['business', 'registration', 'service', 'office'],
            'government': ['service', 'document', 'registration']
        }
        
        for job_type, keywords in job_keywords.items():
            if job_type in user_job:
                product_title = product.get('title', '').lower()
                product_desc = product.get('description', '').lower()
                
                for keyword in keywords:
                    if keyword in product_title or keyword in product_desc:
                        score += 5
                        break
        
        # 6. Featured Bonus (0-15 points)
        if product.get('featured', False):
            score += 15
        
        # 7. Click-Through Rate Performance (0-10 points)
        # Products with good historical performance get bonus
        views = product.get('view_count', 0)
        clicks = product.get('click_count', 0)
        if views > 0:
            ctr = (clicks / views) * 100
            ctr_score = min(ctr, 10)  # Cap at 10 points
            score += ctr_score
        
        # 8. Recency Bonus (0-5 points)
        # Newer products get slight boost
        from datetime import datetime, timedelta
        created_at = product.get('created_at')
        if created_at:
            age_days = (datetime.utcnow() - created_at).days
            if age_days < 7:
                score += 5
            elif age_days < 30:
                score += 3
        
        return round(score, 2)
    
    def get_personalized_ads(self, user_profile, user_interests, limit=5):
        """
        Get personalized ads for a user
        Returns ads sorted by relevance score
        """
        # Get all active products
        products = list(self.db.products.find({'status': 'active'}))
        
        # Calculate relevance score for each product
        scored_products = []
        for product in products:
            score = self.calculate_relevance_score(product, user_profile, user_interests)
            
            if score > 0:  # Only include products with some relevance
                product['_id'] = str(product['_id'])
                product['relevance_score'] = score
                scored_products.append(product)
        
        # Sort by relevance score (highest first)
        scored_products.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Return top N products
        return scored_products[:limit]
    
    def explain_score(self, product, user_profile, user_interests):
        """
        Explain why a product was recommended
        Useful for transparency and debugging
        """
        explanation = {
            'product': {
                'id': str(product.get('_id', '')),
                'title': product.get('title', ''),
                'category': product.get('category', '')
            },
            'total_score': 0,
            'breakdown': {}
        }
        
        score = 0
        user_categories = user_profile.get('ai_categories', [])
        target_categories = product.get('target_categories', [])
        
        # Category match
        if user_categories and target_categories:
            matching_categories = set(user_categories) & set(target_categories)
            category_score = len(matching_categories) * 20
            category_score = min(category_score, 40)
            score += category_score
            explanation['breakdown']['category_match'] = {
                'score': category_score,
                'matched_categories': list(matching_categories)
            }
        
        # Interest match
        product_category = product.get('category', '').lower()
        if user_interests and product_category:
            for interest, percentage in user_interests.items():
                if interest.lower() in product_category:
                    interest_score = (percentage / 100) * 20
                    score += interest_score
                    explanation['breakdown']['interest_match'] = {
                        'score': round(interest_score, 2),
                        'interest': interest,
                        'percentage': percentage
                    }
                    break
        
        # Age match
        user_age = user_profile.get('age')
        target_age_min = product.get('target_age_min')
        target_age_max = product.get('target_age_max')
        if user_age and target_age_min is not None and target_age_max is not None:
            if target_age_min <= user_age <= target_age_max:
                score += 10
                explanation['breakdown']['age_match'] = {
                    'score': 10,
                    'user_age': user_age,
                    'target_range': f"{target_age_min}-{target_age_max}"
                }
        
        # Featured bonus
        if product.get('featured', False):
            score += 15
            explanation['breakdown']['featured_bonus'] = {'score': 15}
        
        # CTR performance
        views = product.get('view_count', 0)
        clicks = product.get('click_count', 0)
        if views > 0:
            ctr = (clicks / views) * 100
            ctr_score = min(ctr, 10)
            score += ctr_score
            explanation['breakdown']['ctr_performance'] = {
                'score': round(ctr_score, 2),
                'ctr': round(ctr, 2),
                'views': views,
                'clicks': clicks
            }
        
        explanation['total_score'] = round(score, 2)
        
        return explanation
    
    def get_similar_products(self, product_id, limit=5):
        """
        Get products similar to a given product
        Based on category, price range, and target audience
        """
        product = self.db.products.find_one({'_id': product_id})
        if not product:
            return []
        
        category = product.get('category')
        price = product.get('price', 0)
        price_range = (price * 0.7, price * 1.3)  # ±30% price range
        
        # Find similar products
        similar = list(self.db.products.find({
            '_id': {'$ne': product_id},
            'status': 'active',
            'category': category,
            'price': {'$gte': price_range[0], '$lte': price_range[1]}
        }).limit(limit))
        
        for prod in similar:
            prod['_id'] = str(prod['_id'])
        
        return similar
    
    def get_trending_products(self, days=7, limit=10):
        """
        Get trending products based on recent engagement
        """
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get products with most clicks in recent period
        pipeline = [
            {
                '$match': {
                    'status': 'active',
                    'updated_at': {'$gte': cutoff_date}
                }
            },
            {
                '$project': {
                    'title': 1,
                    'category': 1,
                    'price': 1,
                    'click_count': 1,
                    'view_count': 1,
                    'ctr': {
                        '$cond': [
                            {'$eq': ['$view_count', 0]},
                            0,
                            {'$multiply': [{'$divide': ['$click_count', '$view_count']}, 100]}
                        ]
                    }
                }
            },
            {
                '$sort': {'click_count': -1, 'ctr': -1}
            },
            {
                '$limit': limit
            }
        ]
        
        trending = list(self.db.products.aggregate(pipeline))
        
        for prod in trending:
            prod['_id'] = str(prod['_id'])
        
        return trending