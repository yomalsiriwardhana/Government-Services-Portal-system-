from datetime import datetime
from bson import ObjectId

class Service:
    """Service model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db.services
    
    def create(self, service_data):
        """Create a new service"""
        service_data['created_at'] = datetime.utcnow()
        service_data['updated_at'] = datetime.utcnow()
        service_data['view_count'] = 0
        service_data['click_count'] = 0
        
        result = self.collection.insert_one(service_data)
        return str(result.inserted_id)
    
    def find_by_id(self, service_id):
        """Find service by ID"""
        return self.collection.find_one({'_id': ObjectId(service_id)})
    
    def find_all(self, category=None, ministry=None):
        """Find all services with optional filters"""
        query = {}
        if category:
            query['category'] = category
        if ministry:
            query['ministry'] = ministry
        
        services = list(self.collection.find(query))
        for service in services:
            service['_id'] = str(service['_id'])
        return services
    
    def search(self, query_text, category=None):
        """Search services by text"""
        search_query = {
            '$or': [
                {'name': {'$regex': query_text, '$options': 'i'}},
                {'description': {'$regex': query_text, '$options': 'i'}},
                {'department': {'$regex': query_text, '$options': 'i'}},
                {'keywords': {'$regex': query_text, '$options': 'i'}}
            ]
        }
        
        if category:
            search_query['category'] = category
        
        services = list(self.collection.find(search_query))
        for service in services:
            service['_id'] = str(service['_id'])
        return services
    
    def update(self, service_id, update_data):
        """Update service data"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(service_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete(self, service_id):
        """Delete a service"""
        result = self.collection.delete_one({'_id': ObjectId(service_id)})
        return result.deleted_count > 0
    
    def increment_view_count(self, service_id):
        """Increment service view count"""
        self.collection.update_one(
            {'_id': ObjectId(service_id)},
            {'$inc': {'view_count': 1}}
        )
    
    def increment_click_count(self, service_id):
        """Increment service click count"""
        self.collection.update_one(
            {'_id': ObjectId(service_id)},
            {'$inc': {'click_count': 1}}
        )
    
    def get_popular_services(self, limit=10):
        """Get most popular services by view count"""
        services = list(
            self.collection.find()
            .sort('view_count', -1)
            .limit(limit)
        )
        for service in services:
            service['_id'] = str(service['_id'])
        return services
    
    def get_by_category(self, category):
        """Get services by category"""
        services = list(self.collection.find({'category': category}))
        for service in services:
            service['_id'] = str(service['_id'])
        return services
    
    def get_categories_with_counts(self):
        """Get all categories with service counts"""
        pipeline = [
            {
                '$group': {
                    '_id': '$category',
                    'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}}
        ]
        
        result = list(self.collection.aggregate(pipeline))
        return result
    
    def seed_initial_services(self):
        """Seed database with initial government services"""
        initial_services = [
            {
                'name': 'Passport Application',
                'description': 'Apply for a new Sri Lankan passport or renew existing passport',
                'category': 'Immigration',
                'ministry': 'Ministry of Foreign Affairs',
                'department': 'Department of Immigration and Emigration',
                'requirements': [
                    'Birth Certificate',
                    'National Identity Card',
                    'Two passport-sized photographs',
                    'Proof of residence'
                ],
                'how_to_apply': 'Visit the nearest District Secretariat or apply online through the official portal',
                'official_link': 'https://www.immigration.gov.lk',
                'keywords': 'passport, travel document, immigration'
            },
            {
                'name': 'Driving License Application',
                'description': 'Apply for a new driving license or renew existing license',
                'category': 'Transport',
                'ministry': 'Ministry of Transport',
                'department': 'Department of Motor Traffic',
                'requirements': [
                    'Medical Certificate',
                    'National Identity Card',
                    'Completed application form',
                    'Passport-sized photographs'
                ],
                'how_to_apply': 'Visit the nearest Motor Traffic Office after completing driving lessons',
                'official_link': 'https://www.motortraffic.gov.lk',
                'keywords': 'driving license, vehicle, transport'
            },
            {
                'name': 'Birth Certificate',
                'description': 'Obtain a certified copy of birth certificate',
                'category': 'Civil Registration',
                'ministry': 'Ministry of Home Affairs',
                'department': 'Department of Registration of Persons',
                'requirements': [
                    'Application form',
                    'Identity card of applicant',
                    'Registration fee'
                ],
                'how_to_apply': 'Visit the Divisional Secretariat where the birth was registered',
                'official_link': 'https://www.rgd.gov.lk',
                'keywords': 'birth certificate, civil registration'
            },
            {
                'name': 'University Admission',
                'description': 'Apply for university admission through the University Grants Commission',
                'category': 'Education',
                'ministry': 'Ministry of Education',
                'department': 'University Grants Commission',
                'requirements': [
                    'A/L Results Sheet',
                    'Application form',
                    'National Identity Card',
                    'School leaving certificate'
                ],
                'how_to_apply': 'Submit online application through UGC portal during application period',
                'official_link': 'https://www.ugc.ac.lk',
                'keywords': 'university, higher education, admission'
            },
            {
                'name': 'Business Registration',
                'description': 'Register a new business with the Registrar of Companies',
                'category': 'Business',
                'ministry': 'Ministry of Finance',
                'department': 'Registrar of Companies',
                'requirements': [
                    'Business name',
                    'Business plan',
                    'Identity documents of directors',
                    'Registered office address'
                ],
                'how_to_apply': 'Apply online or visit the ROC office',
                'official_link': 'https://www.roc.gov.lk',
                'keywords': 'business registration, company, entrepreneur'
            }
        ]
        
        # Check if services already exist
        if self.collection.count_documents({}) == 0:
            for service in initial_services:
                self.create(service)
            print("✅ Initial services seeded successfully")
        else:
            print("ℹ️ Services already exist, skipping seed")