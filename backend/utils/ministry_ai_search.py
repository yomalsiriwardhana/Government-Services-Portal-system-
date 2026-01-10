"""
AI-Powered Search for Government Ministries and Services
Uses sentence transformers and FAISS for semantic search
"""

import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer
import faiss
from bson import ObjectId

class MinistryAISearch:
    def __init__(self, db):
        self.db = db
        self.model = None
        self.index = None
        self.documents = []
        self.model_name = 'all-MiniLM-L6-v2'
        self.index_file = 'faiss_index'
        self.docs_file = 'documents.pkl'
        
    def load_model(self):
        """Load the sentence transformer model"""
        print(f"Loading embedding model: {self.model_name}...")
        self.model = SentenceTransformer(self.model_name)
        print(f"✅ Model loaded. Embedding dimension: {self.model.get_sentence_embedding_dimension()}")
        
    def prepare_documents(self):
        """Prepare documents from database for indexing"""
        self.documents = []
        
        # Get all ministries
        ministries = list(self.db.ministries.find())
        for ministry in ministries:
            doc_text = f"{ministry['name']} - {ministry['description']}. "
            doc_text += f"Keywords: {ministry.get('keywords', '')}. "
            doc_text += f"Contact: {ministry.get('contact_email', '')}"
            
            self.documents.append({
                'id': str(ministry['_id']),
                'type': 'ministry',
                'name': ministry['name'],
                'text': doc_text,
                'data': self._serialize_document(ministry)
            })
        
        # Get all subservices
        subservices = list(self.db.subservices.find())
        for subservice in subservices:
            # Get ministry name
            ministry = self.db.ministries.find_one({'_id': ObjectId(subservice['ministry_id'])})
            ministry_name = ministry['name'] if ministry else 'Unknown Ministry'
            
            doc_text = f"{subservice['name']} - {subservice['description']}. "
            doc_text += f"Ministry: {ministry_name}. "
            doc_text += f"Category: {subservice.get('category', '')}. "
            doc_text += f"Keywords: {subservice.get('keywords', '')}. "
            
            # Add requirements
            if subservice.get('requirements'):
                doc_text += f"Requirements: {', '.join(subservice['requirements'])}. "
            
            # Add FAQs
            if subservice.get('faqs'):
                for faq in subservice['faqs']:
                    doc_text += f"FAQ: {faq['question']} {faq['answer']} "
            
            self.documents.append({
                'id': str(subservice['_id']),
                'type': 'subservice',
                'name': subservice['name'],
                'ministry_name': ministry_name,
                'text': doc_text,
                'data': self._serialize_document(subservice)
            })
        
        print(f"✅ Prepared {len(self.documents)} documents for indexing")
        
    def _serialize_document(self, doc):
        """Convert MongoDB document to JSON-serializable format"""
        serialized = {}
        for key, value in doc.items():
            if isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, list):
                serialized[key] = [self._serialize_value(item) for item in value]
            elif isinstance(value, dict):
                serialized[key] = self._serialize_document(value)
            else:
                serialized[key] = value
        return serialized
    
    def _serialize_value(self, value):
        """Serialize individual values"""
        if isinstance(value, ObjectId):
            return str(value)
        elif isinstance(value, dict):
            return self._serialize_document(value)
        elif isinstance(value, list):
            return [self._serialize_value(item) for item in value]
        else:
            return value
        
    def build_index(self):
        """Build FAISS index from documents"""
        if not self.model:
            self.load_model()
            
        if not self.documents:
            self.prepare_documents()
        
        # Create embeddings
        print("Creating embeddings for all documents...")
        texts = [doc['text'] for doc in self.documents]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Build FAISS index
        print("Building FAISS index...")
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        print(f"✅ FAISS index built with {self.index.ntotal} vectors")
        
    def save_index(self):
        """Save index and documents to disk"""
        faiss.write_index(self.index, self.index_file)
        with open(self.docs_file, 'wb') as f:
            pickle.dump(self.documents, f)
        print(f"✅ Index saved to {self.index_file}")
        print(f"✅ Documents saved to {self.docs_file}")
        
    def load_index(self):
        """Load index and documents from disk"""
        if not os.path.exists(self.index_file) or not os.path.exists(self.docs_file):
            raise FileNotFoundError("Index files not found. Please build index first.")
        
        if not self.model:
            self.load_model()
            
        self.index = faiss.read_index(self.index_file)
        with open(self.docs_file, 'rb') as f:
            self.documents = pickle.load(f)
        
        print(f"✅ Index loaded with {self.index.ntotal} vectors")
        print(f"✅ Loaded {len(self.documents)} documents")
        
    def search(self, query, top_k=5):
        """Search for relevant documents"""
        if not self.model or not self.index:
            self.load_index()
        
        # Create query embedding
        query_embedding = self.model.encode([query])
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                similarity = 1 / (1 + distances[0][i])  # Convert distance to similarity
                
                results.append({
                    'id': doc['id'],
                    'type': doc['type'],
                    'name': doc['name'],
                    'ministry_name': doc.get('ministry_name', ''),
                    'similarity_score': float(similarity),
                    'data': doc['data']
                })
        
        return results
    
    def search_with_answer(self, query, top_k=5):
        """Search and generate an answer"""
        results = self.search(query, top_k)
        
        if not results:
            return {
                'answer': f"No relevant services found for '{query}'. Please try different keywords.",
                'results': [],
                'sources': [],
                'confidence': 0.0
            }
        
        # Generate answer
        answer = f"Based on your query '{query}', here are the relevant government services:\n\n"
        
        for i, result in enumerate(results[:3], 1):
            if result['type'] == 'ministry':
                answer += f"{i}. **{result['name']}**: {result['data'].get('description', '')}\n"
            else:
                answer += f"{i}. **{result['name']}** ({result.get('ministry_name', 'Unknown Ministry')}): "
                answer += f"{result['data'].get('description', '')}\n"
        
        # Extract sources
        sources = []
        for result in results[:5]:
            sources.append({
                'name': result['name'],
                'type': result['type'],
                'ministry': result.get('ministry_name', '')
            })
        
        # Calculate average confidence
        avg_confidence = sum(r['similarity_score'] for r in results[:3]) / min(3, len(results))
        
        return {
            'answer': answer,
            'results': results,
            'sources': sources,
            'confidence': float(avg_confidence)
        }


def initialize_ai_search(db):
    """Initialize and build AI search system"""
    print("\n" + "="*70)
    print("🤖 Initializing AI-Powered Ministry Search")
    print("="*70 + "\n")
    
    ai_search = MinistryAISearch(db)
    ai_search.load_model()
    ai_search.build_index()
    ai_search.save_index()
    
    print("\n" + "="*70)
    print("✅ AI Search System Ready!")
    print("="*70 + "\n")
    
    return ai_search