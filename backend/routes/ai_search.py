from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os
from datetime import datetime

# Create blueprint
ai_search_bp = Blueprint('ai_search', __name__, url_prefix='/api')

# Global variables
model = None
documents = []
embeddings = None
ministry_mappings = {}

def initialize_search_engine():
    """Initialize AI search with pre-trained model"""
    global model, documents, embeddings, ministry_mappings
    
    try:
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Model loaded successfully")
        
        # Load comprehensive services
        documents = get_comprehensive_services()
        
        # Build ministry mappings for intelligent suggestions
        ministry_mappings = build_ministry_mappings()
        
        save_documents()
        
        if documents:
            # Create embeddings from text + keywords + ministry context
            doc_texts = []
            for doc in documents:
                combined_text = (
                    doc['text'] + ' ' + 
                    ' '.join(doc.get('keywords', [])) + ' ' +
                    doc.get('ministry', '') + ' ' +
                    doc.get('category', '')
                )
                doc_texts.append(combined_text)
            
            embeddings = model.encode(doc_texts, convert_to_numpy=True)
            print(f"✓ Loaded {len(documents)} services with embeddings")
            return True
        
        return False
        
    except Exception as e:
        print(f"✗ Error initializing: {e}")
        import traceback
        traceback.print_exc()
        return False

def build_ministry_mappings():
    """Build intelligent ministry mappings for suggestions"""
    return {
        # Education & Exams
        'exam': 'Department of Examinations',
        'o/l': 'Department of Examinations',
        'a/l': 'Department of Examinations',
        'results': 'Department of Examinations',
        'education': 'Ministry of Education',
        'school': 'Ministry of Education',
        'university': 'Ministry of Higher Education',
        
        # Health
        'health': 'Ministry of Health',
        'hospital': 'Ministry of Health',
        'medicine': 'Ministry of Health',
        'doctor': 'Ministry of Health',
        
        # Transport
        'driving': 'Ministry of Road Transport and Highways',
        'vehicle': 'Ministry of Road Transport and Highways',
        'license': 'Ministry of Road Transport and Highways',
        'rto': 'Ministry of Road Transport and Highways',
        
        # Immigration & Travel
        'passport': 'Ministry of External Affairs',
        'visa': 'Ministry of External Affairs',
        'travel': 'Ministry of External Affairs',
        
        # Finance & Tax
        'tax': 'Income Tax Department',
        'pan': 'Income Tax Department',
        'gst': 'Ministry of Finance',
        'income': 'Income Tax Department',
        
        # Civil Registration
        'birth': 'Ministry of Home Affairs',
        'death': 'Ministry of Home Affairs',
        'marriage': 'Ministry of Home Affairs',
        
        # Employment & Jobs
        'job': 'Ministry of Labour and Employment',
        'employment': 'Ministry of Labour and Employment',
        'unemployment': 'Ministry of Labour and Employment',
        
        # Property
        'property': 'Ministry of Housing and Urban Affairs',
        'land': 'Revenue Department',
        'house': 'Ministry of Housing and Urban Affairs',
        
        # Business
        'business': 'Ministry of Corporate Affairs',
        'company': 'Ministry of Corporate Affairs',
        'startup': 'Ministry of Commerce',
    }

def suggest_ministry(query):
    """Intelligently suggest ministry based on query keywords"""
    query_lower = query.lower()
    
    # Check for keyword matches
    for keyword, ministry in ministry_mappings.items():
        if keyword in query_lower:
            return ministry
    
    return "Government Services Department"

def generate_ai_answer(query, top_services):
    """Generate a natural language answer based on the query and found services"""
    
    if not top_services:
        suggested_ministry = suggest_ministry(query)
        return {
            'answer': f"I couldn't find an exact match for '{query}' in our current database. However, this type of service is typically handled by the **{suggested_ministry}**. I recommend contacting them directly or visiting their office for more information.",
            'ministry_suggestion': suggested_ministry,
            'has_direct_service': False
        }
    
    # Get the top matching service
    top_service = top_services[0]
    service_name = top_service.get('title', 'this service')
    ministry = top_service.get('ministry', 'the relevant department')
    
    # Generate comprehensive answer
    answer_parts = []
    
    # Introduction
    answer_parts.append(f"To {query}, you need to apply for **{service_name}** through the **{ministry}**.")
    
    # Requirements
    requirements = top_service.get('requirements', [])
    if requirements:
        answer_parts.append("\n\n**Required Documents:**")
        for req in requirements:
            answer_parts.append(f"• {req}")
    
    # Fees
    fees = top_service.get('fees', '')
    if fees and fees != 'N/A':
        answer_parts.append(f"\n\n**Fees:** {fees}")
    
    # Processing time
    processing_time = top_service.get('processing_time', '')
    if processing_time and processing_time != 'Varies':
        answer_parts.append(f"\n**Processing Time:** {processing_time}")
    
    # Steps
    steps = top_service.get('steps', [])
    if steps:
        answer_parts.append("\n\n**Application Steps:**")
        for i, step in enumerate(steps, 1):
            answer_parts.append(f"{i}. {step}")
    
    # Additional info
    answer_parts.append(f"\n\nYou can find more information and apply through the {ministry} portal or visit their office.")
    
    return {
        'answer': '\n'.join(answer_parts),
        'ministry_suggestion': ministry,
        'has_direct_service': True
    }

def get_comprehensive_services():
    """Return comprehensive government services database"""
    return [
        {
            'id': 1,
            'title': 'Driving License Application & Renewal',
            'text': 'Apply for a new driving license, learner permit, or renew your existing license. Available for two-wheelers, four-wheelers, and commercial vehicles. Complete the driving test, submit required documents including identity proof, address proof, and medical certificate. Online and offline application available through Parivahan website or visit local RTO office.',
            'ministry': 'Ministry of Road Transport and Highways',
            'category': 'Transportation',
            'keywords': ['driving license', 'driver license', 'DL', 'learner permit', 'driving test', 'license renewal', 'two wheeler license', 'car license', 'vehicle license', 'how to get driving license', 'driving licence', 'licence', 'get a driving license', 'apply for driving license'],
            'url': '/services/driving-license',
            'icon': '🚗',
            'requirements': ['Age 18+', 'Identity Proof (Aadhaar/PAN)', 'Address Proof', 'Medical Certificate', '2 Photographs'],
            'fees': 'Rs. 200 - Rs. 1,000',
            'processing_time': '15-30 days',
            'steps': [
                'Visit Parivahan Sewa website',
                'Fill online application form',
                'Upload required documents',
                'Book appointment for test',
                'Pass written test',
                'Pass driving test',
                'Collect your license'
            ]
        },
        {
            'id': 2,
            'title': 'Passport Application & Renewal',
            'text': 'Apply for Indian passport, renew expired passport, or apply for tatkal (urgent) passport services. Available for adults and minors. Online application through Passport Seva portal with appointment booking at passport offices.',
            'ministry': 'Ministry of External Affairs',
            'category': 'Immigration & Travel',
            'keywords': ['passport', 'passport application', 'passport renewal', 'tatkal passport', 'travel document', 'international travel', 'how to get passport'],
            'url': '/services/passport',
            'icon': '🛂',
            'requirements': ['Birth Certificate', 'Address Proof', 'Identity Proof', 'Photographs'],
            'fees': 'Rs. 1,500 (Regular) - Rs. 3,500 (Tatkal)',
            'processing_time': '30-45 days (Regular), 3-7 days (Tatkal)',
            'steps': [
                'Register on Passport Seva portal',
                'Fill application form',
                'Pay fees online',
                'Book appointment at passport office',
                'Visit passport office with documents',
                'Collect passport or track delivery'
            ]
        },
        {
            'id': 3,
            'title': 'Birth Certificate Registration',
            'text': 'Register birth and obtain official birth certificate. Essential document for school admission, passport application, and other government services. Can be applied within 21 days of birth or as delayed registration.',
            'ministry': 'Ministry of Home Affairs',
            'category': 'Civil Registration',
            'keywords': ['birth certificate', 'birth registration', 'newborn registration', 'baby certificate', 'how to get birth certificate'],
            'url': '/services/birth-certificate',
            'icon': '👶',
            'requirements': ['Hospital birth certificate', 'Parents ID proof', 'Address proof'],
            'fees': 'Rs. 50 - Rs. 100',
            'processing_time': '7-15 days',
            'steps': [
                'Visit municipal corporation website',
                'Fill birth registration form',
                'Upload hospital certificate',
                'Submit parents documents',
                'Receive birth certificate'
            ]
        },
        {
            'id': 4,
            'title': 'PAN Card Application',
            'text': 'Apply for Permanent Account Number (PAN) card required for tax filing, banking, and financial transactions. Essential for income tax returns, opening bank accounts, and investments.',
            'ministry': 'Income Tax Department',
            'category': 'Finance & Tax',
            'keywords': ['PAN card', 'permanent account number', 'tax card', 'income tax', 'PAN application'],
            'url': '/services/pan-card',
            'icon': '💳',
            'requirements': ['Identity proof', 'Address proof', 'Date of birth proof', 'Photograph'],
            'fees': 'Rs. 110 (India) - Rs. 1,020 (Foreign)',
            'processing_time': '15-30 days',
            'steps': [
                'Visit NSDL or UTIITSL website',
                'Fill PAN application form',
                'Upload documents',
                'Pay application fee',
                'Receive PAN card by post'
            ]
        },
        {
            'id': 5,
            'title': 'Aadhaar Card Services',
            'text': 'Apply for new Aadhaar card, update Aadhaar details, or download e-Aadhaar. 12-digit unique identity number for Indian residents. Required for government schemes and services.',
            'ministry': 'UIDAI (Unique Identification Authority of India)',
            'category': 'Identity Services',
            'keywords': ['aadhaar', 'aadhaar card', 'UID', 'biometric', 'update aadhaar', 'aadhaar enrollment'],
            'url': '/services/aadhaar',
            'icon': '🆔',
            'requirements': ['Proof of Identity', 'Proof of Address', 'Date of birth proof'],
            'fees': 'Free (New enrollment), Rs. 50 (Update)',
            'processing_time': '30-90 days'
        },
        {
            'id': 6,
            'title': 'Voter ID Card (EPIC)',
            'text': 'Apply for new voter ID card or update existing electoral details. Required for voting in elections and useful as identity proof.',
            'ministry': 'Election Commission of India',
            'category': 'Electoral Services',
            'keywords': ['voter id', 'voter card', 'election card', 'EPIC', 'voter registration'],
            'url': '/services/voter-id',
            'icon': '🗳️',
            'requirements': ['Age 18+', 'Address proof', 'Photograph'],
            'fees': 'Free',
            'processing_time': '30-60 days'
        },
        {
            'id': 7,
            'title': 'Property Registration',
            'text': 'Register property purchase, sale, or transfer. Pay stamp duty online. Get property documents verified and registered.',
            'ministry': 'Ministry of Housing and Urban Affairs',
            'category': 'Property',
            'keywords': ['property registration', 'land registration', 'house registration', 'property transfer'],
            'url': '/services/property-registration',
            'icon': '🏠',
            'fees': 'Stamp Duty (5-7% of value) + Registration Fee',
            'processing_time': '15-30 days'
        },
        {
            'id': 8,
            'title': 'Business Registration',
            'text': 'Register new business, startup, or company. Get GST registration and business license.',
            'ministry': 'Ministry of Corporate Affairs',
            'category': 'Business',
            'keywords': ['business registration', 'company registration', 'GST', 'startup'],
            'url': '/services/business-registration',
            'icon': '💼',
            'fees': 'Rs. 5,000 - Rs. 50,000',
            'processing_time': '7-21 days'
        },
        {
            'id': 9,
            'title': 'Marriage Certificate',
            'text': 'Register marriage and obtain marriage certificate. Legal proof of marriage required for various services.',
            'ministry': 'Ministry of Home Affairs',
            'category': 'Civil Registration',
            'keywords': ['marriage certificate', 'marriage registration', 'wedding certificate'],
            'url': '/services/marriage-certificate',
            'icon': '💍',
            'fees': 'Rs. 100 - Rs. 500',
            'processing_time': '30 days'
        },
        {
            'id': 10,
            'title': 'Ration Card',
            'text': 'Apply for ration card to receive subsidized food grains through Public Distribution System.',
            'ministry': 'Ministry of Consumer Affairs',
            'category': 'Welfare',
            'keywords': ['ration card', 'food subsidy', 'PDS', 'public distribution'],
            'url': '/services/ration-card',
            'icon': '🌾',
            'fees': 'Free',
            'processing_time': '30-45 days'
        },
        {
            'id': 11,
            'title': 'Health Insurance',
            'text': 'Enroll in government health insurance schemes including Ayushman Bharat. Coverage for hospitalization.',
            'ministry': 'Ministry of Health and Family Welfare',
            'category': 'Healthcare',
            'keywords': ['health insurance', 'ayushman bharat', 'medical insurance'],
            'url': '/services/health-insurance',
            'icon': '🏥',
            'fees': 'Free to Rs. 5,000/year',
            'processing_time': '30 days'
        },
        {
            'id': 12,
            'title': 'Pension Schemes',
            'text': 'Apply for government pension schemes including old age pension, widow pension, disability pension.',
            'ministry': 'Ministry of Social Justice and Empowerment',
            'category': 'Welfare',
            'keywords': ['pension', 'old age pension', 'retirement', 'widow pension'],
            'url': '/services/pension',
            'icon': '👴',
            'fees': 'Free',
            'processing_time': '60-90 days'
        }
    ]

def save_documents():
    """Save documents to disk"""
    global documents
    try:
        with open('documents.pkl', 'wb') as f:
            pickle.dump(documents, f)
        print("✓ Documents saved")
    except Exception as e:
        print(f"✗ Error saving: {e}")

def preprocess_query(query):
    """Expand query for better matching"""
    query = query.lower().strip()
    
    expansions = {
        'dl': 'driving license',
        'o/l': 'ordinary level exam examination results',
        'a/l': 'advanced level exam examination results',
        'how to get': 'apply application process obtain',
        'how do i': 'apply application process',
        'i want': 'apply for obtain',
        'i need': 'apply for obtain',
        'how can i': 'apply application process',
        'licence': 'license',
        'get a': 'apply for obtain',
        'getting': 'apply for obtain',
        'exam results': 'examination results certificate department of examinations',
    }
    
    expanded = query
    for key, value in expansions.items():
        if key in query:
            expanded += ' ' + value
    
    return expanded

def keyword_search(query, documents):
    """Fallback keyword search"""
    query_words = set(query.lower().split())
    results = []
    
    for doc in documents:
        score = 0
        doc_text = (doc.get('title', '') + ' ' + doc.get('text', '') + ' ' + ' '.join(doc.get('keywords', []))).lower()
        
        for word in query_words:
            if len(word) > 2 and word in doc_text:
                score += 1
        
        if score > 0:
            results.append((doc, score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in results[:5]]

@ai_search_bp.route('/ai-search/ministry', methods=['POST'])
def ai_search_ministry():
    """AI-powered search with LLM-generated answers"""
    try:
        print("=== AI Search Request Received ===")
        
        data = request.get_json()
        query = data.get('query', '').strip()
        
        print(f"Query received: '{query}'")
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Please enter a search query'
            }), 400
        
        # Initialize if needed
        if model is None or embeddings is None:
            print("Initializing search engine...")
            success = initialize_search_engine()
            if not success:
                return jsonify({
                    'success': False,
                    'error': 'Search engine initialization failed'
                }), 500
        
        # Preprocess query
        expanded_query = preprocess_query(query)
        print(f"Expanded query: '{expanded_query}'")
        
        # Generate query embedding
        query_embedding = model.encode([expanded_query], convert_to_numpy=True)[0]
        
        # Calculate cosine similarity
        similarities = np.dot(embeddings, query_embedding) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        print(f"Top 3 similarities: {sorted(similarities, reverse=True)[:3]}")
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:10]
        services = []
        sources = []
        
        # Threshold for considering a match
        SIMILARITY_THRESHOLD = 0.25
        
        for idx in top_indices:
            if similarities[idx] >= SIMILARITY_THRESHOLD:
                doc = documents[idx]
                score = float(similarities[idx])
                
                service = {
                    'id': doc.get('id', idx),
                    'name': doc.get('title', 'Unknown Service'),
                    'title': doc.get('title', 'Unknown Service'),
                    'description': doc.get('text', '')[:300] + '...' if len(doc.get('text', '')) > 300 else doc.get('text', ''),
                    'ministry': doc.get('ministry', 'Government of India'),
                    'ministry_name': doc.get('ministry', 'Government of India'),
                    'category': doc.get('category', 'General'),
                    'url': doc.get('url', '#'),
                    'icon': doc.get('icon', '📋'),
                    'requirements': doc.get('requirements', []),
                    'fees': doc.get('fees', 'N/A'),
                    'processing_time': doc.get('processing_time', 'Varies'),
                    'steps': doc.get('steps', []),
                    'relevance_score': score,
                    'confidence': 'High' if score > 0.5 else 'Medium' if score > 0.35 else 'Low'
                }
                services.append(service)
                
                sources.append({
                    'title': doc.get('title', 'Unknown'),
                    'url': doc.get('url', '#'),
                    'ministry': doc.get('ministry', 'Government of India'),
                    'relevance': score
                })
        
        # Limit to top 5
        services = services[:5]
        sources = sources[:5]
        
        # Generate AI answer
        ai_response = generate_ai_answer(query, services)
        
        # Fallback to keyword search if no good matches
        if not services or (services and services[0]['relevance_score'] < 0.30):
            print("Using keyword fallback or low confidence - providing intelligent suggestion")
            keyword_results = keyword_search(query, documents)
            
            if keyword_results and not services:
                for doc in keyword_results:
                    services.append({
                        'id': doc.get('id', 0),
                        'name': doc.get('title', 'Unknown Service'),
                        'title': doc.get('title', 'Unknown Service'),
                        'description': doc.get('text', '')[:300],
                        'ministry': doc.get('ministry', 'Government of India'),
                        'ministry_name': doc.get('ministry', 'Government of India'),
                        'url': doc.get('url', '#'),
                        'icon': doc.get('icon', '📋'),
                        'confidence': 'Low'
                    })
                    sources.append({
                        'title': doc.get('title', 'Unknown'),
                        'url': doc.get('url', '#')
                    })
        
        print(f"✓ Returning {len(services)} services")
        print(f"✓ AI Answer generated: {ai_response['has_direct_service']}")
        
        return jsonify({
            'success': True,
            'services': services,
            'sources': sources,
            'total': len(services),
            'query': query,
            'confidence': services[0]['confidence'] if services else 'N/A',
            'answer': ai_response['answer'],
            'ministry_suggestion': ai_response['ministry_suggestion'],
            'has_direct_service': ai_response['has_direct_service']
        })
        
    except Exception as e:
        print(f"❌ Error in AI search: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': 'Sorry, an error occurred while processing your question. Please try again.',
            'services': [],
            'sources': []
        }), 500

@ai_search_bp.route('/ai-search', methods=['POST'])
def ai_search():
    """Standard AI search endpoint"""
    return ai_search_ministry()

# Initialize on import
print("🔧 Initializing AI Search Engine with LLM capabilities...")
initialize_search_engine()