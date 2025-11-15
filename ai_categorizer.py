"""
AI Auto-Categorization Module
Automatically categorizes users on registration and re-analyzes based on search behavior
"""

from datetime import datetime
from bson import ObjectId


class AIUserCategorizer:
    """
    Intelligent user categorization system that automatically assigns
    categories based on user profile and behavior
    """
    
    def __init__(self, db):
        self.db = db
        self.users_col = db["users"]
        self.search_history_col = db["search_history"]
    
    def categorize_user_on_registration(self, user_data):
        """
        Automatically categorize user immediately after registration
        
        Args:
            user_data: Dictionary containing user registration data
            
        Returns:
            List of assigned categories
        """
        categories = []
        scores = {}
        
        # Extract user information
        age = user_data.get('age')
        job = user_data.get('job', '').lower() if user_data.get('job') else ''
        location = user_data.get('location', '').lower() if user_data.get('location') else ''
        interests = [i.lower() for i in user_data.get('interests', [])]
        
        # AGE-BASED CATEGORIZATION
        if age:
            if age < 25:
                categories.append("young_adult")
                scores["education_seeker"] = scores.get("education_seeker", 0) + 30
                scores["tech_enthusiast"] = scores.get("tech_enthusiast", 0) + 20
            elif 25 <= age <= 35:
                categories.append("early_career")
                scores["career_focused"] = scores.get("career_focused", 0) + 30
                scores["property_seeker"] = scores.get("property_seeker", 0) + 10
            elif 36 <= age <= 45:
                categories.append("mid_career_family")
                scores["family_oriented"] = scores.get("family_oriented", 0) + 30
                scores["property_seeker"] = scores.get("property_seeker", 0) + 20
                scores["vehicle_buyer"] = scores.get("vehicle_buyer", 0) + 20
            elif 46 <= age <= 60:
                categories.append("established_professional")
                scores["investment_focused"] = scores.get("investment_focused", 0) + 30
                scores["property_investor"] = scores.get("property_investor", 0) + 25
            else:
                categories.append("senior")
                scores["health_focused"] = scores.get("health_focused", 0) + 20
        
        # JOB-BASED CATEGORIZATION
        if job:
            if 'government' in job or 'officer' in job:
                categories.append("government_employee")
                scores["education_seeker"] = scores.get("education_seeker", 0) + 25
                scores["course_buyer"] = scores.get("course_buyer", 0) + 20
            
            if any(word in job for word in ['teacher', 'lecturer', 'professor']):
                categories.append("education_professional")
                scores["book_buyer"] = scores.get("book_buyer", 0) + 40
                scores["course_creator"] = scores.get("course_creator", 0) + 30
            
            if any(word in job for word in ['engineer', 'developer', 'it', 'tech']):
                categories.append("tech_professional")
                scores["tech_enthusiast"] = scores.get("tech_enthusiast", 0) + 40
                scores["electronics_buyer"] = scores.get("electronics_buyer", 0) + 35
            
            if any(word in job for word in ['manager', 'director', 'ceo', 'executive']):
                categories.append("management")
                scores["vehicle_buyer"] = scores.get("vehicle_buyer", 0) + 30
                scores["property_investor"] = scores.get("property_investor", 0) + 25
            
            if any(word in job for word in ['business', 'entrepreneur', 'owner']):
                categories.append("business_owner")
                scores["investment_focused"] = scores.get("investment_focused", 0) + 35
                scores["property_investor"] = scores.get("property_investor", 0) + 30
            
            if 'student' in job:
                categories.append("student")
                scores["education_seeker"] = scores.get("education_seeker", 0) + 50
                scores["book_buyer"] = scores.get("book_buyer", 0) + 45
                scores["past_paper_buyer"] = scores.get("past_paper_buyer", 0) + 40
        
        # INTEREST-BASED CATEGORIZATION
        for interest in interests:
            if interest in ['education', 'learning']:
                scores["education_seeker"] = scores.get("education_seeker", 0) + 35
                scores["course_buyer"] = scores.get("course_buyer", 0) + 30
                scores["book_buyer"] = scores.get("book_buyer", 0) + 25
            
            if interest in ['technology', 'tech', 'computers']:
                scores["tech_enthusiast"] = scores.get("tech_enthusiast", 0) + 35
                scores["electronics_buyer"] = scores.get("electronics_buyer", 0) + 30
            
            if interest in ['business', 'entrepreneurship']:
                scores["business_oriented"] = scores.get("business_oriented", 0) + 35
                scores["course_buyer"] = scores.get("course_buyer", 0) + 20
            
            if interest in ['health', 'fitness', 'wellness']:
                scores["health_focused"] = scores.get("health_focused", 0) + 35
            
            if interest in ['transport', 'vehicles', 'cars']:
                scores["vehicle_buyer"] = scores.get("vehicle_buyer", 0) + 40
            
            if interest in ['housing', 'property', 'real estate']:
                scores["property_seeker"] = scores.get("property_seeker", 0) + 40
            
            if interest in ['employment', 'jobs', 'career']:
                scores["career_focused"] = scores.get("career_focused", 0) + 35
                scores["course_buyer"] = scores.get("course_buyer", 0) + 25
        
        # LOCATION-BASED CATEGORIZATION
        urban_areas = ['colombo', 'kandy', 'gampaha', 'negombo', 'moratuwa']
        if location and any(city in location for city in urban_areas):
            categories.append("urban_resident")
            scores["tech_enthusiast"] = scores.get("tech_enthusiast", 0) + 10
            scores["electronics_buyer"] = scores.get("electronics_buyer", 0) + 10
        else:
            categories.append("rural_resident")
        
        # ADD TOP SCORING BEHAVIORAL CATEGORIES
        # Sort scores and add top 5 categories
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for category, score in sorted_scores[:5]:
            if score >= 20:  # Threshold
                categories.append(category)
        
        # Remove duplicates and return
        return {
            "categories": list(set(categories)),
            "category_scores": scores,
            "categorized_at": datetime.utcnow(),
            "categorization_type": "registration"
        }
    
    def recategorize_based_on_search(self, user_id):
        """
        Re-analyze and update user categories based on search behavior
        
        Args:
            user_id: User's ObjectId as string
            
        Returns:
            Updated categories
        """
        # Get user's current data
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None
        
        # Get search history (last 50 searches)
        searches = list(self.search_history_col.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(50))
        
        if not searches:
            # No search history, return current categories
            return user.get("ai_categories", {})
        
        # Analyze search patterns
        search_scores = {}
        
        for search in searches:
            query = search.get("query", "").lower()
            
            # Education-related searches
            if any(word in query for word in ['degree', 'course', 'education', 'study', 'learn', 'class', 'tuition']):
                search_scores["education_seeker"] = search_scores.get("education_seeker", 0) + 5
                search_scores["course_buyer"] = search_scores.get("course_buyer", 0) + 4
            
            # Books and papers
            if any(word in query for word in ['book', 'paper', 'past paper', 'guide', 'notes']):
                search_scores["book_buyer"] = search_scores.get("book_buyer", 0) + 5
                search_scores["past_paper_buyer"] = search_scores.get("past_paper_buyer", 0) + 5
            
            # Technology and electronics
            if any(word in query for word in ['laptop', 'phone', 'computer', 'gadget', 'tech', 'electronic']):
                search_scores["tech_enthusiast"] = search_scores.get("tech_enthusiast", 0) + 5
                search_scores["electronics_buyer"] = search_scores.get("electronics_buyer", 0) + 6
            
            # Vehicles
            if any(word in query for word in ['car', 'vehicle', 'bike', 'motorcycle', 'van', 'auto']):
                search_scores["vehicle_buyer"] = search_scores.get("vehicle_buyer", 0) + 6
            
            # Property
            if any(word in query for word in ['land', 'house', 'property', 'apartment', 'estate', 'plot']):
                search_scores["property_seeker"] = search_scores.get("property_seeker", 0) + 6
                search_scores["property_investor"] = search_scores.get("property_investor", 0) + 4
            
            # Career and jobs
            if any(word in query for word in ['job', 'career', 'employment', 'work', 'vacancy']):
                search_scores["career_focused"] = search_scores.get("career_focused", 0) + 5
            
            # News and information
            if any(word in query for word in ['news', 'newspaper', 'magazine', 'article']):
                search_scores["news_reader"] = search_scores.get("news_reader", 0) + 4
        
        # Get current categories
        current_categories = user.get("ai_categories", {})
        current_scores = current_categories.get("category_scores", {})
        
        # Merge scores (search behavior has higher weight for behavioral categories)
        for category, score in search_scores.items():
            current_scores[category] = current_scores.get(category, 0) + score
        
        # Rebuild category list
        new_categories = current_categories.get("categories", [])
        
        # Add new high-scoring categories
        for category, score in search_scores.items():
            if score >= 15 and category not in new_categories:  # Threshold for search-based
                new_categories.append(category)
        
        # Update in database
        updated_categorization = {
            "categories": list(set(new_categories)),
            "category_scores": current_scores,
            "last_recategorized": datetime.utcnow(),
            "categorization_type": "search_behavior"
        }
        
        self.users_col.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"ai_categories": updated_categorization}}
        )
        
        return updated_categorization
    
    def get_user_categories(self, user_id):
        """Get user's current AI categories"""
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        if user:
            return user.get("ai_categories", {}).get("categories", [])
        return []
    
    def get_category_explanation(self):
        """Return explanation of all categories"""
        return {
            "demographic": {
                "young_adult": "Users under 25 years old",
                "early_career": "Users aged 25-35",
                "mid_career_family": "Users aged 36-45 with family",
                "established_professional": "Users aged 46-60",
                "senior": "Users over 60",
                "urban_resident": "Lives in urban area",
                "rural_resident": "Lives in rural area"
            },
            "professional": {
                "government_employee": "Works in government sector",
                "education_professional": "Teacher/lecturer/professor",
                "tech_professional": "IT/Engineering professional",
                "management": "Manager or executive",
                "business_owner": "Business owner/entrepreneur",
                "student": "Current student"
            },
            "behavioral": {
                "education_seeker": "Interested in education and courses",
                "course_buyer": "Likely to purchase courses",
                "book_buyer": "Interested in books",
                "past_paper_buyer": "Interested in past papers",
                "tech_enthusiast": "Interested in technology",
                "electronics_buyer": "Likely to buy electronics",
                "vehicle_buyer": "Interested in vehicles",
                "property_seeker": "Looking for property",
                "property_investor": "Property investment interest",
                "career_focused": "Career development focused",
                "investment_focused": "Investment opportunities",
                "health_focused": "Health and wellness interest",
                "news_reader": "Regular news consumer",
                "family_oriented": "Family-focused purchases"
            }
        }


def get_ai_categorizer(db):
    """Factory function to get categorizer instance"""
    return AIUserCategorizer(db)