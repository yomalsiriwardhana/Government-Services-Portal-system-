"""
Comprehensive Seed Script for Government Portal Ministries
This script loads 20+ government ministries with their subservices, FAQs, downloads, and locations
"""

from pymongo import MongoClient
from datetime import datetime
import sys

# MongoDB connection
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'government_portal'

def seed_ministries():
    """Seed database with 20+ government ministries and their subservices"""
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        ministries_collection = db.ministries
        subservices_collection = db.subservices
        
        print("🔄 Starting ministry seeding process...")
        
        # Clear existing data
        ministries_collection.delete_many({})
        subservices_collection.delete_many({})
        print("✅ Cleared existing ministry data")
        
        # Define 20+ ministries with comprehensive data
        ministries_data = [
            {
                'name': 'Ministry of IT & Digital Affairs',
                'short_name': 'MITDA',
                'description': 'Leading Sri Lanka\'s digital transformation and IT infrastructure development',
                'minister': 'Hon. Digital Affairs Minister',
                'secretary': 'Secretary of IT & Digital Affairs',
                'website': 'https://www.mitda.gov.lk',
                'contact_email': 'info@mitda.gov.lk',
                'contact_phone': '+94-11-2345678',
                'address': 'IT Tower, Colombo 07, Sri Lanka',
                'keywords': 'technology digital IT computer software certificate cyber',
                'icon': 'computer',
                'color': '#3B82F6'
            },
            {
                'name': 'Ministry of Education',
                'short_name': 'MOE',
                'description': 'Empowering Sri Lanka through quality education at all levels',
                'minister': 'Hon. Education Minister',
                'secretary': 'Secretary of Education',
                'website': 'https://www.moe.gov.lk',
                'contact_email': 'info@moe.gov.lk',
                'contact_phone': '+94-11-2369874',
                'address': 'Isurupaya, Battaramulla, Sri Lanka',
                'keywords': 'school education university admission exam results certificate',
                'icon': 'book',
                'color': '#10B981'
            },
            {
                'name': 'Ministry of Health',
                'short_name': 'MOH',
                'description': 'Ensuring accessible and quality healthcare for all citizens',
                'minister': 'Hon. Health Minister',
                'secretary': 'Secretary of Health',
                'website': 'https://www.health.gov.lk',
                'contact_email': 'info@health.gov.lk',
                'contact_phone': '+94-11-2671111',
                'address': 'No. 385, Baddegama Wimalawansa Thero Mawatha, Colombo 10',
                'keywords': 'hospital medical doctor clinic health treatment vaccination',
                'icon': 'heart',
                'color': '#EF4444'
            },
            {
                'name': 'Ministry of Immigration & Emigration',
                'short_name': 'MOIE',
                'description': 'Managing border control, visa services, and passport issuance',
                'minister': 'Hon. Immigration Minister',
                'secretary': 'Secretary of Immigration',
                'website': 'https://www.immigration.gov.lk',
                'contact_email': 'info@immigration.gov.lk',
                'contact_phone': '+94-11-5329000',
                'address': 'Suhurupaya, Battaramulla, Sri Lanka',
                'keywords': 'passport visa travel border immigration emigration',
                'icon': 'passport',
                'color': '#8B5CF6'
            },
            {
                'name': 'Ministry of Transport & Highways',
                'short_name': 'MOTH',
                'description': 'Developing and maintaining Sri Lanka\'s transport infrastructure',
                'minister': 'Hon. Transport Minister',
                'secretary': 'Secretary of Transport',
                'website': 'https://www.transport.gov.lk',
                'contact_email': 'info@transport.gov.lk',
                'contact_phone': '+94-11-2328851',
                'address': 'No. 1, D.R. Wijewardena Mawatha, Colombo 10',
                'keywords': 'driving license vehicle transport road highway bus train',
                'icon': 'car',
                'color': '#F59E0B'
            },
            {
                'name': 'Ministry of Finance',
                'short_name': 'MOF',
                'description': 'Managing national economy, budget, and financial policy',
                'minister': 'Hon. Finance Minister',
                'secretary': 'Secretary of Finance',
                'website': 'https://www.treasury.gov.lk',
                'contact_email': 'info@treasury.gov.lk',
                'contact_phone': '+94-11-2484500',
                'address': 'The Secretariat, Colombo 01, Sri Lanka',
                'keywords': 'tax finance budget economy treasury revenue payment',
                'icon': 'dollar-sign',
                'color': '#059669'
            },
            {
                'name': 'Ministry of Justice',
                'short_name': 'MOJ',
                'description': 'Upholding rule of law and administering justice system',
                'minister': 'Hon. Justice Minister',
                'secretary': 'Secretary of Justice',
                'website': 'https://www.justice.gov.lk',
                'contact_email': 'info@justice.gov.lk',
                'contact_phone': '+94-11-2323936',
                'address': 'Superior Courts Complex, Colombo 12',
                'keywords': 'court law legal justice attorney lawyer case',
                'icon': 'scale',
                'color': '#DC2626'
            },
            {
                'name': 'Ministry of Home Affairs',
                'short_name': 'MOHA',
                'description': 'Managing internal security and administrative services',
                'minister': 'Hon. Home Affairs Minister',
                'secretary': 'Secretary of Home Affairs',
                'website': 'https://www.homeaffairs.gov.lk',
                'contact_email': 'info@homeaffairs.gov.lk',
                'contact_phone': '+94-11-2694211',
                'address': 'Independence Square, Colombo 07',
                'keywords': 'police security ID card birth certificate registration',
                'icon': 'home',
                'color': '#7C3AED'
            },
            {
                'name': 'Ministry of Labour & Employment',
                'short_name': 'MOLE',
                'description': 'Promoting employment opportunities and workers\' rights',
                'minister': 'Hon. Labour Minister',
                'secretary': 'Secretary of Labour',
                'website': 'https://www.labour.gov.lk',
                'contact_email': 'info@labour.gov.lk',
                'contact_phone': '+94-11-2368378',
                'address': 'Labour Secretariat, Colombo 05',
                'keywords': 'job employment work worker EPF ETF labor career',
                'icon': 'briefcase',
                'color': '#0891B2'
            },
            {
                'name': 'Ministry of Agriculture',
                'short_name': 'MOA',
                'description': 'Enhancing agricultural productivity and food security',
                'minister': 'Hon. Agriculture Minister',
                'secretary': 'Secretary of Agriculture',
                'website': 'https://www.agrimin.gov.lk',
                'contact_email': 'info@agrimin.gov.lk',
                'contact_phone': '+94-11-2868421',
                'address': 'Govijana Mandiraya, Rajamalwatta Road, Battaramulla',
                'keywords': 'farming agriculture crop fertilizer subsidy farmer',
                'icon': 'leaf',
                'color': '#84CC16'
            },
            {
                'name': 'Ministry of Trade & Commerce',
                'short_name': 'MOTC',
                'description': 'Facilitating domestic and international trade',
                'minister': 'Hon. Trade Minister',
                'secretary': 'Secretary of Trade',
                'website': 'https://www.trade.gov.lk',
                'contact_email': 'info@trade.gov.lk',
                'contact_phone': '+94-11-2391520',
                'address': 'Rakshana Mandiraya, Colombo 01',
                'keywords': 'business trade export import commerce license permit',
                'icon': 'shopping-cart',
                'color': '#F97316'
            },
            {
                'name': 'Ministry of Housing & Urban Development',
                'short_name': 'MOHUD',
                'description': 'Planning urban development and providing housing solutions',
                'minister': 'Hon. Housing Minister',
                'secretary': 'Secretary of Housing',
                'website': 'https://www.housing.gov.lk',
                'contact_email': 'info@housing.gov.lk',
                'contact_phone': '+94-11-2691211',
                'address': 'Sethsiripaya, Battaramulla',
                'keywords': 'house housing apartment land property development urban',
                'icon': 'building',
                'color': '#6366F1'
            },
            {
                'name': 'Ministry of Environment',
                'short_name': 'MOENV',
                'description': 'Protecting environment and managing natural resources',
                'minister': 'Hon. Environment Minister',
                'secretary': 'Secretary of Environment',
                'website': 'https://www.env.gov.lk',
                'contact_email': 'info@env.gov.lk',
                'contact_phone': '+94-11-2034300',
                'address': 'Sobanadara Mawatha, Battaramulla',
                'keywords': 'environment climate pollution conservation ecology green',
                'icon': 'tree',
                'color': '#22C55E'
            },
            {
                'name': 'Ministry of Tourism',
                'short_name': 'MOT',
                'description': 'Promoting Sri Lanka as a premier tourist destination',
                'minister': 'Hon. Tourism Minister',
                'secretary': 'Secretary of Tourism',
                'website': 'https://www.srilanka.travel',
                'contact_email': 'info@srilanka.travel',
                'contact_phone': '+94-11-2426900',
                'address': 'No. 80, Galle Road, Colombo 03',
                'keywords': 'tourism travel hotel tour guide visa tourist attraction',
                'icon': 'map',
                'color': '#EC4899'
            },
            {
                'name': 'Ministry of Sports',
                'short_name': 'MOS',
                'description': 'Developing sports and youth activities nationwide',
                'minister': 'Hon. Sports Minister',
                'secretary': 'Secretary of Sports',
                'website': 'https://www.sports.gov.lk',
                'contact_email': 'info@sports.gov.lk',
                'contact_phone': '+94-11-2695371',
                'address': 'Independence Avenue, Colombo 07',
                'keywords': 'sports cricket football athlete stadium youth fitness',
                'icon': 'trophy',
                'color': '#F59E0B'
            },
            {
                'name': 'Ministry of Energy',
                'short_name': 'MOEN',
                'description': 'Managing energy resources and power generation',
                'minister': 'Hon. Energy Minister',
                'secretary': 'Secretary of Energy',
                'website': 'https://www.energy.gov.lk',
                'contact_email': 'info@energy.gov.lk',
                'contact_phone': '+94-11-2697722',
                'address': 'BMICH, Bauddhaloka Mawatha, Colombo 07',
                'keywords': 'electricity power energy solar renewable bill CEB',
                'icon': 'zap',
                'color': '#FBBF24'
            },
            {
                'name': 'Ministry of Water Supply',
                'short_name': 'MOWS',
                'description': 'Providing clean water and sanitation services',
                'minister': 'Hon. Water Supply Minister',
                'secretary': 'Secretary of Water Supply',
                'website': 'https://www.waterboard.gov.lk',
                'contact_email': 'info@waterboard.gov.lk',
                'contact_phone': '+94-11-2697722',
                'address': 'Galle Road, Ratmalana',
                'keywords': 'water supply sewage drainage sanitation bill NWSDB',
                'icon': 'droplet',
                'color': '#0EA5E9'
            },
            {
                'name': 'Ministry of Telecommunication',
                'short_name': 'MOTEL',
                'description': 'Regulating telecommunications and digital connectivity',
                'minister': 'Hon. Telecommunication Minister',
                'secretary': 'Secretary of Telecommunication',
                'website': 'https://www.telecom.gov.lk',
                'contact_email': 'info@telecom.gov.lk',
                'contact_phone': '+94-11-2369099',
                'address': 'Lotus Road, Colombo 01',
                'keywords': 'phone mobile internet broadband telecom network 4G 5G',
                'icon': 'phone',
                'color': '#06B6D4'
            },
            {
                'name': 'Ministry of Social Services',
                'short_name': 'MOSS',
                'description': 'Providing social welfare and assistance programs',
                'minister': 'Hon. Social Services Minister',
                'secretary': 'Secretary of Social Services',
                'website': 'https://www.socialservices.gov.lk',
                'contact_email': 'info@socialservices.gov.lk',
                'contact_phone': '+94-11-2697460',
                'address': 'Sethsiripaya, Battaramulla',
                'keywords': 'welfare pension samurdhi assistance elderly disability',
                'icon': 'users',
                'color': '#8B5CF6'
            },
            {
                'name': 'Ministry of Foreign Affairs',
                'short_name': 'MOFA',
                'description': 'Managing international relations and diplomatic missions',
                'minister': 'Hon. Foreign Affairs Minister',
                'secretary': 'Secretary of Foreign Affairs',
                'website': 'https://www.mfa.gov.lk',
                'contact_email': 'info@mfa.gov.lk',
                'contact_phone': '+94-11-2325371',
                'address': 'Republic Building, Colombo 01',
                'keywords': 'embassy consulate visa diplomatic foreign travel international',
                'icon': 'globe',
                'color': '#14B8A6'
            },
            {
                'name': 'Ministry of Defense',
                'short_name': 'MOD',
                'description': 'Ensuring national security and defense',
                'minister': 'Hon. Defense Minister',
                'secretary': 'Secretary of Defense',
                'website': 'https://www.defence.lk',
                'contact_email': 'info@defence.lk',
                'contact_phone': '+94-11-2430860',
                'address': '15/5, Baladaksha Mawatha, Colombo 03',
                'keywords': 'defense security army navy air force military national',
                'icon': 'shield',
                'color': '#991B1B'
            },
            {
                'name': 'Ministry of Women & Child Affairs',
                'short_name': 'MOWCA',
                'description': 'Protecting rights and welfare of women and children',
                'minister': 'Hon. Women & Child Affairs Minister',
                'secretary': 'Secretary of Women & Child Affairs',
                'website': 'https://www.childwomenmin.gov.lk',
                'contact_email': 'info@childwomenmin.gov.lk',
                'contact_phone': '+94-11-2694184',
                'address': '177/1, Nawala Road, Koswatte',
                'keywords': 'women child children protection rights welfare family mother',
                'icon': 'heart',
                'color': '#DB2777'
            }
        ]
        
        # Insert ministries and get their IDs
        ministry_ids = {}
        for ministry in ministries_data:
            ministry['created_at'] = datetime.utcnow()
            ministry['updated_at'] = datetime.utcnow()
            ministry['view_count'] = 0
            result = ministries_collection.insert_one(ministry)
            ministry_ids[ministry['name']] = str(result.inserted_id)
            print(f"  ✓ Created: {ministry['name']}")
        
        print(f"\n✅ Created {len(ministry_ids)} ministries")
        print("\n🔄 Creating subservices with FAQs, downloads, and locations...")
        
        # Define subservices for each ministry with comprehensive data
        subservices_data = [
            # IT & Digital Affairs Subservices
            {
                'ministry_id': ministry_ids['Ministry of IT & Digital Affairs'],
                'name': 'IT Certificate Issuance',
                'description': 'Obtain official IT certification for professionals and students',
                'category': 'Certification',
                'keywords': 'IT certificate certification professional tech',
                'requirements': [
                    'Completed IT course certificate',
                    'National Identity Card',
                    'Passport-sized photographs (2)',
                    'Application fee receipt'
                ],
                'step_by_step': [
                    'Visit MITDA online portal or nearest office',
                    'Fill out IT certificate application form',
                    'Upload required documents',
                    'Pay application fee (LKR 1,500)',
                    'Submit application online or in person',
                    'Receive certificate within 14 working days'
                ],
                'faqs': [
                    {
                        'question': 'How long does it take to get an IT certificate?',
                        'answer': 'IT certificates are typically issued within 14 working days after submission of complete documentation and payment.'
                    },
                    {
                        'question': 'What is the validity period of the IT certificate?',
                        'answer': 'IT certificates are valid for 5 years from the date of issuance. Renewal can be done 3 months before expiry.'
                    },
                    {
                        'question': 'Can I apply for an IT certificate online?',
                        'answer': 'Yes, you can apply online through the MITDA portal at https://www.mitda.gov.lk/certificates. You will need to create an account and upload scanned documents.'
                    },
                    {
                        'question': 'What is the application fee for IT certificate?',
                        'answer': 'The application fee is LKR 1,500 for standard processing. Express processing (7 days) is available for LKR 3,000.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'IT Certificate Application Form',
                        'file_name': 'IT_Certificate_Application_Form.pdf',
                        'file_url': '/downloads/it/IT_Certificate_Application_Form.pdf',
                        'file_size': '245 KB',
                        'description': 'Official application form for IT certificate issuance'
                    },
                    {
                        'title': 'Required Documents Checklist',
                        'file_name': 'IT_Certificate_Documents_Checklist.pdf',
                        'file_url': '/downloads/it/IT_Certificate_Documents_Checklist.pdf',
                        'file_size': '128 KB',
                        'description': 'Complete checklist of required documents'
                    },
                    {
                        'title': 'IT Certificate Guidelines',
                        'file_name': 'IT_Certificate_Guidelines.pdf',
                        'file_url': '/downloads/it/IT_Certificate_Guidelines.pdf',
                        'file_size': '512 KB',
                        'description': 'Comprehensive guidelines for IT certification process'
                    }
                ],
                'locations': [
                    {
                        'name': 'MITDA Head Office - Colombo',
                        'address': 'IT Tower, Galle Road, Colombo 07',
                        'phone': '+94-11-2345678',
                        'email': 'certificates@mitda.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8612',
                        'latitude': 6.9147,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:30 AM - 4:00 PM'
                    },
                    {
                        'name': 'MITDA Regional Office - Kandy',
                        'address': 'Digital Centre, Peradeniya Road, Kandy',
                        'phone': '+94-81-2223344',
                        'email': 'kandy@mitda.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=7.2906,80.6337',
                        'latitude': 7.2906,
                        'longitude': 80.6337,
                        'working_hours': 'Monday to Friday: 9:00 AM - 3:30 PM'
                    }
                ],
                'processing_time': '14 working days',
                'fees': 'LKR 1,500 (Standard), LKR 3,000 (Express)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'certificates@mitda.gov.lk',
                    'working_hours': '24/7 for online, Office hours: 8:30 AM - 4:00 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of IT & Digital Affairs'],
                'name': 'Cyber Security Certification',
                'description': 'Professional certification for cybersecurity professionals',
                'category': 'Certification',
                'keywords': 'cyber security certification hacking network',
                'requirements': [
                    'Relevant IT degree or diploma',
                    'Minimum 2 years experience in IT security',
                    'National Identity Card',
                    'Professional references (2)'
                ],
                'step_by_step': [
                    'Register on MITDA certification portal',
                    'Complete online application form',
                    'Upload educational certificates and experience letters',
                    'Pay examination fee (LKR 5,000)',
                    'Schedule certification exam',
                    'Pass written and practical examinations',
                    'Receive certification within 7 days of passing'
                ],
                'faqs': [
                    {
                        'question': 'What are the exam requirements for cyber security certification?',
                        'answer': 'The exam consists of a written test (3 hours) covering security fundamentals, networking, and threat analysis, plus a practical lab test (2 hours) demonstrating security tools proficiency.'
                    },
                    {
                        'question': 'Is work experience mandatory for this certification?',
                        'answer': 'Yes, a minimum of 2 years of verifiable experience in IT security or related field is required to apply for the certification exam.'
                    },
                    {
                        'question': 'How often can I retake the exam if I fail?',
                        'answer': 'You can retake the exam after 30 days. Maximum of 3 attempts per year is allowed. Each retake requires payment of the exam fee.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Cyber Security Exam Syllabus',
                        'file_name': 'Cyber_Security_Syllabus.pdf',
                        'file_url': '/downloads/it/Cyber_Security_Syllabus.pdf',
                        'file_size': '892 KB',
                        'description': 'Detailed syllabus for cyber security certification exam'
                    }
                ],
                'locations': [
                    {
                        'name': 'MITDA Examination Center - Colombo',
                        'address': 'IT Tower, Galle Road, Colombo 07',
                        'phone': '+94-11-2345680',
                        'email': 'exams@mitda.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8612',
                        'latitude': 6.9147,
                        'longitude': 79.8612,
                        'working_hours': 'Exam sessions: Monday, Wednesday, Friday 9:00 AM & 2:00 PM'
                    }
                ],
                'processing_time': '7 working days after passing exam',
                'fees': 'LKR 5,000 (Exam fee)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'exams@mitda.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 4:00 PM'
                }
            },
            
            # Education Subservices
            {
                'ministry_id': ministry_ids['Ministry of Education'],
                'name': 'School Registration',
                'description': 'Register children for admission to government schools',
                'category': 'Registration',
                'keywords': 'school admission registration student child enrollment',
                'requirements': [
                    'Child\'s Birth Certificate (certified copy)',
                    'Parent/Guardian National Identity Card',
                    'Proof of residence (utility bill or Grama Niladhari certificate)',
                    'Immunization record card',
                    'Two passport-sized photographs of child'
                ],
                'step_by_step': [
                    'Visit the school or Zonal Education Office',
                    'Collect school registration form',
                    'Fill form with accurate information',
                    'Attach required documents',
                    'Submit application during registration period',
                    'Await confirmation from school/ZEO',
                    'Complete admission process if selected'
                ],
                'faqs': [
                    {
                        'question': 'What is the age requirement for Grade 1 admission?',
                        'answer': 'Children must be 5 years old as of January 1st of the admission year. Age will be verified using the birth certificate.'
                    },
                    {
                        'question': 'When does school registration usually take place?',
                        'answer': 'School registration for Grade 1 typically opens in September/October for admission in January of the following year. Exact dates are announced by the Ministry annually.'
                    },
                    {
                        'question': 'Can I register my child at multiple schools?',
                        'answer': 'Yes, you can apply to up to 3 schools in order of preference. However, final admission will be to only one school based on the selection criteria.'
                    },
                    {
                        'question': 'What is the distance criterion for school admission?',
                        'answer': 'Schools typically prioritize children living within 1-2 km radius. Proof of residence within this distance significantly increases admission chances.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'School Registration Form - Grade 1',
                        'file_name': 'School_Registration_Grade1.pdf',
                        'file_url': '/downloads/education/School_Registration_Grade1.pdf',
                        'file_size': '156 KB',
                        'description': 'Official registration form for Grade 1 admission'
                    },
                    {
                        'title': 'Documents Required Checklist',
                        'file_name': 'School_Admission_Documents.pdf',
                        'file_url': '/downloads/education/School_Admission_Documents.pdf',
                        'file_size': '98 KB',
                        'description': 'Complete list of documents required for registration'
                    },
                    {
                        'title': 'School Admission Guidelines 2025',
                        'file_name': 'Admission_Guidelines_2025.pdf',
                        'file_url': '/downloads/education/Admission_Guidelines_2025.pdf',
                        'file_size': '742 KB',
                        'description': 'Comprehensive guidelines for school admission process'
                    }
                ],
                'locations': [
                    {
                        'name': 'Ministry of Education - Head Office',
                        'address': 'Isurupaya, Battaramulla, Sri Lanka',
                        'phone': '+94-11-2369874',
                        'email': 'info@moe.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9034,79.9185',
                        'latitude': 6.9034,
                        'longitude': 79.9185,
                        'working_hours': 'Monday to Friday: 8:30 AM - 4:15 PM'
                    },
                    {
                        'name': 'Zonal Education Office - Colombo',
                        'address': 'Felix Dias Bandaranaike Mawatha, Colombo 08',
                        'phone': '+94-11-2695279',
                        'email': 'zeo.colombo@moe.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8612',
                        'latitude': 6.9147,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:30 AM - 4:00 PM'
                    }
                ],
                'processing_time': '30-45 days (selection notification)',
                'fees': 'Free of charge',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'admissions@moe.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 4:15 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Education'],
                'name': 'University Admission',
                'description': 'Apply for university admission through UGC',
                'category': 'Higher Education',
                'keywords': 'university admission UGC higher education degree AL',
                'requirements': [
                    'G.C.E. Advanced Level examination results sheet',
                    'National Identity Card',
                    'Birth Certificate (certified copy)',
                    'School leaving certificate',
                    'Character certificate from school principal'
                ],
                'step_by_step': [
                    'Obtain A/L examination results',
                    'Register on UGC online application portal',
                    'Fill application form with course preferences',
                    'Upload required documents',
                    'Submit application before deadline',
                    'Check Z-Score and selection results',
                    'Accept admission offer and register at university'
                ],
                'faqs': [
                    {
                        'question': 'What is the minimum Z-Score required for university admission?',
                        'answer': 'The minimum Z-Score varies by course and university, typically ranging from 1.0 to 2.5. Highly competitive courses like Medicine and Engineering require Z-scores above 2.0.'
                    },
                    {
                        'question': 'How many course preferences can I select?',
                        'answer': 'You can select up to 20 course preferences in order of priority. You will be admitted to the highest preference course for which you qualify based on Z-Score.'
                    },
                    {
                        'question': 'Can I defer my university admission?',
                        'answer': 'Yes, deferment is possible for valid reasons (medical, family circumstances). You must apply for deferment through the relevant university within 14 days of admission offer.'
                    },
                    {
                        'question': 'When does the university admission application process start?',
                        'answer': 'Applications typically open 2-3 months after A/L results are released, usually around March/April. The UGC publishes the exact schedule annually.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'UGC Handbook for University Admission',
                        'file_name': 'UGC_Admission_Handbook.pdf',
                        'file_url': '/downloads/education/UGC_Admission_Handbook.pdf',
                        'file_size': '1.2 MB',
                        'description': 'Complete guide to university admission process'
                    },
                    {
                        'title': 'Course Details and Requirements',
                        'file_name': 'University_Courses_Guide.pdf',
                        'file_url': '/downloads/education/University_Courses_Guide.pdf',
                        'file_size': '2.5 MB',
                        'description': 'Detailed information about all university courses and entry requirements'
                    }
                ],
                'locations': [
                    {
                        'name': 'University Grants Commission',
                        'address': 'No. 20, Ward Place, Colombo 07',
                        'phone': '+94-11-2695301',
                        'email': 'info@ugc.ac.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8612',
                        'latitude': 6.9147,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:30 AM - 4:15 PM'
                    }
                ],
                'processing_time': '45-60 days (selection results)',
                'fees': 'Free of charge',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'admissions@ugc.ac.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 4:15 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Education'],
                'name': 'Exam Results Verification',
                'description': 'Obtain certified copies of examination results',
                'category': 'Certification',
                'keywords': 'exam results certificate OL AL verification',
                'requirements': [
                    'Original examination results sheet',
                    'National Identity Card',
                    'Application form',
                    'Certification fee payment receipt'
                ],
                'step_by_step': [
                    'Visit Department of Examinations office',
                    'Collect verification application form',
                    'Fill form with examination details',
                    'Submit original results sheet for verification',
                    'Pay certification fee (LKR 500)',
                    'Collect certified copy within 7 working days'
                ],
                'faqs': [
                    {
                        'question': 'How can I get a certified copy of my old examination results?',
                        'answer': 'Visit the Department of Examinations with your index number and NIC. If you don\'t have the original, request a duplicate certificate with proper documentation.'
                    },
                    {
                        'question': 'How long does it take to get exam result verification?',
                        'answer': 'Standard verification takes 7 working days. Express service (3 days) is available for an additional fee of LKR 1,000.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Results Verification Application Form',
                        'file_name': 'Results_Verification_Form.pdf',
                        'file_url': '/downloads/education/Results_Verification_Form.pdf',
                        'file_size': '142 KB',
                        'description': 'Application form for exam results certification'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Examinations - Colombo',
                        'address': 'Pelawatta, Battaramulla',
                        'phone': '+94-11-2785141',
                        'email': 'info@exams.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.8923,79.9185',
                        'latitude': 6.8923,
                        'longitude': 79.9185,
                        'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                    }
                ],
                'processing_time': '7 working days',
                'fees': 'LKR 500 (Standard), LKR 1,500 (Express)',
                'contact_info': {
                    'hotline': '0112-777777',
                    'email': 'info@exams.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                }
            },
            
            # Health Subservices
            {
                'ministry_id': ministry_ids['Ministry of Health'],
                'name': 'Birth/Death Certificate from Hospital',
                'description': 'Obtain birth or death certificates issued by hospitals',
                'category': 'Civil Registration',
                'keywords': 'birth death certificate hospital registration',
                'requirements': [
                    'Hospital admission records',
                    'Parent/Next of kin National Identity Card',
                    'Marriage certificate (for birth certificate)',
                    'Medical report (for death certificate)'
                ],
                'step_by_step': [
                    'Visit hospital medical records office',
                    'Request birth/death certificate application form',
                    'Fill form with accurate details',
                    'Submit required identification documents',
                    'Pay certificate fee (LKR 200)',
                    'Receive certificate within 3 working days'
                ],
                'faqs': [
                    {
                        'question': 'How soon after birth can I get a birth certificate?',
                        'answer': 'The hospital issues a notification of birth immediately. The official birth certificate can be obtained from the hospital within 7 days or from the Registrar of Births within 30 days.'
                    },
                    {
                        'question': 'Can I get a duplicate death certificate?',
                        'answer': 'Yes, duplicates can be issued by the hospital where death occurred or by the Registrar General\'s Department with proper identification and fee payment.'
                    },
                    {
                        'question': 'Is there a time limit for registering a birth?',
                        'answer': 'Births should be registered within 42 days. Late registration (after 42 days) requires additional documentation and approval from the Registrar.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Birth Certificate Application Form',
                        'file_name': 'Birth_Certificate_Form.pdf',
                        'file_url': '/downloads/health/Birth_Certificate_Form.pdf',
                        'file_size': '178 KB',
                        'description': 'Application form for hospital birth certificate'
                    },
                    {
                        'title': 'Death Certificate Application Form',
                        'file_name': 'Death_Certificate_Form.pdf',
                        'file_url': '/downloads/health/Death_Certificate_Form.pdf',
                        'file_size': '165 KB',
                        'description': 'Application form for death certificate'
                    }
                ],
                'locations': [
                    {
                        'name': 'National Hospital of Sri Lanka',
                        'address': 'Regent Street, Colombo 10',
                        'phone': '+94-11-2691111',
                        'email': 'nhsl@health.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9271,79.8612',
                        'latitude': 6.9271,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    },
                    {
                        'name': 'Lady Ridgeway Hospital',
                        'address': 'Dr. Danister De Silva Mawatha, Colombo 08',
                        'phone': '+94-11-2693711',
                        'email': 'lrh@health.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8612',
                        'latitude': 6.9147,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    }
                ],
                'processing_time': '3 working days',
                'fees': 'LKR 200',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'certificates@health.gov.lk',
                    'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Health'],
                'name': 'Medical Fitness Certificate',
                'description': 'Obtain medical fitness certificates for employment, education, or travel',
                'category': 'Health Services',
                'keywords': 'medical fitness certificate health check doctor',
                'requirements': [
                    'National Identity Card',
                    'Recent passport-sized photograph',
                    'Medical examination fee',
                    'Previous medical records (if any)'
                ],
                'step_by_step': [
                    'Visit government hospital or MOH office',
                    'Register at OPD for medical examination',
                    'Undergo medical examination by doctor',
                    'Complete necessary lab tests if required',
                    'Pay certificate fee (LKR 500)',
                    'Collect medical fitness certificate'
                ],
                'faqs': [
                    {
                        'question': 'What tests are included in medical fitness examination?',
                        'answer': 'Standard examination includes vital signs check, general physical examination, vision and hearing tests. Additional tests may be required based on the purpose (employment, visa, etc.).'
                    },
                    {
                        'question': 'How long is a medical fitness certificate valid?',
                        'answer': 'Typically valid for 3-6 months depending on the purpose. For employment, usually 6 months. For visa applications, check specific country requirements.'
                    },
                    {
                        'question': 'Can I get a medical fitness certificate the same day?',
                        'answer': 'If no additional tests are needed, certificates can be issued the same day. If lab tests are required, it may take 2-3 working days.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Medical Fitness Certificate Application',
                        'file_name': 'Medical_Fitness_Application.pdf',
                        'file_url': '/downloads/health/Medical_Fitness_Application.pdf',
                        'file_size': '134 KB',
                        'description': 'Application form for medical fitness certificate'
                    }
                ],
                'locations': [
                    {
                        'name': 'National Hospital - Medical Certificates',
                        'address': 'Regent Street, Colombo 10',
                        'phone': '+94-11-2691111',
                        'email': 'nhsl@health.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9271,79.8612',
                        'latitude': 6.9271,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:00 AM - 12:00 PM'
                    }
                ],
                'processing_time': 'Same day to 3 working days',
                'fees': 'LKR 500',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'medical.certificates@health.gov.lk',
                    'working_hours': 'Monday to Friday: 8:00 AM - 4:00 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Health'],
                'name': 'Vaccination Services',
                'description': 'Access routine and travel vaccination programs',
                'category': 'Preventive Health',
                'keywords': 'vaccine vaccination immunization covid travel health',
                'requirements': [
                    'National Identity Card or Birth Certificate',
                    'Vaccination card (if previously vaccinated)',
                    'For children: Parent/Guardian NIC'
                ],
                'step_by_step': [
                    'Visit nearest MOH office or vaccination center',
                    'Register at vaccination counter',
                    'Present vaccination card or health record',
                    'Receive required vaccine(s)',
                    'Get vaccination details recorded in card',
                    'Receive next appointment date if follow-up needed'
                ],
                'faqs': [
                    {
                        'question': 'Are vaccinations free in government hospitals?',
                        'answer': 'Yes, all routine vaccinations in the national immunization program are provided free of charge at government hospitals and MOH offices.'
                    },
                    {
                        'question': 'What vaccinations do I need for international travel?',
                        'answer': 'Travel vaccination requirements vary by destination. Common travel vaccines include Yellow Fever, Hepatitis A/B, Typhoid, and COVID-19. Consult the travel medicine clinic at least 6 weeks before travel.'
                    },
                    {
                        'question': 'Can adults get vaccinated at government facilities?',
                        'answer': 'Yes, adult vaccinations including COVID-19, Influenza, and Tetanus boosters are available. Some vaccines may have a nominal charge.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'National Immunization Schedule',
                        'file_name': 'Immunization_Schedule.pdf',
                        'file_url': '/downloads/health/Immunization_Schedule.pdf',
                        'file_size': '456 KB',
                        'description': 'Complete schedule for childhood and adult vaccinations'
                    },
                    {
                        'title': 'Travel Vaccination Guide',
                        'file_name': 'Travel_Vaccination_Guide.pdf',
                        'file_url': '/downloads/health/Travel_Vaccination_Guide.pdf',
                        'file_size': '623 KB',
                        'description': 'Guide to vaccinations required for international travel'
                    }
                ],
                'locations': [
                    {
                        'name': 'Epidemiology Unit - Travel Medicine',
                        'address': '231, De Saram Place, Colombo 10',
                        'phone': '+94-11-2695112',
                        'email': 'travel.clinic@health.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9271,79.8612',
                        'latitude': 6.9271,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    }
                ],
                'processing_time': 'Immediate (walk-in service)',
                'fees': 'Free for routine vaccines; Travel vaccines: LKR 500-2,000',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'immunization@health.gov.lk',
                    'working_hours': '24/7 for emergencies'
                }
            },
            
            # Immigration Subservices
            {
                'ministry_id': ministry_ids['Ministry of Immigration & Emigration'],
                'name': 'Passport Application/Renewal',
                'description': 'Apply for new passport or renew existing passport',
                'category': 'Travel Documents',
                'keywords': 'passport travel visa immigration document renewal',
                'requirements': [
                    'Birth Certificate (certified copy)',
                    'National Identity Card',
                    'Two recent passport-sized photographs',
                    'Previous passport (for renewal)',
                    'Proof of residence'
                ],
                'step_by_step': [
                    'Book appointment online at www.immigration.gov.lk',
                    'Visit Divisional Secretariat or passport office',
                    'Submit completed application form',
                    'Provide biometric data (fingerprints, photo)',
                    'Pay passport fee',
                    'Receive acknowledgment receipt',
                    'Collect passport after 10 working days'
                ],
                'faqs': [
                    {
                        'question': 'How long does it take to get a passport?',
                        'answer': 'Standard processing is 10 working days. Fast-track service (3 working days) and express service (1 working day) are available at additional cost.'
                    },
                    {
                        'question': 'Can I renew my passport if it has already expired?',
                        'answer': 'Yes, expired passports can be renewed. You need to submit the expired passport along with current documents. The process is the same as renewal of a valid passport.'
                    },
                    {
                        'question': 'What are the passport fees?',
                        'answer': 'Standard 32-page passport: LKR 5,000 (10 days), LKR 10,000 (3 days), LKR 15,000 (1 day). 64-page passport available at higher fees.'
                    },
                    {
                        'question': 'Can I apply for a passport for my child?',
                        'answer': 'Yes, both parents must be present with the child. Required documents include child\'s birth certificate, parents\' NICs and passports, and child\'s recent photographs.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Passport Application Form',
                        'file_name': 'Passport_Application_Form.pdf',
                        'file_url': '/downloads/immigration/Passport_Application_Form.pdf',
                        'file_size': '289 KB',
                        'description': 'Official passport application form'
                    },
                    {
                        'title': 'Passport Photo Guidelines',
                        'file_name': 'Passport_Photo_Guidelines.pdf',
                        'file_url': '/downloads/immigration/Passport_Photo_Guidelines.pdf',
                        'file_size': '445 KB',
                        'description': 'Specifications for passport photographs'
                    },
                    {
                        'title': 'Document Checklist',
                        'file_name': 'Passport_Documents_Checklist.pdf',
                        'file_url': '/downloads/immigration/Passport_Documents_Checklist.pdf',
                        'file_size': '156 KB',
                        'description': 'Complete checklist of required documents'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Immigration - Head Office',
                        'address': 'Suhurupaya, Battaramulla',
                        'phone': '+94-11-5329000',
                        'email': 'info@immigration.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9034,79.9185',
                        'latitude': 6.9034,
                        'longitude': 79.9185,
                        'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                    },
                    {
                        'name': 'Regional Passport Office - Kandy',
                        'address': 'Kings Pavilion, Kandy',
                        'phone': '+94-81-2223366',
                        'email': 'kandy@immigration.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=7.2906,80.6337',
                        'latitude': 7.2906,
                        'longitude': 80.6337,
                        'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                    }
                ],
                'processing_time': '10 working days (Standard)',
                'fees': 'LKR 5,000 - 15,000 (depending on processing time)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'passport@immigration.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Immigration & Emigration'],
                'name': 'Visa Application',
                'description': 'Apply for various types of visas for visitors to Sri Lanka',
                'category': 'Travel Documents',
                'keywords': 'visa tourist business visit ETA travel',
                'requirements': [
                    'Valid passport (minimum 6 months validity)',
                    'Passport-sized photograph',
                    'Proof of accommodation in Sri Lanka',
                    'Return/onward ticket',
                    'Financial proof',
                    'Purpose of visit documentation'
                ],
                'step_by_step': [
                    'Apply online at www.eta.gov.lk',
                    'Select visa type (Tourist/Business/Transit)',
                    'Fill online application form',
                    'Upload required documents',
                    'Pay visa fee online',
                    'Receive ETA approval via email',
                    'Print ETA and carry during travel'
                ],
                'faqs': [
                    {
                        'question': 'Do I need a visa to visit Sri Lanka?',
                        'answer': 'Most nationalities require an Electronic Travel Authorization (ETA). Citizens of Singapore and Maldives are exempt. Check www.eta.gov.lk for specific country requirements.'
                    },
                    {
                        'question': 'How long does it take to get an ETA?',
                        'answer': 'ETAs are typically approved within 24 hours of application. It is recommended to apply at least 3 days before travel.'
                    },
                    {
                        'question': 'Can I extend my tourist visa while in Sri Lanka?',
                        'answer': 'Yes, tourist visas can be extended up to 6 months. Apply at the Department of Immigration with passport, ETA, proof of funds, and extension fee (USD 35 per month).'
                    },
                    {
                        'question': 'What is the difference between tourist and business visa?',
                        'answer': 'Tourist visa is for leisure travel (30 days, extendable). Business visa is for business meetings, conferences (30 days, multiple entry possible). Requirements and fees differ.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'ETA Application Guide',
                        'file_name': 'ETA_Application_Guide.pdf',
                        'file_url': '/downloads/immigration/ETA_Application_Guide.pdf',
                        'file_size': '678 KB',
                        'description': 'Step-by-step guide for online ETA application'
                    },
                    {
                        'title': 'Visa Extension Application Form',
                        'file_name': 'Visa_Extension_Form.pdf',
                        'file_url': '/downloads/immigration/Visa_Extension_Form.pdf',
                        'file_size': '234 KB',
                        'description': 'Form for visa extension application'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Immigration - Visa Section',
                        'address': 'Suhurupaya, Battaramulla',
                        'phone': '+94-11-5329000',
                        'email': 'visa@immigration.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9034,79.9185',
                        'latitude': 6.9034,
                        'longitude': 79.9185,
                        'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                    }
                ],
                'processing_time': '24 hours (online ETA)',
                'fees': 'USD 20-100 (varies by visa type and nationality)',
                'contact_info': {
                    'hotline': '+94-11-5329000',
                    'email': 'visa@immigration.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                }
            },
            
            # Transport Subservices
            {
                'ministry_id': ministry_ids['Ministry of Transport & Highways'],
                'name': 'Driving License Application',
                'description': 'Apply for new driving license or license renewal',
                'category': 'Vehicle Services',
                'keywords': 'driving license vehicle car motorcycle learner permit',
                'requirements': [
                    'Medical fitness certificate',
                    'National Identity Card',
                    'Completed application form',
                    'Eye test report',
                    'Passport-sized photographs (3)',
                    'Learner\'s permit (for full license)'
                ],
                'step_by_step': [
                    'Obtain medical fitness certificate',
                    'Visit nearest Motor Traffic Office',
                    'Submit application with documents',
                    'Complete eye test at office',
                    'Pay application fee',
                    'Attend driving lessons (minimum 40 hours)',
                    'Pass written and practical driving tests',
                    'Receive driving license'
                ],
                'faqs': [
                    {
                        'question': 'What is the minimum age to apply for a driving license?',
                        'answer': 'Minimum age is 18 years for motorcycles and light vehicles. For heavy vehicles and passenger transport, minimum age is 20-22 years depending on category.'
                    },
                    {
                        'question': 'How long is a driving license valid?',
                        'answer': 'Driving licenses are typically valid for 5 years for regular categories and 3 years for commercial categories. Renewal must be done before expiry.'
                    },
                    {
                        'question': 'Can I convert my foreign driving license?',
                        'answer': 'Foreign driving licenses can be converted if you have permanent residence. Process involves document verification, eye test, and payment of conversion fee (LKR 1,500).'
                    },
                    {
                        'question': 'How many times can I attempt the driving test?',
                        'answer': 'You can attempt the test 3 times. After 3 failures, you must reapply for a learner\'s permit and complete the process from the beginning.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Driving License Application Form',
                        'file_name': 'Driving_License_Application.pdf',
                        'file_url': '/downloads/transport/Driving_License_Application.pdf',
                        'file_size': '245 KB',
                        'description': 'Official application form for driving license'
                    },
                    {
                        'title': 'Driving Test Guidelines',
                        'file_name': 'Driving_Test_Guidelines.pdf',
                        'file_url': '/downloads/transport/Driving_Test_Guidelines.pdf',
                        'file_size': '1.1 MB',
                        'description': 'Complete guide to written and practical tests'
                    },
                    {
                        'title': 'Medical Certificate for Driving',
                        'file_name': 'Driving_Medical_Certificate.pdf',
                        'file_url': '/downloads/transport/Driving_Medical_Certificate.pdf',
                        'file_size': '167 KB',
                        'description': 'Medical fitness certificate format for driving license'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Motor Traffic - Colombo',
                        'address': 'Werahera, Borella, Colombo',
                        'phone': '+94-11-2729444',
                        'email': 'info@motortraffic.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8779',
                        'latitude': 6.9147,
                        'longitude': 79.8779,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    },
                    {
                        'name': 'Motor Traffic Office - Kandy',
                        'address': 'Peradeniya Road, Kandy',
                        'phone': '+94-81-2222443',
                        'email': 'kandy@motortraffic.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=7.2906,80.6337',
                        'latitude': 7.2906,
                        'longitude': 80.6337,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    }
                ],
                'processing_time': '30-45 days (including lessons and tests)',
                'fees': 'LKR 2,500 (application + tests)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'license@motortraffic.gov.lk',
                    'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                }
            },
            {
                'ministry_id': ministry_ids['Ministry of Transport & Highways'],
                'name': 'Vehicle Registration',
                'description': 'Register new or used vehicles',
                'category': 'Vehicle Services',
                'keywords': 'vehicle registration car motorcycle ownership transfer',
                'requirements': [
                    'Invoice/Bill of sale',
                    'Import permit (for imported vehicles)',
                    'Insurance certificate',
                    'Emission test certificate',
                    'National Identity Card of owner',
                    'Revenue license fee payment'
                ],
                'step_by_step': [
                    'Complete vehicle inspection at authorized center',
                    'Obtain emission test certificate',
                    'Get vehicle insurance',
                    'Visit Motor Traffic Department',
                    'Submit all required documents',
                    'Pay registration and revenue license fees',
                    'Receive vehicle registration certificate and number plates'
                ],
                'faqs': [
                    {
                        'question': 'How much does vehicle registration cost?',
                        'answer': 'Registration fees vary by vehicle type and engine capacity. Motorcycles: LKR 5,000-10,000, Cars: LKR 15,000-50,000. Plus annual revenue license fees.'
                    },
                    {
                        'question': 'Can I transfer vehicle ownership?',
                        'answer': 'Yes, both buyer and seller must visit Motor Traffic Office with vehicle, original registration, NICs, and transfer documents. Transfer fee is approximately LKR 2,500.'
                    },
                    {
                        'question': 'Do I need to renew vehicle registration annually?',
                        'answer': 'The registration is permanent, but revenue license must be renewed annually. Insurance must also be renewed annually and is mandatory for registration renewal.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'Vehicle Registration Form',
                        'file_name': 'Vehicle_Registration_Form.pdf',
                        'file_url': '/downloads/transport/Vehicle_Registration_Form.pdf',
                        'file_size': '198 KB',
                        'description': 'Application form for new vehicle registration'
                    },
                    {
                        'title': 'Ownership Transfer Form',
                        'file_name': 'Ownership_Transfer_Form.pdf',
                        'file_url': '/downloads/transport/Ownership_Transfer_Form.pdf',
                        'file_size': '176 KB',
                        'description': 'Form for vehicle ownership transfer'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Motor Traffic - Registration',
                        'address': 'Werahera, Borella, Colombo',
                        'phone': '+94-11-2729444',
                        'email': 'registration@motortraffic.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9147,79.8779',
                        'latitude': 6.9147,
                        'longitude': 79.8779,
                        'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                    }
                ],
                'processing_time': '7 working days',
                'fees': 'LKR 15,000-50,000 (varies by vehicle type)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'registration@motortraffic.gov.lk',
                    'working_hours': 'Monday to Friday: 8:00 AM - 3:00 PM'
                }
            },
            
            # Finance Subservices
            {
                'ministry_id': ministry_ids['Ministry of Finance'],
                'name': 'Tax Identification Number (TIN)',
                'description': 'Obtain Tax Identification Number for tax purposes',
                'category': 'Taxation',
                'keywords': 'TIN tax identification number income tax registration',
                'requirements': [
                    'National Identity Card',
                    'Business Registration Certificate (if applicable)',
                    'Proof of address',
                    'Completed application form'
                ],
                'step_by_step': [
                    'Visit nearest Inland Revenue office',
                    'Collect TIN application form',
                    'Fill form with accurate information',
                    'Submit form with required documents',
                    'Receive TIN certificate within 7 days'
                ],
                'faqs': [
                    {
                        'question': 'Who needs a TIN?',
                        'answer': 'Anyone earning taxable income, business owners, self-employed individuals, and those required to file tax returns must have a TIN.'
                    },
                    {
                        'question': 'Is there a fee for obtaining TIN?',
                        'answer': 'No, TIN registration is free of charge for individuals and businesses.'
                    },
                    {
                        'question': 'Can I apply for TIN online?',
                        'answer': 'Yes, you can apply online through the Inland Revenue Department website at www.ird.gov.lk. Online applications are processed within 3 working days.'
                    }
                ],
                'downloads': [
                    {
                        'title': 'TIN Application Form',
                        'file_name': 'TIN_Application_Form.pdf',
                        'file_url': '/downloads/finance/TIN_Application_Form.pdf',
                        'file_size': '187 KB',
                        'description': 'Application form for Tax Identification Number'
                    }
                ],
                'locations': [
                    {
                        'name': 'Inland Revenue Department - Head Office',
                        'address': 'Sir Chittampalam A. Gardiner Mawatha, Colombo 02',
                        'phone': '+94-11-2427582',
                        'email': 'info@ird.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9271,79.8612',
                        'latitude': 6.9271,
                        'longitude': 79.8612,
                        'working_hours': 'Monday to Friday: 8:30 AM - 4:00 PM'
                    }
                ],
                'processing_time': '7 working days',
                'fees': 'Free',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'tin@ird.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 4:00 PM'
                }
            },
            
            # Home Affairs
            {
                'ministry_id': ministry_ids['Ministry of Home Affairs'],
                'name': 'National Identity Card',
                'description': 'Apply for or renew National Identity Card',
                'category': 'Civil Registration',
                'keywords': 'NIC identity card ID national registration',
                'requirements': [
                    'Birth Certificate (certified copy)',
                    'Grama Niladhari certificate',
                    'Passport-sized photographs (2)',
                    'Previous NIC (for renewal)'
                ],
                'step_by_step': [
                    'Visit Divisional Secretariat',
                    'Collect NIC application form',
                    'Fill form with accurate details',
                    'Submit form with required documents',
                    'Provide biometric data',
                    'Pay application fee (LKR 150)',
                    'Receive NIC within 30 days'
                ],
                'faqs': [
                    {
                        'question': 'At what age can I get my first NIC?',
                        'answer': 'You can apply for your first NIC at age 16. It becomes mandatory at age 18 for voting and legal purposes.'
                    },
                    {
                        'question': 'How do I replace a lost NIC?',
                        'answer': 'Report loss to police, obtain police report, visit Divisional Secretariat with police report and birth certificate, pay replacement fee (LKR 500), receive duplicate NIC within 14 days.'
                    },
                    {
                        'question': 'Can I update my address on NIC?',
                        'answer': 'Yes, address changes can be updated by visiting your Divisional Secretariat with proof of new address (utility bill or Grama Niladhari certificate).'
                    }
                ],
                'downloads': [
                    {
                        'title': 'NIC Application Form',
                        'file_name': 'NIC_Application_Form.pdf',
                        'file_url': '/downloads/homeaffairs/NIC_Application_Form.pdf',
                        'file_size': '234 KB',
                        'description': 'Application form for National Identity Card'
                    }
                ],
                'locations': [
                    {
                        'name': 'Department of Registration of Persons',
                        'address': 'Battaramulla, Sri Lanka',
                        'phone': '+94-11-2877801',
                        'email': 'info@rgd.gov.lk',
                        'google_maps_url': 'https://maps.google.com/?q=6.9034,79.9185',
                        'latitude': 6.9034,
                        'longitude': 79.9185,
                        'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                    }
                ],
                'processing_time': '30 working days',
                'fees': 'LKR 150 (new), LKR 500 (replacement)',
                'contact_info': {
                    'hotline': '1919',
                    'email': 'nic@rgd.gov.lk',
                    'working_hours': 'Monday to Friday: 8:30 AM - 3:30 PM'
                }
            }
        ]
        
        # Insert all subservices
        subservice_count = 0
        for subservice in subservices_data:
            subservice['created_at'] = datetime.utcnow()
            subservice['updated_at'] = datetime.utcnow()
            subservice['view_count'] = 0
            subservices_collection.insert_one(subservice)
            subservice_count += 1
            print(f"  ✓ Created: {subservice['name']}")
        
        print(f"\n✅ Created {subservice_count} subservices")
        print("\n" + "="*70)
        print("🎉 MINISTRY SEEDING COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\nSummary:")
        print(f"  • Ministries created: {len(ministry_ids)}")
        print(f"  • Subservices created: {subservice_count}")
        print(f"  • Total FAQs: {sum(len(s.get('faqs', [])) for s in subservices_data)}")
        print(f"  • Total Downloads: {sum(len(s.get('downloads', [])) for s in subservices_data)}")
        print(f"  • Total Locations: {sum(len(s.get('locations', [])) for s in subservices_data)}")
        print("\n✨ Database is ready for use!\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🏛️  GOVERNMENT PORTAL - MINISTRY SEEDER")
    print("="*70)
    print("\nThis script will populate the database with:")
    print("  • 20+ Government Ministries")
    print("  • Comprehensive Subservices")
    print("  • FAQs with Official Answers")
    print("  • Downloadable PDF Forms")
    print("  • Location Links (Google Maps)")
    print("  • Step-by-Step Instructions")
    print("\n" + "="*70 + "\n")
    
    seed_ministries()