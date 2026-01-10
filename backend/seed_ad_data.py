"""
Mock Data Generator for Advertisement Recommendation System
Generates 100 users, 20+ ads, and 3 months of behavioral data
"""

from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from bson import ObjectId

# Import models
from models.advertisement import Advertisement
from models.user_profile import UserProfile
from models.user_activity import UserActivity
from models.ad_click import AdClick
from models.user import User

# Configuration
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'government_portal'

# Connect to MongoDB
print("🔌 Connecting to MongoDB...")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Initialize models
ad_model = Advertisement(db)
profile_model = UserProfile(db)
activity_model = UserActivity(db)
click_model = AdClick(db)
user_model = User(db)

print("✅ Connected to database")
print("=" * 60)

# ========================================
# PART 1: USER PROFILES DATA
# ========================================

USER_PROFILES = [
    # Teachers (15 users)
    {'name': 'Nimal Perera', 'email': 'nimal.p@email.com', 'age': 32, 'job': 'teacher', 'education': 'Bachelor of Education', 'location': 'Colombo', 'interests': ['Education', 'Health']},
    {'name': 'Kamala Silva', 'email': 'kamala.s@email.com', 'age': 28, 'job': 'teacher', 'education': 'Bachelor of Arts', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Sunil Fernando', 'email': 'sunil.f@email.com', 'age': 45, 'job': 'teacher', 'education': 'Master of Education', 'location': 'Galle', 'interests': ['Education', 'Business']},
    {'name': 'Ayesha Azeez', 'email': 'ayesha.a@email.com', 'age': 35, 'job': 'teacher', 'education': 'Bachelor of Science', 'location': 'Colombo', 'interests': ['Education', 'Health']},
    {'name': 'Rohan Wickrama', 'email': 'rohan.w@email.com', 'age': 29, 'job': 'teacher', 'education': 'Bachelor of Education', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Dilini Jayasinghe', 'email': 'dilini.j@email.com', 'age': 38, 'job': 'teacher', 'education': 'Master of Arts', 'location': 'Colombo', 'interests': ['Education']},
    {'name': 'Kasun Rajapakse', 'email': 'kasun.r@email.com', 'age': 41, 'job': 'teacher', 'education': 'Bachelor of Education', 'location': 'Negombo', 'interests': ['Education', 'Business']},
    {'name': 'Sanduni Perera', 'email': 'sanduni.p@email.com', 'age': 27, 'job': 'teacher', 'education': 'Bachelor of Science', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Malith Rathnayake', 'email': 'malith.r@email.com', 'age': 33, 'job': 'teacher', 'education': 'Master of Education', 'location': 'Galle', 'interests': ['Education', 'Health']},
    {'name': 'Thilini Gunawardena', 'email': 'thilini.g@email.com', 'age': 30, 'job': 'teacher', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Education']},
    {'name': 'Chamara Dias', 'email': 'chamara.d@email.com', 'age': 36, 'job': 'teacher', 'education': 'Bachelor of Education', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Madhavi Fernando', 'email': 'madhavi.f@email.com', 'age': 42, 'job': 'teacher', 'education': 'Master of Science', 'location': 'Colombo', 'interests': ['Education', 'Health']},
    {'name': 'Dinesh Kumara', 'email': 'dinesh.k@email.com', 'age': 31, 'job': 'teacher', 'education': 'Bachelor of Education', 'location': 'Matara', 'interests': ['Education']},
    {'name': 'Samanthi Silva', 'email': 'samanthi.s@email.com', 'age': 34, 'job': 'teacher', 'education': 'Bachelor of Arts', 'location': 'Kandy', 'interests': ['Education', 'Business']},
    {'name': 'Pradeep Wijesinghe', 'email': 'pradeep.w@email.com', 'age': 39, 'job': 'teacher', 'education': 'Master of Education', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    
    # Engineers (20 users)
    {'name': 'Rajitha Bandara', 'email': 'rajitha.b@email.com', 'age': 28, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Business']},
    {'name': 'Nimali Hewage', 'email': 'nimali.h@email.com', 'age': 26, 'job': 'software engineer', 'education': 'Bachelor of IT', 'location': 'Colombo', 'interests': ['Technology', 'Education']},
    {'name': 'Asanka Perera', 'email': 'asanka.p@email.com', 'age': 32, 'job': 'civil engineer', 'education': 'Bachelor of Engineering', 'location': 'Kandy', 'interests': ['Technology', 'Business']},
    {'name': 'Tharushi Wijeratne', 'email': 'tharushi.w@email.com', 'age': 27, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Housing']},
    {'name': 'Chamath Silva', 'email': 'chamath.s@email.com', 'age': 30, 'job': 'software engineer', 'education': 'Master of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Business']},
    {'name': 'Ishara Gunasekara', 'email': 'ishara.g@email.com', 'age': 29, 'job': 'mechanical engineer', 'education': 'Bachelor of Engineering', 'location': 'Galle', 'interests': ['Technology', 'Transport']},
    {'name': 'Dulaj Fernando', 'email': 'dulaj.f@email.com', 'age': 31, 'job': 'software engineer', 'education': 'Bachelor of IT', 'location': 'Colombo', 'interests': ['Technology', 'Education']},
    {'name': 'Hasini Mendis', 'email': 'hasini.m@email.com', 'age': 25, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Health']},
    {'name': 'Sachith Dissanayake', 'email': 'sachith.d@email.com', 'age': 33, 'job': 'electrical engineer', 'education': 'Bachelor of Engineering', 'location': 'Kandy', 'interests': ['Technology', 'Business']},
    {'name': 'Oshadi Perera', 'email': 'oshadi.p@email.com', 'age': 28, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology']},
    {'name': 'Ravindu Jayawardena', 'email': 'ravindu.j@email.com', 'age': 34, 'job': 'software engineer', 'education': 'Master of IT', 'location': 'Colombo', 'interests': ['Technology', 'Business']},
    {'name': 'Kavindi Rathnayake', 'email': 'kavindi.r@email.com', 'age': 27, 'job': 'software engineer', 'education': 'Bachelor of IT', 'location': 'Colombo', 'interests': ['Technology', 'Education']},
    {'name': 'Shanaka Fernando', 'email': 'shanaka.f@email.com', 'age': 35, 'job': 'civil engineer', 'education': 'Master of Engineering', 'location': 'Kandy', 'interests': ['Technology', 'Housing']},
    {'name': 'Udari Silva', 'email': 'udari.s@email.com', 'age': 26, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology']},
    {'name': 'Chathura Gamage', 'email': 'chathura.g@email.com', 'age': 29, 'job': 'software engineer', 'education': 'Bachelor of IT', 'location': 'Colombo', 'interests': ['Technology', 'Business']},
    {'name': 'Manori Jayasuriya', 'email': 'manori.j@email.com', 'age': 30, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Health']},
    {'name': 'Lahiru Pathirana', 'email': 'lahiru.p@email.com', 'age': 32, 'job': 'software engineer', 'education': 'Master of Computer Science', 'location': 'Colombo', 'interests': ['Technology', 'Business']},
    {'name': 'Piyumi Wickramasinghe', 'email': 'piyumi.w@email.com', 'age': 28, 'job': 'software engineer', 'education': 'Bachelor of IT', 'location': 'Colombo', 'interests': ['Technology', 'Education']},
    {'name': 'Nuwan Senanayake', 'email': 'nuwan.s@email.com', 'age': 36, 'job': 'mechanical engineer', 'education': 'Bachelor of Engineering', 'location': 'Galle', 'interests': ['Technology', 'Transport']},
    {'name': 'Shehani Gunathilake', 'email': 'shehani.g@email.com', 'age': 27, 'job': 'software engineer', 'education': 'Bachelor of Computer Science', 'location': 'Colombo', 'interests': ['Technology']},
    
    # Doctors (15 users)
    {'name': 'Anura Jayasinghe', 'email': 'anura.j@email.com', 'age': 38, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health', 'Education']},
    {'name': 'Nishantha Fernando', 'email': 'nishantha.f@email.com', 'age': 42, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Kandy', 'interests': ['Health', 'Technology']},
    {'name': 'Dilrukshi Perera', 'email': 'dilrukshi.p@email.com', 'age': 35, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health']},
    {'name': 'Sarath Kumara', 'email': 'sarath.k@email.com', 'age': 45, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Galle', 'interests': ['Health', 'Business']},
    {'name': 'Chandima Silva', 'email': 'chandima.s@email.com', 'age': 40, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health', 'Education']},
    {'name': 'Gayan Wickramasinghe', 'email': 'gayan.w@email.com', 'age': 37, 'job': 'doctor', 'education': 'MBBS', 'location': 'Kandy', 'interests': ['Health']},
    {'name': 'Nadeesha Rathnayake', 'email': 'nadeesha.r@email.com', 'age': 34, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health', 'Technology']},
    {'name': 'Tharindu Gamage', 'email': 'tharindu.g@email.com', 'age': 39, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Colombo', 'interests': ['Health', 'Business']},
    {'name': 'Sandali Jayawardena', 'email': 'sandali.j@email.com', 'age': 36, 'job': 'doctor', 'education': 'MBBS', 'location': 'Kandy', 'interests': ['Health', 'Education']},
    {'name': 'Ruwan Bandara', 'email': 'ruwan.b@email.com', 'age': 43, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Galle', 'interests': ['Health']},
    {'name': 'Anusha Gunawardena', 'email': 'anusha.g@email.com', 'age': 38, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health', 'Technology']},
    {'name': 'Janaka Silva', 'email': 'janaka.s@email.com', 'age': 41, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Kandy', 'interests': ['Health', 'Business']},
    {'name': 'Menaka Fernando', 'email': 'menaka.f@email.com', 'age': 37, 'job': 'doctor', 'education': 'MBBS', 'location': 'Colombo', 'interests': ['Health']},
    {'name': 'Prasad Wijeratne', 'email': 'prasad.w@email.com', 'age': 44, 'job': 'doctor', 'education': 'MBBS, MD', 'location': 'Colombo', 'interests': ['Health', 'Education']},
    {'name': 'Buddhika Jayasuriya', 'email': 'buddhika.j@email.com', 'age': 39, 'job': 'doctor', 'education': 'MBBS', 'location': 'Kandy', 'interests': ['Health', 'Technology']},
    
    # Business Owners (15 users)
    {'name': 'Ajith Dissanayake', 'email': 'ajith.d@email.com', 'age': 42, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Technology']},
    {'name': 'Lalith Perera', 'email': 'lalith.p@email.com', 'age': 48, 'job': 'business owner', 'education': 'MBA', 'location': 'Colombo', 'interests': ['Business', 'Financial']},
    {'name': 'Sumith Fernando', 'email': 'sumith.f@email.com', 'age': 38, 'job': 'business owner', 'education': 'Bachelor of Commerce', 'location': 'Kandy', 'interests': ['Business', 'Transport']},
    {'name': 'Ranjith Silva', 'email': 'ranjith.s@email.com', 'age': 45, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Technology']},
    {'name': 'Mahesh Gunasekara', 'email': 'mahesh.g@email.com', 'age': 40, 'job': 'business owner', 'education': 'MBA', 'location': 'Galle', 'interests': ['Business', 'Housing']},
    {'name': 'Susantha Jayawardena', 'email': 'susantha.j@email.com', 'age': 43, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Financial']},
    {'name': 'Upul Wickramasinghe', 'email': 'upul.w@email.com', 'age': 46, 'job': 'business owner', 'education': 'MBA', 'location': 'Colombo', 'interests': ['Business', 'Technology']},
    {'name': 'Anil Rathnayake', 'email': 'anil.r@email.com', 'age': 41, 'job': 'business owner', 'education': 'Bachelor of Commerce', 'location': 'Kandy', 'interests': ['Business', 'Education']},
    {'name': 'Bandula Gamage', 'email': 'bandula.g@email.com', 'age': 44, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Transport']},
    {'name': 'Priyantha Silva', 'email': 'priyantha.s@email.com', 'age': 47, 'job': 'business owner', 'education': 'MBA', 'location': 'Galle', 'interests': ['Business', 'Technology']},
    {'name': 'Sarath Perera', 'email': 'sarath.p@email.com', 'age': 39, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Financial']},
    {'name': 'Gamini Fernando', 'email': 'gamini.f@email.com', 'age': 49, 'job': 'business owner', 'education': 'MBA', 'location': 'Colombo', 'interests': ['Business', 'Housing']},
    {'name': 'Nalin Wijesinghe', 'email': 'nalin.w@email.com', 'age': 42, 'job': 'business owner', 'education': 'Bachelor of Commerce', 'location': 'Kandy', 'interests': ['Business', 'Technology']},
    {'name': 'Jayantha Dissanayake', 'email': 'jayantha.d@email.com', 'age': 45, 'job': 'business owner', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Education']},
    {'name': 'Hemantha Jayasuriya', 'email': 'hemantha.j@email.com', 'age': 43, 'job': 'business owner', 'education': 'MBA', 'location': 'Colombo', 'interests': ['Business', 'Financial']},
    
    # Students (20 users)
    {'name': 'Sahan Bandara', 'email': 'sahan.b@email.com', 'age': 22, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Nethmi Silva', 'email': 'nethmi.s@email.com', 'age': 21, 'job': 'student', 'education': 'A/L completed', 'location': 'Kandy', 'interests': ['Education', 'Health']},
    {'name': 'Dasun Perera', 'email': 'dasun.p@email.com', 'age': 23, 'job': 'student', 'education': 'Undergraduate', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Amaya Fernando', 'email': 'amaya.f@email.com', 'age': 20, 'job': 'student', 'education': 'A/L completed', 'location': 'Galle', 'interests': ['Education']},
    {'name': 'Kavindu Jayasinghe', 'email': 'kavindu.j@email.com', 'age': 22, 'job': 'student', 'education': 'Undergraduate', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Dilini Wickrama', 'email': 'dilini.w@email.com', 'age': 21, 'job': 'student', 'education': 'A/L completed', 'location': 'Kandy', 'interests': ['Education', 'Business']},
    {'name': 'Shehan Rathnayake', 'email': 'shehan.r@email.com', 'age': 24, 'job': 'student', 'education': 'Undergraduate', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Nuwani Gunasekara', 'email': 'nuwani.g@email.com', 'age': 20, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education', 'Health']},
    {'name': 'Dhanushka Silva', 'email': 'dhanushka.s@email.com', 'age': 23, 'job': 'student', 'education': 'Undergraduate', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Charuni Perera', 'email': 'charuni.p@email.com', 'age': 21, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education']},
    {'name': 'Raveen Fernando', 'email': 'raveen.f@email.com', 'age': 22, 'job': 'student', 'education': 'Undergraduate', 'location': 'Galle', 'interests': ['Education', 'Technology']},
    {'name': 'Tharusha Mendis', 'email': 'tharusha.m@email.com', 'age': 20, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education', 'Business']},
    {'name': 'Isuru Dissanayake', 'email': 'isuru.d@email.com', 'age': 24, 'job': 'student', 'education': 'Undergraduate', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Sachini Jayawardena', 'email': 'sachini.j@email.com', 'age': 21, 'job': 'student', 'education': 'A/L completed', 'location': 'Kandy', 'interests': ['Education', 'Health']},
    {'name': 'Kasun Wijesinghe', 'email': 'kasun.w@email.com', 'age': 23, 'job': 'student', 'education': 'Undergraduate', 'location': 'Colombo', 'interests': ['Education', 'Technology']},
    {'name': 'Dinali Rathnayake', 'email': 'dinali.r@email.com', 'age': 20, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education']},
    {'name': 'Thisara Gamage', 'email': 'thisara.g@email.com', 'age': 22, 'job': 'student', 'education': 'Undergraduate', 'location': 'Kandy', 'interests': ['Education', 'Technology']},
    {'name': 'Sachini Silva', 'email': 'sachini.si@email.com', 'age': 21, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education', 'Business']},
    {'name': 'Chatura Pathirana', 'email': 'chatura.p@email.com', 'age': 24, 'job': 'student', 'education': 'Undergraduate', 'location': 'Galle', 'interests': ['Education', 'Technology']},
    {'name': 'Imesha Wickramasinghe', 'email': 'imesha.w@email.com', 'age': 20, 'job': 'student', 'education': 'A/L completed', 'location': 'Colombo', 'interests': ['Education', 'Health']},
    
    # Government Officers (15 users)
    {'name': 'Wasantha Silva', 'email': 'wasantha.s@email.com', 'age': 35, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Education']},
    {'name': 'Athula Perera', 'email': 'athula.p@email.com', 'age': 40, 'job': 'government officer', 'education': 'Bachelor of Commerce', 'location': 'Kandy', 'interests': ['Business', 'Financial']},
    {'name': 'Anoja Fernando', 'email': 'anoja.f@email.com', 'age': 38, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Education']},
    {'name': 'Chaminda Jayasinghe', 'email': 'chaminda.j@email.com', 'age': 42, 'job': 'government officer', 'education': 'Bachelor of Business', 'location': 'Galle', 'interests': ['Business', 'Housing']},
    {'name': 'Sumana Wickrama', 'email': 'sumana.w@email.com', 'age': 36, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Health']},
    {'name': 'Lakshman Rathnayake', 'email': 'lakshman.r@email.com', 'age': 39, 'job': 'government officer', 'education': 'Bachelor of Commerce', 'location': 'Kandy', 'interests': ['Business', 'Financial']},
    {'name': 'Nilmini Gunasekara', 'email': 'nilmini.g@email.com', 'age': 37, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Education']},
    {'name': 'Wimal Silva', 'email': 'wimal.s@email.com', 'age': 41, 'job': 'government officer', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Technology']},
    {'name': 'Shirani Perera', 'email': 'shirani.p@email.com', 'age': 38, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Kandy', 'interests': ['Business', 'Education']},
    {'name': 'Sudath Fernando', 'email': 'sudath.f@email.com', 'age': 43, 'job': 'government officer', 'education': 'Bachelor of Commerce', 'location': 'Galle', 'interests': ['Business', 'Financial']},
    {'name': 'Chandrika Jayawardena', 'email': 'chandrika.j@email.com', 'age': 36, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Health']},
    {'name': 'Siripala Wickramasinghe', 'email': 'siripala.w@email.com', 'age': 40, 'job': 'government officer', 'education': 'Bachelor of Business', 'location': 'Colombo', 'interests': ['Business', 'Housing']},
    {'name': 'Dharshani Dissanayake', 'email': 'dharshani.d@email.com', 'age': 37, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Kandy', 'interests': ['Business', 'Education']},
    {'name': 'Palitha Gamage', 'email': 'palitha.g@email.com', 'age': 42, 'job': 'government officer', 'education': 'Bachelor of Commerce', 'location': 'Colombo', 'interests': ['Business', 'Financial']},
    {'name': 'Sriyani Silva', 'email': 'sriyani.s@email.com', 'age': 39, 'job': 'government officer', 'education': 'Bachelor of Arts', 'location': 'Colombo', 'interests': ['Business', 'Technology']},
]

# ========================================
# PART 2: ADVERTISEMENT DATA
# ========================================

ADVERTISEMENTS = [
    # Education Ads (7)
    {
        'title': 'Online Python Programming Course - 50% Off',
        'description': 'Master Python programming with our comprehensive online course. Perfect for students and professionals.',
        'image_url': 'https://example.com/images/python-course.jpg',
        'link_url': 'https://example.com/courses/python',
        'category': 'Education',
        'target_age_min': 18,
        'target_age_max': 35,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['student', 'engineer', 'teacher'],
        'target_categories': ['education_seeker', 'tech_enthusiast', 'course_buyer', 'student', 'tech_professional'],
        'budget': 50000.0,
        'bid_amount': 8.0
    },
    {
        'title': 'MBA Program - Admissions Open',
        'description': 'Join our prestigious MBA program. Flexible schedules for working professionals.',
        'image_url': 'https://example.com/images/mba.jpg',
        'link_url': 'https://example.com/education/mba',
        'category': 'Education',
        'target_age_min': 25,
        'target_age_max': 45,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['business owner', 'manager', 'engineer'],
        'target_categories': ['education_seeker', 'management', 'business_owner', 'early_career', 'mid_career_family'],
        'budget': 80000.0,
        'bid_amount': 12.0
    },
    {
        'title': 'English Speaking Course - Start Today',
        'description': 'Improve your English speaking skills with native speakers. Online and offline classes available.',
        'image_url': 'https://example.com/images/english-course.jpg',
        'link_url': 'https://example.com/courses/english',
        'category': 'Education',
        'target_age_min': 18,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['student', 'teacher', 'government officer'],
        'target_categories': ['education_seeker', 'course_buyer', 'student', 'young_adult'],
        'budget': 40000.0,
        'bid_amount': 6.0
    },
    {
        'title': 'Data Science Bootcamp - Career Guaranteed',
        'description': 'Become a data scientist in 6 months. Job placement assistance included.',
        'image_url': 'https://example.com/images/data-science.jpg',
        'link_url': 'https://example.com/bootcamp/data-science',
        'category': 'Education',
        'target_age_min': 22,
        'target_age_max': 35,
        'target_locations': ['Colombo'],
        'target_jobs': ['engineer', 'student', 'it professional'],
        'target_categories': ['tech_enthusiast', 'tech_professional', 'course_buyer', 'job_seeker', 'early_career'],
        'budget': 100000.0,
        'bid_amount': 15.0
    },
    {
        'title': 'O/L & A/L Exam Preparation Classes',
        'description': 'Expert teachers for all subjects. High success rate. Limited seats available.',
        'image_url': 'https://example.com/images/exam-prep.jpg',
        'link_url': 'https://example.com/tuition/exam-prep',
        'category': 'Education',
        'target_age_min': 14,
        'target_age_max': 20,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['student'],
        'target_categories': ['student', 'young_adult', 'education_seeker'],
        'budget': 60000.0,
        'bid_amount': 7.0
    },
    {
        'title': 'Digital Marketing Masterclass',
        'description': 'Learn SEO, Social Media Marketing, Google Ads. Perfect for entrepreneurs.',
        'image_url': 'https://example.com/images/digital-marketing.jpg',
        'link_url': 'https://example.com/courses/digital-marketing',
        'category': 'Education',
        'target_age_min': 25,
        'target_age_max': 45,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['business owner', 'manager', 'entrepreneur'],
        'target_categories': ['business_owner', 'course_buyer', 'tech_enthusiast', 'management'],
        'budget': 70000.0,
        'bid_amount': 10.0
    },
    {
        'title': 'Professional Photography Course',
        'description': 'Learn photography from basics to advanced. Hands-on training with DSLR cameras.',
        'image_url': 'https://example.com/images/photography.jpg',
        'link_url': 'https://example.com/courses/photography',
        'category': 'Education',
        'target_age_min': 20,
        'target_age_max': 40,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['student', 'teacher', 'business owner'],
        'target_categories': ['course_buyer', 'education_seeker', 'young_adult', 'early_career'],
        'budget': 45000.0,
        'bid_amount': 7.0
    },
    
    # Technology Ads (5)
    {
        'title': 'Latest Laptops - EMI Available',
        'description': 'Premium laptops for students and professionals. 0% interest EMI. Free delivery in Colombo.',
        'image_url': 'https://example.com/images/laptop.jpg',
        'link_url': 'https://example.com/shop/laptops',
        'category': 'Technology',
        'target_age_min': 20,
        'target_age_max': 40,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['student', 'engineer', 'teacher'],
        'target_categories': ['tech_enthusiast', 'electronics_buyer', 'student', 'tech_professional'],
        'budget': 90000.0,
        'bid_amount': 12.0
    },
    {
        'title': 'Smartphone Sale - Up to 40% Off',
        'description': 'Premium smartphones at unbeatable prices. Latest models available.',
        'image_url': 'https://example.com/images/smartphone.jpg',
        'link_url': 'https://example.com/shop/phones',
        'category': 'Technology',
        'target_age_min': 18,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['student', 'engineer', 'business owner', 'doctor'],
        'target_categories': ['tech_enthusiast', 'electronics_buyer', 'young_adult', 'early_career', 'mid_career_family'],
        'budget': 120000.0,
        'bid_amount': 10.0
    },
    {
        'title': 'Cloud Storage - 1TB Free',
        'description': 'Secure cloud storage for your important files. Sign up now and get 1TB free for 3 months.',
        'image_url': 'https://example.com/images/cloud-storage.jpg',
        'link_url': 'https://example.com/services/cloud',
        'category': 'Technology',
        'target_age_min': 22,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['engineer', 'business owner', 'doctor'],
        'target_categories': ['tech_enthusiast', 'tech_professional', 'business_owner', 'management'],
        'budget': 55000.0,
        'bid_amount': 8.0
    },
    {
        'title': 'Gaming Laptop - Special Offer',
        'description': 'High-performance gaming laptops with latest graphics cards. Perfect for gamers and designers.',
        'image_url': 'https://example.com/images/gaming-laptop.jpg',
        'link_url': 'https://example.com/shop/gaming-laptops',
        'category': 'Technology',
        'target_age_min': 18,
        'target_age_max': 35,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['student', 'engineer'],
        'target_categories': ['tech_enthusiast', 'electronics_buyer', 'student', 'tech_professional', 'young_adult'],
        'budget': 75000.0,
        'bid_amount': 11.0
    },
    {
        'title': 'Smart Home Devices - Automate Your Life',
        'description': 'Smart lights, cameras, and voice assistants. Control your home from anywhere.',
        'image_url': 'https://example.com/images/smart-home.jpg',
        'link_url': 'https://example.com/shop/smart-home',
        'category': 'Technology',
        'target_age_min': 25,
        'target_age_max': 50,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['engineer', 'business owner', 'doctor'],
        'target_categories': ['tech_enthusiast', 'electronics_buyer', 'property_seeker', 'established_professional'],
        'budget': 65000.0,
        'bid_amount': 9.0
    },
    
    # Vehicle & Transport Ads (3)
    {
        'title': 'New Car Models - Test Drive Today',
        'description': 'Latest car models with best financing options. Visit our showroom this weekend.',
        'image_url': 'https://example.com/images/new-car.jpg',
        'link_url': 'https://example.com/vehicles/new-cars',
        'category': 'Transport',
        'target_age_min': 28,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['engineer', 'doctor', 'business owner'],
        'target_categories': ['vehicle_buyer', 'established_professional', 'mid_career_family', 'business_owner'],
        'budget': 150000.0,
        'bid_amount': 20.0
    },
    {
        'title': 'Driving School - Get Your License Fast',
        'description': 'Professional driving instructors. High pass rate. Flexible timings available.',
        'image_url': 'https://example.com/images/driving-school.jpg',
        'link_url': 'https://example.com/services/driving-school',
        'category': 'Transport',
        'target_age_min': 18,
        'target_age_max': 40,
        'target_locations': ['Colombo', 'Kandy', 'Galle', 'Negombo'],
        'target_jobs': ['student', 'teacher', 'engineer'],
        'target_categories': ['young_adult', 'early_career', 'student'],
        'budget': 35000.0,
        'bid_amount': 6.0
    },
    {
        'title': 'Used Cars - Best Deals',
        'description': 'Quality used cars with warranty. Low mileage, well maintained. Easy financing.',
        'image_url': 'https://example.com/images/used-car.jpg',
        'link_url': 'https://example.com/vehicles/used-cars',
        'category': 'Transport',
        'target_age_min': 25,
        'target_age_max': 45,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['engineer', 'teacher', 'business owner'],
        'target_categories': ['vehicle_buyer', 'early_career', 'mid_career_family'],
        'budget': 80000.0,
        'bid_amount': 12.0
    },
    
    # Health Ads (3)
    {
        'title': 'Health Insurance - Family Plans',
        'description': 'Comprehensive health coverage for your entire family. Affordable premiums.',
        'image_url': 'https://example.com/images/health-insurance.jpg',
        'link_url': 'https://example.com/insurance/health',
        'category': 'Health',
        'target_age_min': 28,
        'target_age_max': 55,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['engineer', 'doctor', 'teacher', 'business owner'],
        'target_categories': ['health_focused', 'parent', 'mid_career_family', 'established_professional'],
        'budget': 70000.0,
        'bid_amount': 10.0
    },
    {
        'title': 'Gym Membership - Special Discount',
        'description': 'State-of-the-art gym with personal trainers. Get fit in 3 months guaranteed.',
        'image_url': 'https://example.com/images/gym.jpg',
        'link_url': 'https://example.com/fitness/gym',
        'category': 'Health',
        'target_age_min': 20,
        'target_age_max': 45,
        'target_locations': ['Colombo', 'Kandy'],
        'target_jobs': ['engineer', 'student', 'doctor', 'business owner'],
        'target_categories': ['health_focused', 'young_adult', 'early_career', 'mid_career_family'],
        'budget': 45000.0,
        'bid_amount': 7.0
    },
    {
        'title': 'Medical Checkup Packages',
        'description': 'Complete health screening at affordable prices. Book your appointment online.',
        'image_url': 'https://example.com/images/checkup.jpg',
        'link_url': 'https://example.com/health/checkup',
        'category': 'Health',
        'target_age_min': 30,
        'target_age_max': 65,
        'target_locations': ['Colombo', 'Kandy', 'Galle'],
        'target_jobs': ['engineer', 'doctor', 'teacher', 'business owner', 'government officer'],
        'target_categories': ['health_focused', 'established_professional', 'senior', 'mid_career_family'],
        'budget': 60000.0,
        'bid_amount': 9.0
    },
    
    # Property & Housing Ads (2)
    {
        'title': 'Luxury Apartments - Colombo 7',
        'description': 'Premium apartments with sea view. Modern amenities. Easy payment plans.',
        'image_url': 'https://example.com/images/apartment.jpg',
        'link_url': 'https://example.com/property/apartments',
        'category': 'Housing',
        'target_age_min': 30,
        'target_age_max': 55,
        'target_locations': ['Colombo'],
        'target_jobs': ['engineer', 'doctor', 'business owner'],
        'target_categories': ['property_seeker', 'established_professional', 'mid_career_family'],
        'budget': 200000.0,
        'bid_amount': 25.0
    },
    {
        'title': 'Land for Sale - Kandy District',
        'description': 'Prime land plots near Kandy city. Perfect for building your dream home.',
        'image_url': 'https://example.com/images/land.jpg',
        'link_url': 'https://example.com/property/land',
        'category': 'Housing',
        'target_age_min': 35,
        'target_age_max': 60,
        'target_locations': ['Kandy', 'Colombo'],
        'target_jobs': ['doctor', 'business owner', 'engineer'],
        'target_categories': ['property_seeker', 'established_professional', 'business_owner'],
        'budget': 180000.0,
        'bid_amount': 22.0
    },
]

# ========================================
# PART 3: SEARCH PATTERNS
# ========================================

# Common search queries by category
SEARCH_QUERIES = {
    'Education': [
        'university admission', 'exam results', 'scholarship application', 
        'online courses', 'o/l results', 'a/l results', 'degree programs',
        'vocational training', 'student visa', 'education loan'
    ],
    'Technology': [
        'laptop price', 'smartphone deals', 'internet connection',
        'software download', 'tech support', 'computer repair',
        'online shopping', 'mobile apps', 'cloud storage'
    ],
    'Health': [
        'hospital services', 'doctor appointment', 'medical certificate',
        'health insurance', 'vaccination', 'health checkup',
        'pharmacy', 'medical report', 'health tips'
    ],
    'Business': [
        'business registration', 'tax filing', 'company incorporation',
        'trade license', 'business loan', 'accounting services',
        'business plan', 'startup guide', 'business insurance'
    ],
    'Transport': [
        'driving license', 'vehicle registration', 'passport application',
        'visa application', 'travel permit', 'car insurance',
        'vehicle tax', 'road tax', 'traffic fines'
    ],
    'Housing': [
        'property registration', 'land deed', 'building permit',
        'house plans', 'mortgage loan', 'rent agreement',
        'property tax', 'house for sale', 'apartment for rent'
    ],
    'Employment': [
        'job vacancies', 'government jobs', 'resume writing',
        'job application', 'employment certificate', 'salary slip',
        'job interview tips', 'career guidance', 'job training'
    ],
    'Financial': [
        'bank account', 'loan application', 'credit card',
        'fixed deposit', 'savings account', 'investment options',
        'tax returns', 'pension scheme', 'financial planning'
    ]
}

# ========================================
# MAIN GENERATION FUNCTIONS
# ========================================

def create_users():
    """Create 100 mock users"""
    print("\n📝 STEP 1: Creating Mock Users...")
    print("-" * 60)
    
    created_users = []
    
    for user_data in USER_PROFILES:
        try:
            # Check if user already exists
            existing_user = user_model.find_by_email(user_data['email'])
            if existing_user:
                print(f"⚠️  User already exists: {user_data['email']}")
                created_users.append(str(existing_user['_id']))
                continue
            
            # Set password
            user_data['password'] = 'password123'
            
            # Add additional fields
            user_data['marital_status'] = random.choice(['single', 'married', 'married', 'single'])
            user_data['children'] = []
            user_data['experience_years'] = max(0, user_data['age'] - 22) if user_data['job'] != 'student' else 0
            
            # Create user
            user_id = user_model.create(user_data)
            created_users.append(user_id)
            
            print(f"✅ Created: {user_data['name']} ({user_data['job']}) - {user_data['email']}")
            
        except Exception as e:
            print(f"❌ Error creating user {user_data['email']}: {e}")
    
    print(f"\n✨ Total users created/found: {len(created_users)}")
    return created_users

def create_advertisements():
    """Create 20+ mock advertisements"""
    print("\n📝 STEP 2: Creating Advertisements...")
    print("-" * 60)
    
    created_ads = []
    
    for ad_data in ADVERTISEMENTS:
        try:
            # Check if ad already exists by title
            existing_ads = ad_model.search_ads({'title': ad_data['title']})
            if existing_ads:
                print(f"⚠️  Ad already exists: {ad_data['title']}")
                created_ads.append(existing_ads[0]['_id'])
                continue
            
            ad_id = ad_model.create(ad_data)
            created_ads.append(ad_id)
            
            print(f"✅ Created: {ad_data['title']} ({ad_data['category']})")
            
        except Exception as e:
            print(f"❌ Error creating ad {ad_data['title']}: {e}")
    
    print(f"\n✨ Total ads created/found: {len(created_ads)}")
    return created_ads

def generate_user_behavior(user_ids, ad_ids):
    """Generate 3 months of user behavior data"""
    print("\n📝 STEP 3: Generating 3 Months of User Behavior...")
    print("-" * 60)
    
    start_date = datetime.utcnow() - timedelta(days=90)
    
    for user_id in user_ids:
        try:
            # Get user details
            user = user_model.find_by_id(user_id)
            if not user:
                continue
            
            user_interests = user.get('interests', ['Education'])
            
            # Create or get profile
            profile_model.create_or_get(user_id)
            
            # Generate 10-30 searches per user over 3 months
            num_searches = random.randint(10, 30)
            
            for _ in range(num_searches):
                # Pick a random date in the last 90 days
                days_ago = random.randint(0, 90)
                search_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # Pick a category based on user interests
                if user_interests:
                    category = random.choice(user_interests)
                else:
                    category = random.choice(list(SEARCH_QUERIES.keys()))
                
                # Pick a search query
                query = random.choice(SEARCH_QUERIES[category])
                
                # Log the search
                activity_model.log_search(user_id, query, category, random.randint(1, 10))
                
                # Update profile
                profile_model.add_recent_search(user_id, query, category)
                
                # Extract keywords
                keywords = query.split()
                profile_model.update_search_keywords(user_id, keywords)
            
            # Generate 5-15 service views
            num_views = random.randint(5, 15)
            for _ in range(num_views):
                days_ago = random.randint(0, 90)
                view_date = datetime.utcnow() - timedelta(days=days_ago)
                
                category = random.choice(user_interests) if user_interests else 'Education'
                
                activity_model.log_service_view(
                    user_id, 
                    str(ObjectId()), 
                    f"Service in {category}", 
                    category
                )
                
                profile_model.add_recent_click(user_id, 'service', str(ObjectId()), category)
                profile_model.increment_service_views(user_id)
            
            # Detect life events
            profile_model.detect_life_events(user_id)
            
            print(f"✅ Generated behavior for: {user['name']} ({num_searches} searches, {num_views} views)")
            
        except Exception as e:
            print(f"❌ Error generating behavior for user {user_id}: {e}")
    
    print(f"\n✨ Behavior data generated for {len(user_ids)} users")

def generate_ad_clicks(user_ids, ad_ids):
    """Generate realistic ad click history"""
    print("\n📝 STEP 4: Generating Ad Click History...")
    print("-" * 60)
    
    total_clicks = 0
    
    # Get all ads
    all_ads = ad_model.get_all_active()
    
    for user_id in user_ids:
        try:
            user = user_model.find_by_id(user_id)
            if not user:
                continue
            
            profile = profile_model.get_by_user_id(user_id)
            if not profile:
                continue
            
            user_interests = user.get('interests', [])
            
            # 30% of users click on ads (realistic)
            if random.random() < 0.3:
                # Click on 1-3 ads
                num_clicks = random.randint(1, 3)
                
                for _ in range(num_clicks):
                    # Find matching ads
                    matching_ads = [
                        ad for ad in all_ads 
                        if ad.get('category') in user_interests
                    ]
                    
                    if not matching_ads:
                        matching_ads = all_ads
                    
                    if matching_ads:
                        clicked_ad = random.choice(matching_ads)
                        
                        # Log ad click
                        days_ago = random.randint(0, 90)
                        
                        activity_model.log_ad_click(
                            user_id,
                            clicked_ad['_id'],
                            clicked_ad['title'],
                            clicked_ad['category']
                        )
                        
                        # Record in ad_clicks collection
                        click_model.record_click(user_id, clicked_ad['_id'], clicked_ad)
                        
                        # Update ad statistics
                        ad_model.record_impression(clicked_ad['_id'])
                        ad_model.record_click(clicked_ad['_id'], clicked_ad.get('bid_amount', 5.0))
                        
                        # Update user profile
                        profile_model.add_recent_click(
                            user_id, 
                            'ad', 
                            clicked_ad['_id'], 
                            clicked_ad['category']
                        )
                        
                        total_clicks += 1
                        
                        print(f"  👆 {user['name']} clicked: {clicked_ad['title']}")
        
        except Exception as e:
            print(f"❌ Error generating clicks for user {user_id}: {e}")
    
    print(f"\n✨ Total ad clicks generated: {total_clicks}")

def generate_ad_impressions(ad_ids):
    """Generate random impressions for ads (so CTR is realistic)"""
    print("\n📝 STEP 5: Generating Ad Impressions...")
    print("-" * 60)
    
    for ad_id in ad_ids:
        try:
            # Generate 50-200 impressions per ad
            num_impressions = random.randint(50, 200)
            
            for _ in range(num_impressions):
                ad_model.record_impression(ad_id)
            
            ad = ad_model.find_by_id(ad_id)
            print(f"✅ {ad['title']}: {num_impressions} impressions")
            
        except Exception as e:
            print(f"❌ Error generating impressions for ad {ad_id}: {e}")
    
    print(f"\n✨ Impressions generated for {len(ad_ids)} ads")

def print_summary():
    """Print summary statistics"""
    print("\n" + "=" * 60)
    print("📊 DATA GENERATION SUMMARY")
    print("=" * 60)
    
    # Count users
    total_users = db.users.count_documents({})
    print(f"\n👥 Total Users: {total_users}")
    
    # Count ads
    total_ads = db.advertisements.count_documents({})
    print(f"📢 Total Advertisements: {total_ads}")
    
    # Count activities
    total_searches = db.user_activities.count_documents({'activity_type': 'search'})
    total_views = db.user_activities.count_documents({'activity_type': 'service_view'})
    total_ad_clicks = db.user_activities.count_documents({'activity_type': 'ad_click'})
    
    print(f"\n🔍 Total Searches: {total_searches}")
    print(f"👀 Total Service Views: {total_views}")
    print(f"👆 Total Ad Clicks: {total_ad_clicks}")
    
    # Count profiles
    total_profiles = db.user_profiles.count_documents({})
    print(f"\n📊 User Profiles Created: {total_profiles}")
    
    # Get top performing ads
    print("\n🏆 Top 5 Performing Ads by CTR:")
    top_ads = ad_model.get_top_performing(5)
    for i, ad in enumerate(top_ads, 1):
        print(f"  {i}. {ad['title']}: {ad.get('ctr', 0)}% CTR ({ad.get('clicks', 0)} clicks / {ad.get('impressions', 0)} impressions)")
    
    print("\n" + "=" * 60)
    print("✅ MOCK DATA GENERATION COMPLETED!")
    print("=" * 60)
    print("\n💡 Next Steps:")
    print("  1. The system is now ready with 3 months of historical data")
    print("  2. You can start testing the recommendation engine")
    print("  3. Real user data will continue to accumulate")
    print("\n")

# ========================================
# MAIN EXECUTION
# ========================================

def main():
    """Main function to run all data generation"""
    
    print("\n" + "=" * 60)
    print("🚀 STARTING MOCK DATA GENERATION")
    print("=" * 60)
    print("\nThis will generate:")
    print("  • 100 realistic mock users")
    print("  • 20+ targeted advertisements")
    print("  • 3 months of user behavior data")
    print("  • Realistic ad click history")
    print("\n" + "=" * 60)
    
    try:
        # Step 1: Create users
        user_ids = create_users()
        
        # Step 2: Create advertisements
        ad_ids = create_advertisements()
        
        # Step 3: Generate user behavior (searches, views)
        generate_user_behavior(user_ids, ad_ids)
        
        # Step 4: Generate ad clicks
        generate_ad_clicks(user_ids, ad_ids)
        
        # Step 5: Generate ad impressions
        generate_ad_impressions(ad_ids)
        
        # Print summary
        print_summary()
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
