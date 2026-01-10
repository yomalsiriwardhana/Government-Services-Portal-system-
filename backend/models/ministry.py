from datetime import datetime
from bson import ObjectId

class Ministry:
    """Ministry model for MongoDB"""
    
    def __init__(self, db):
        self.collection = db.ministries
        self.subservices_collection = db.subservices
    
    def create(self, ministry_data):
        """Create a new ministry"""
        ministry_data['created_at'] = datetime.utcnow()
        ministry_data['updated_at'] = datetime.utcnow()
        ministry_data['view_count'] = 0
        
        result = self.collection.insert_one(ministry_data)
        return str(result.inserted_id)
    
    def find_by_id(self, ministry_id):
        """Find ministry by ID"""
        ministry = self.collection.find_one({'_id': ObjectId(ministry_id)})
        if ministry:
            ministry['_id'] = str(ministry['_id'])
        return ministry
    
    def find_all(self):
        """Find all ministries"""
        ministries = list(self.collection.find().sort('name', 1))
        for ministry in ministries:
            ministry['_id'] = str(ministry['_id'])
        return ministries
    
    def search(self, query_text):
        """Search ministries by text"""
        search_query = {
            '$or': [
                {'name': {'$regex': query_text, '$options': 'i'}},
                {'description': {'$regex': query_text, '$options': 'i'}},
                {'keywords': {'$regex': query_text, '$options': 'i'}}
            ]
        }
        
        ministries = list(self.collection.find(search_query))
        for ministry in ministries:
            ministry['_id'] = str(ministry['_id'])
        return ministries
    
    def update(self, ministry_id, update_data):
        """Update ministry data"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(ministry_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete(self, ministry_id):
        """Delete a ministry"""
        result = self.collection.delete_one({'_id': ObjectId(ministry_id)})
        return result.deleted_count > 0
    
    def increment_view_count(self, ministry_id):
        """Increment ministry view count"""
        self.collection.update_one(
            {'_id': ObjectId(ministry_id)},
            {'$inc': {'view_count': 1}}
        )
    
    # Subservice methods
    def create_subservice(self, subservice_data):
        """Create a new subservice"""
        subservice_data['created_at'] = datetime.utcnow()
        subservice_data['updated_at'] = datetime.utcnow()
        subservice_data['view_count'] = 0
        
        result = self.subservices_collection.insert_one(subservice_data)
        return str(result.inserted_id)
    
    def find_subservice_by_id(self, subservice_id):
        """Find subservice by ID"""
        subservice = self.subservices_collection.find_one({'_id': ObjectId(subservice_id)})
        if subservice:
            subservice['_id'] = str(subservice['_id'])
        return subservice
    
    def find_subservices_by_ministry(self, ministry_id):
        """Find all subservices for a ministry"""
        subservices = list(self.subservices_collection.find({'ministry_id': ministry_id}).sort('name', 1))
        for subservice in subservices:
            subservice['_id'] = str(subservice['_id'])
        return subservices
    
    def search_subservices(self, query_text, ministry_id=None):
        """Search subservices by text"""
        search_query = {
            '$or': [
                {'name': {'$regex': query_text, '$options': 'i'}},
                {'description': {'$regex': query_text, '$options': 'i'}},
                {'keywords': {'$regex': query_text, '$options': 'i'}},
                {'faqs.question': {'$regex': query_text, '$options': 'i'}},
                {'faqs.answer': {'$regex': query_text, '$options': 'i'}}
            ]
        }
        
        if ministry_id:
            search_query['ministry_id'] = ministry_id
        
        subservices = list(self.subservices_collection.find(search_query))
        for subservice in subservices:
            subservice['_id'] = str(subservice['_id'])
        return subservices
    
    def update_subservice(self, subservice_id, update_data):
        """Update subservice data"""
        update_data['updated_at'] = datetime.utcnow()
        result = self.subservices_collection.update_one(
            {'_id': ObjectId(subservice_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete_subservice(self, subservice_id):
        """Delete a subservice"""
        result = self.subservices_collection.delete_one({'_id': ObjectId(subservice_id)})
        return result.deleted_count > 0
    
    def increment_subservice_view_count(self, subservice_id):
        """Increment subservice view count"""
        self.subservices_collection.update_one(
            {'_id': ObjectId(subservice_id)},
            {'$inc': {'view_count': 1}}
        )
    
    def get_ministry_with_subservices(self, ministry_id):
        """Get ministry with all its subservices"""
        ministry = self.find_by_id(ministry_id)
        if ministry:
            ministry['subservices'] = self.find_subservices_by_ministry(ministry_id)
        return ministry
    
    def get_all_ministries_with_counts(self):
        """Get all ministries with subservice counts"""
        ministries = self.find_all()
        for ministry in ministries:
            ministry_id = ministry['_id']
            ministry['subservice_count'] = self.subservices_collection.count_documents({'ministry_id': ministry_id})
        return ministries