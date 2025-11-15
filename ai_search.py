import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Try to import FAISS, but don't crash if it fails
try:
    import faiss
    FAISS_AVAILABLE = True
    print("✅ FAISS loaded successfully")
except Exception as e:
    FAISS_AVAILABLE = False
    print(f"⚠️  FAISS not available, using fallback search: {e}")

class AISearchEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self.embeddings = None
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.mongo_client["citizen_portal"]

    def extract_searchable_content(self):
        """Extract all searchable content from services"""
        services = list(self.db["services"].find({}, {"_id": 0}))
        documents = []
        
        for service in services:
            service_name = service.get("name", {}).get("en", "Unknown Service")
            
            # Add service-level document
            service_doc = {
                "type": "service",
                "title": service_name,
                "content": f"Service: {service_name}",
                "service_id": service.get("id"),
                "metadata": {
                    "service_name": service_name,
                    "multilingual_names": service.get("name", {})
                }
            }
            documents.append(service_doc)
            
            # Add subservice and question documents
            for subservice in service.get("subservices", []):
                subservice_name = subservice.get("name", {}).get("en", "Unknown Subservice")
                
                for question in subservice.get("questions", []):
                    question_text = question.get("q", {}).get("en", "")
                    answer_text = question.get("answer", {}).get("en", "")
                    instructions = question.get("instructions", "")
                    
                    # Create comprehensive searchable content
                    content = f"""
Service: {service_name}
Subservice: {subservice_name}
Question: {question_text}
Answer: {answer_text}
Instructions: {instructions}
""".strip()
                    
                    doc = {
                        "type": "qa",
                        "title": question_text,
                        "content": content,
                        "service_id": service.get("id"),
                        "subservice_id": subservice.get("id"),
                        "metadata": {
                            "service_name": service_name,
                            "subservice_name": subservice_name,
                            "question": question.get("q", {}),
                            "answer": question.get("answer", {}),
                            "downloads": question.get("downloads", []),
                            "location": question.get("location", ""),
                            "instructions": instructions
                        }
                    }
                    documents.append(doc)
        
        return documents

    def build_index(self):
        """Build search index from service content"""
        print("Extracting searchable content...")
        self.documents = self.extract_searchable_content()
        
        if not self.documents:
            print("No documents found to index")
            return False
        
        print(f"Found {len(self.documents)} documents to index")
        
        # Extract text content for embedding
        texts = [doc["content"] for doc in self.documents]
        
        print("Generating embeddings...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        
        if FAISS_AVAILABLE:
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            self.index.add(self.embeddings.astype('float32'))
            
            print(f"✅ FAISS index built with {self.index.ntotal} documents")
        else:
            # Fallback: normalize embeddings for cosine similarity
            norms = np.linalg.norm(self.embeddings, axis=1, keepdims=True)
            self.embeddings = self.embeddings / (norms + 1e-10)
            print(f"✅ Fallback index built with {len(self.documents)} documents")
        
        return True

    def search(self, query, top_k=5):
        """Search for relevant documents"""
        if self.embeddings is None:
            return {"error": "Search index not built"}
        
        # Generate query embedding
        query_embedding = self.model.encode([query])
        
        if FAISS_AVAILABLE and self.index is not None:
            # FAISS search
            faiss.normalize_L2(query_embedding)
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx >= 0:
                    doc = self.documents[idx]
                    result = {
                        "rank": i + 1,
                        "score": float(score),
                        "title": doc["title"],
                        "content": doc["content"],
                        "type": doc["type"],
                        "metadata": doc["metadata"]
                    }
                    results.append(result)
        else:
            # Fallback: cosine similarity search
            query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-10)
            scores = np.dot(self.embeddings, query_norm.T).flatten()
            
            # Get top k indices
            top_indices = np.argsort(scores)[::-1][:top_k]
            
            results = []
            for i, idx in enumerate(top_indices):
                doc = self.documents[idx]
                result = {
                    "rank": i + 1,
                    "score": float(scores[idx]),
                    "title": doc["title"],
                    "content": doc["content"],
                    "type": doc["type"],
                    "metadata": doc["metadata"]
                }
                results.append(result)
        
        return {
            "query": query,
            "results": results,
            "total_found": len(results)
        }

    def generate_answer(self, query, search_results):
        """Generate an answer based on search results"""
        if not search_results["results"]:
            return {
                "answer": "I couldn't find specific information about your question. Please try rephrasing your query or contact the relevant ministry directly.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Get the best matching result
        best_result = search_results["results"][0]
        metadata = best_result["metadata"]
        
        # Generate contextual answer
        if best_result["type"] == "qa":
            answer = metadata.get("answer", {}).get("en", "")
            service_name = metadata.get("service_name", "")
            subservice_name = metadata.get("subservice_name", "")
            instructions = metadata.get("instructions", "")
            downloads = metadata.get("downloads", [])
            location = metadata.get("location", "")
            
            response = f"**{service_name} - {subservice_name}**\n\n"
            response += f"{answer}\n\n"
            
            if instructions:
                response += f"**Instructions:** {instructions}\n\n"
            
            if downloads:
                response += f"**Downloads:** {', '.join([d.split('/')[-1] for d in downloads])}\n\n"
            
            if location:
                response += f"**Location:** [View on Map]({location})\n\n"
            
            sources = [f"{service_name} - {subservice_name}"]
            confidence = best_result["score"]
        else:
            # Service-level result
            service_name = metadata.get("service_name", "")
            response = f"For questions about **{service_name}**, please explore the available subservices and specific questions in that ministry section."
            sources = [service_name]
            confidence = best_result["score"]
        
        return {
            "answer": response.strip(),
            "sources": sources,
            "confidence": confidence,
            "related_results": search_results["results"][:3]
        }

# Global search engine instance
search_engine = None

def initialize_search_engine():
    """Initialize the search engine"""
    global search_engine
    if search_engine is None:
        search_engine = AISearchEngine()
        success = search_engine.build_index()
        if not success:
            search_engine = None
    return search_engine

def perform_ai_search(query):
    """Perform AI search and return formatted results"""
    engine = initialize_search_engine()
    if engine is None:
        return {"error": "Search engine not available"}
    
    search_results = engine.search(query, top_k=5)
    answer_data = engine.generate_answer(query, search_results)
    
    return {
        "query": query,
        "answer": answer_data["answer"],
        "sources": answer_data["sources"],
        "confidence": answer_data["confidence"],
        "search_results": search_results["results"],
        "status": "success"
    }