class AICategorizer:
    """AI-powered user categorization system"""
    
    def categorize_user(self, user_data):
        """
        Automatically categorize user based on profile data
        Returns a list of AI category tags
        """
        categories = []
        
        age = user_data.get('age', 0)
        job = user_data.get('job', '').lower()
        education = user_data.get('education', '').lower()
        interests = user_data.get('interests', [])
        marital_status = user_data.get('marital_status', '').lower()
        children = user_data.get('children', [])
        experience_years = user_data.get('experience_years', 0)
        
        # Demographic Categories (Age-based)
        if 18 <= age <= 24:
            categories.append('young_adult')
        elif 25 <= age <= 35:
            categories.append('early_career')
        elif 36 <= age <= 45:
            categories.append('mid_career_family')
        elif 46 <= age <= 60:
            categories.append('established_professional')
        elif age > 60:
            categories.append('senior')
        
        # Professional Categories (Job-based)
        if 'student' in job or 'o/l' in education or 'a/l' in education:
            categories.append('student')
        
        if 'government' in job or 'officer' in job or 'clerk' in job:
            categories.append('government_employee')
        
        if 'teacher' in job or 'lecturer' in job or 'professor' in job:
            categories.append('education_professional')
        
        if any(tech_word in job for tech_word in ['software', 'developer', 'engineer', 'programmer', 'it', 'tech', 'computer']):
            categories.append('tech_professional')
        
        if 'business' in job or 'entrepreneur' in job or 'owner' in job:
            categories.append('business_owner')
        
        if any(mgmt_word in job for mgmt_word in ['manager', 'director', 'ceo', 'cto', 'executive', 'head']):
            categories.append('management')
        
        # Behavioral Categories (Interest-based)
        interest_map = {
            'Education': ['education_seeker', 'course_buyer', 'book_buyer'],
            'Technology': ['tech_enthusiast', 'electronics_buyer'],
            'Business': ['business_owner', 'entrepreneur'],
            'Health': ['health_focused'],
            'Transport': ['vehicle_buyer'],
            'Housing': ['property_seeker'],
            'Employment': ['job_seeker'],
            'Immigration': ['travel_seeker']
        }
        
        for interest in interests:
            if interest in interest_map:
                categories.extend(interest_map[interest])
        
        # Family-based Categories
        if children and len(children) > 0:
            categories.append('parent')
            
            # Check children's ages for specific parent categories
            for child in children:
                child_age = child.get('age', 0)
                if child_age < 5:
                    categories.append('preschool_parent')
                elif 5 <= child_age <= 10:
                    categories.append('primary_school_parent')
                elif 11 <= child_age <= 15:
                    categories.append('secondary_school_parent')
                elif child_age > 15:
                    categories.append('teen_parent')
        
        # Experience-based Categories
        if experience_years > 10:
            categories.append('experienced_professional')
        elif experience_years > 5:
            categories.append('mid_level_professional')
        elif experience_years > 0:
            categories.append('entry_level_professional')
        
        # Education-based Categories
        if 'degree' in education or 'bachelor' in education or 'master' in education or 'phd' in education:
            categories.append('higher_educated')
        
        # Remove duplicates and return
        return list(set(categories))
    
    def update_categories_based_on_behavior(self, current_categories, behavior_data):
        """
        Update user categories based on behavioral data (searches, clicks, etc.)
        """
        new_categories = list(current_categories)
        
        # Extract behavioral insights
        search_patterns = behavior_data.get('search_patterns', {})
        interest_profile = behavior_data.get('interest_profile', {})
        ad_clicks = behavior_data.get('ad_clicks', [])
        
        # Add categories based on search frequency
        total_searches = search_patterns.get('total_searches', 0)
        if total_searches > 50:
            if 'power_user' not in new_categories:
                new_categories.append('power_user')
        elif total_searches > 20:
            if 'engaged_user' not in new_categories:
                new_categories.append('engaged_user')
        
        # Add categories based on interests shown through searches
        for category, percentage in interest_profile.items():
            if percentage > 30:  # Strong interest
                category_lower = category.lower()
                
                if 'education' in category_lower and 'education_seeker' not in new_categories:
                    new_categories.append('education_seeker')
                
                if 'technology' in category_lower and 'tech_enthusiast' not in new_categories:
                    new_categories.append('tech_enthusiast')
                
                if 'health' in category_lower and 'health_focused' not in new_categories:
                    new_categories.append('health_focused')
                
                if 'business' in category_lower and 'business_owner' not in new_categories:
                    new_categories.append('business_owner')
                
                if 'employment' in category_lower and 'job_seeker' not in new_categories:
                    new_categories.append('job_seeker')
                
                if 'transport' in category_lower and 'vehicle_buyer' not in new_categories:
                    new_categories.append('vehicle_buyer')
                
                if 'housing' in category_lower and 'property_seeker' not in new_categories:
                    new_categories.append('property_seeker')
                
                if 'immigration' in category_lower and 'travel_seeker' not in new_categories:
                    new_categories.append('travel_seeker')
        
        # Add categories based on ad clicks
        for click in ad_clicks:
            product_category = click.get('product_category', '').lower()
            
            if 'education' in product_category:
                if 'course_buyer' not in new_categories:
                    new_categories.append('course_buyer')
                if 'book_buyer' not in new_categories:
                    new_categories.append('book_buyer')
            
            if 'electronics' in product_category or 'laptop' in product_category or 'phone' in product_category:
                if 'electronics_buyer' not in new_categories:
                    new_categories.append('electronics_buyer')
            
            if 'vehicle' in product_category or 'car' in product_category:
                if 'vehicle_buyer' not in new_categories:
                    new_categories.append('vehicle_buyer')
            
            if 'property' in product_category or 'land' in product_category or 'house' in product_category:
                if 'property_seeker' not in new_categories:
                    new_categories.append('property_seeker')
            
            if 'course' in product_category:
                if 'course_buyer' not in new_categories:
                    new_categories.append('course_buyer')
        
        # Remove duplicates
        return list(set(new_categories))
    
    def get_category_description(self, category):
        """Get human-readable description for a category"""
        descriptions = {
            'young_adult': 'Young adult (18-24 years)',
            'early_career': 'Early career professional (25-35 years)',
            'mid_career_family': 'Mid-career with family (36-45 years)',
            'established_professional': 'Established professional (46-60 years)',
            'senior': 'Senior citizen (60+ years)',
            'student': 'Student',
            'government_employee': 'Government employee',
            'education_professional': 'Education professional',
            'tech_professional': 'Technology professional',
            'business_owner': 'Business owner',
            'management': 'Management position',
            'education_seeker': 'Interested in education',
            'course_buyer': 'Interested in courses',
            'book_buyer': 'Interested in books',
            'tech_enthusiast': 'Technology enthusiast',
            'electronics_buyer': 'Interested in electronics',
            'vehicle_buyer': 'Interested in vehicles',
            'property_seeker': 'Looking for property',
            'job_seeker': 'Looking for employment',
            'travel_seeker': 'Interested in travel/immigration',
            'health_focused': 'Health conscious',
            'parent': 'Parent',
            'preschool_parent': 'Parent of preschool child',
            'primary_school_parent': 'Parent of primary school child',
            'secondary_school_parent': 'Parent of secondary school child',
            'teen_parent': 'Parent of teenager',
            'power_user': 'Very active user',
            'engaged_user': 'Active user',
            'experienced_professional': 'Experienced professional (10+ years)',
            'mid_level_professional': 'Mid-level professional (5-10 years)',
            'entry_level_professional': 'Entry-level professional',
            'higher_educated': 'University educated'
        }
        
        return descriptions.get(category, category.replace('_', ' ').title())