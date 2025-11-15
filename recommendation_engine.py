import numpy as np
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()


class RecommendationEngine:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client["citizen_portal"]
        self.users_col = self.db["users"]
        self.eng_col = self.db["engagements"]
        self.ads_col = self.db["ads"]
    
    def get_user_segment(self, user_id):
        """Segment users based on demographics and behavior"""
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return ["unknown"]
        
        profile = user.get('extended_profile', {})
        engagements = list(self.eng_col.find({"user_id": user_id}).sort("timestamp", -1).limit(50))
        
        # Demographic segmentation
        age = user.get('age') or profile.get('family', {}).get('age')
        education = profile.get('education', {}).get('highest_qualification', 'unknown')
        children = profile.get('family', {}).get('children', [])
        job = user.get('job') or profile.get('career', {}).get('current_job', 'unknown')
        
        segment = []
        
        # Age-based segments
        if age:
            if age < 25:
                segment.append("young_adult")
            elif 25 <= age <= 35:
                segment.append("early_career")
            elif 36 <= age <= 45:
                segment.append("mid_career_family")
            elif 46 <= age <= 60:
                segment.append("established_professional")
            else:
                segment.append("senior")
        
        # Education-based segments
        if education in ['none', 'school', 'ol']:
            segment.append("needs_qualification")
        elif education in ['al', 'diploma']:
            segment.append("mid_education")
        elif education in ['degree', 'masters', 'phd']:
            segment.append("highly_educated")
        
        # Family-based segments
        if children:
            segment.append("parent")
            children_ages = profile.get('family', {}).get('children_ages', [])
            if any(age in [5, 6, 7, 8, 9, 10] for age in children_ages):
                segment.append("primary_school_parent")
            if any(age in [11, 12, 13, 14, 15, 16] for age in children_ages):
                segment.append("secondary_school_parent")
            if any(age in [17, 18, 19, 20] for age in children_ages):
                segment.append("university_age_parent")
        
        # Career-based segments
        if job:
            if 'government' in job.lower():
                segment.append("government_employee")
            if any(word in job.lower() for word in ['manager', 'director', 'head']):
                segment.append("management")
        
        return list(set(segment))
    
    def get_personalized_ads(self, user_id, limit=5):
        """Get personalized ads based on user segment and behavior"""
        segments = self.get_user_segment(user_id)
        user_engagements = list(self.eng_col.find({"user_id": user_id}))
        
        # Extract interests from engagements
        interests = []
        for eng in user_engagements:
            interests.extend(eng.get('desires', []))
            if eng.get('question_clicked'):
                interests.append(eng['question_clicked'])
            if eng.get('service'):
                interests.append(eng['service'])
        
        # Score ads based on relevance
        ads = list(self.ads_col.find({"active": True}))
        scored_ads = []
        
        for ad in ads:
            score = 0
            ad_tags = ad.get('tags', [])
            ad_segments = ad.get('target_segments', [])
            
            # Segment matching
            segment_match = len(set(segments) & set(ad_segments))
            score += segment_match * 10
            
            # Interest matching
            interest_match = len(set(interests) & set(ad_tags))
            score += interest_match * 5
            
            # Recency boost
            if ad.get('created'):
                days_old = (datetime.utcnow() - ad['created']).days
                if days_old < 7:
                    score += 5
                elif days_old < 30:
                    score += 2
            
            scored_ads.append((ad, score))
        
        # Sort by score and return top ones
        scored_ads.sort(key=lambda x: x[1], reverse=True)
        return [ad for ad, score in scored_ads[:limit]]
    
    def generate_education_recommendations(self, user_id):
        """Generate education recommendations based on profile"""
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        profile = user.get('extended_profile', {})
        education = profile.get('education', {})
        career = profile.get('career', {})
        age = user.get('age') or profile.get('family', {}).get('age')
        
        recommendations = []
        
        # Degree completion for government employees without degrees
        if (education.get('highest_qualification') in ['ol', 'al', 'diploma'] and
            career.get('current_job', '').lower().find('government') != -1 and
            age and 25 <= age <= 50):
            recommendations.append({
                "type": "education",
                "title": "Complete Your Degree",
                "message": "Enhance your career with a recognized degree program",
                "priority": "high",
                "tags": ["degree", "government", "career_advancement"]
            })
        
        # Children education recommendations
        children_ages = profile.get('family', {}).get('children_ages', [])
        children_education = profile.get('family', {}).get('children_education', [])
        
        for i, child_age in enumerate(children_ages):
            if 15 <= child_age <= 18:
                if i < len(children_education) and 'ol' not in children_education[i].lower():
                    recommendations.append({
                        "type": "child_education",
                        "title": "O/L Exam Preparation",
                        "message": "Special courses for your child's O/L exams",
                        "priority": "medium",
                        "tags": ["ol_exams", "tuition", "secondary_education"]
                    })
            
            if 17 <= child_age <= 20:
                if i < len(children_education) and 'al' not in children_education[i].lower():
                    recommendations.append({
                        "type": "child_education",
                        "title": "A/L Stream Selection Guidance",
                        "message": "Expert guidance for A/L subject selection",
                        "priority": "medium",
                        "tags": ["al_exams", "career_guidance", "higher_education"]
                    })
        
        return recommendations
    
    def get_career_recommendations(self, user_id):
        """Generate career development recommendations"""
        user = self.users_col.find_one({"_id": ObjectId(user_id)})
        if not user:
            return []
        
        profile = user.get('extended_profile', {})
        career = profile.get('career', {})
        age = user.get('age') or profile.get('family', {}).get('age')
        
        recommendations = []
        
        # IELTS for young professionals
        if age and 25 <= age <= 35:
            recommendations.append({
                "type": "career",
                "title": "IELTS Preparation Course",
                "message": "Prepare for overseas opportunities with IELTS certification",
                "priority": "high",
                "tags": ["ielts", "overseas", "career_growth"]
            })
        
        # Skill development
        career_goals = career.get('career_goals', [])
        if 'skill_development' in career_goals or 'career_advancement' in career_goals:
            recommendations.append({
                "type": "career",
                "title": "Professional Development Courses",
                "message": "Advance your career with industry-recognized certifications",
                "priority": "medium",
                "tags": ["skills", "certification", "career_growth"]
            })
        
        return recommendations
    
    def analyze_search_behavior(self, user_id):
        """Analyze user search patterns and re-categorize"""
        try:
            # Get user's recent searches
            search_col = self.db["user_searches"]
            recent_searches = list(search_col.find(
                {"user_id": user_id}
            ).sort("timestamp", -1).limit(50))
            
            if not recent_searches:
                return self.get_user_segment(user_id)
            
            # Extract keywords from searches
            keywords = []
            for search in recent_searches:
                keywords.append(search.get("query", "").lower())
            
            # Get base segments
            base_segments = self.get_user_segment(user_id)
            
            # Add interest-based segments from searches
            interest_segments = []
            
            # Education interests
            education_keywords = ['degree', 'course', 'study', 'education', 'tuition', 'exam', 'ol', 'al', 'university']
            if any(kw in ' '.join(keywords) for kw in education_keywords):
                interest_segments.append("education_seeker")
            
            # Job/Career interests
            job_keywords = ['job', 'career', 'employment', 'work', 'visa', 'overseas', 'salary']
            if any(kw in ' '.join(keywords) for kw in job_keywords):
                interest_segments.append("job_seeker")
            
            # Technology interests
            tech_keywords = ['laptop', 'computer', 'phone', 'tablet', 'electronic', 'tech', 'software']
            if any(kw in ' '.join(keywords) for kw in tech_keywords):
                interest_segments.append("tech_enthusiast")
            
            # Property interests
            property_keywords = ['land', 'house', 'property', 'real estate', 'rent', 'buy']
            if any(kw in ' '.join(keywords) for kw in property_keywords):
                interest_segments.append("property_buyer")
            
            # Vehicle interests
            vehicle_keywords = ['car', 'vehicle', 'bike', 'motorcycle', 'automobile']
            if any(kw in ' '.join(keywords) for kw in vehicle_keywords):
                interest_segments.append("vehicle_buyer")
            
            # Shopping interests
            shopping_keywords = ['buy', 'purchase', 'shop', 'price', 'sale', 'discount']
            if any(kw in ' '.join(keywords) for kw in shopping_keywords):
                interest_segments.append("active_shopper")
            
            # Combine base segments with interest segments
            all_segments = list(set(base_segments + interest_segments))
            
            return all_segments
            
        except Exception as e:
            print(f"Error analyzing search behavior: {e}")
            return self.get_user_segment(user_id)


# Global instance
recommendation_engine = None

def get_recommendation_engine():
    """Get or create recommendation engine instance"""
    global recommendation_engine
    if recommendation_engine is None:
        recommendation_engine = RecommendationEngine()
    return recommendation_engine