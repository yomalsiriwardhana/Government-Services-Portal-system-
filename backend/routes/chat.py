"""
Chatbot Routes with Conversation Flow
Implements Intent-based + RAG hybrid chatbot

States:
- GREETING: Say Hi, identify user  
- ASK_HELP: Ask what help is needed
- AI_SEARCH: Answer using AI Search (Task 7)
"""

from flask import Blueprint, request, jsonify, current_app, session
from datetime import datetime
import jwt
from functools import wraps

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# ========================================
# AUTHENTICATION HELPER
# ========================================

def get_current_user():
    """Get current user from token if available"""
    token = None
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return None
    
    if not token:
        return None
    
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = data['user_id']
        from bson import ObjectId
        user = current_app.db.users.find_one({'_id': ObjectId(user_id)})
        return user
    except:
        return None

# ========================================
# CONVERSATION STATE MANAGEMENT
# ========================================

# In-memory session store (simple approach for demo)
# In production, use Redis or database
chat_sessions = {}

def get_session(session_id):
    """Get or create chat session"""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {
            'stage': 'GREETING',
            'username': 'User',
            'created_at': datetime.now().isoformat()
        }
    return chat_sessions[session_id]

def update_session(session_id, updates):
    """Update chat session"""
    if session_id in chat_sessions:
        chat_sessions[session_id].update(updates)

# ========================================
# GREETING HANDLER
# ========================================

def handle_greeting(msg, session_state):
    """Handle greeting stage"""
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'hii', 'hiii']
    
    msg_lower = msg.lower().strip()
    
    # Check if message contains a greeting
    is_greeting = any(greeting in msg_lower for greeting in greetings)
    
    if is_greeting:
        session_state['stage'] = 'ASK_HELP'
        username = session_state.get('username', 'User')
        
        return {
            'reply': f"Hi {username} 👋 How can I help you today?",
            'stage': 'ASK_HELP',
            'suggestions': ['I need help', 'Apply for passport', 'Get driving license']
        }
    
    return {
        'reply': "Hello 👋 Please say Hi to start our conversation!",
        'stage': 'GREETING',
        'suggestions': ['Hi', 'Hello']
    }

# ========================================
# HELP INTENT HANDLER
# ========================================

def handle_help(msg, session_state):
    """Handle help request stage"""
    msg_lower = msg.lower().strip()
    
    # Keywords that indicate user wants help
    help_keywords = ['help', 'assist', 'support', 'need', 'want', 'looking for', 'how to', 'apply', 'get']
    
    # Check if user is asking for help or stating intent
    wants_help = any(keyword in msg_lower for keyword in help_keywords)
    
    # Check for direct service queries (skip to AI_SEARCH)
    service_keywords = ['passport', 'license', 'driving', 'birth', 'certificate', 'business', 
                        'tax', 'pan', 'aadhaar', 'voter', 'property', 'marriage', 'pension', 
                        'o/l', 'a/l', 'exam', 'result']
    
    is_service_query = any(keyword in msg_lower for keyword in service_keywords)
    
    if is_service_query:
        # Direct service query - go to AI_SEARCH
        session_state['stage'] = 'AI_SEARCH'
        return handle_ai_search(msg, session_state)
    
    if wants_help:
        session_state['stage'] = 'AI_SEARCH'
        return {
            'reply': "Sure 😊 What do you need help with? You can ask about any government service like passport, driving license, birth certificate, etc.",
            'stage': 'AI_SEARCH',
            'suggestions': ['Apply for passport', 'Get driving license', 'Register business']
        }
    
    return {
        'reply': "I'm here to help 🙂 Please tell me what government service you need assistance with.",
        'stage': 'ASK_HELP',
        'suggestions': ['I need help', 'How to apply for passport?']
    }

# ========================================
# AI SEARCH HANDLER (RAG)
# ========================================

def handle_ai_search(msg, session_state):
    """Handle AI search using existing RAG system"""
    from routes.ai_search import model, embeddings, documents, generate_ai_answer, preprocess_query, keyword_search, initialize_search_engine
    import numpy as np
    
    # Initialize if needed
    if model is None or embeddings is None:
        initialize_search_engine()
    
    try:
        # Preprocess query
        expanded_query = preprocess_query(msg)
        
        # Generate query embedding
        query_embedding = model.encode([expanded_query], convert_to_numpy=True)[0]
        
        # Calculate cosine similarity
        similarities = np.dot(embeddings, query_embedding) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:5]
        services = []
        
        SIMILARITY_THRESHOLD = 0.25
        
        for idx in top_indices:
            if similarities[idx] >= SIMILARITY_THRESHOLD:
                doc = documents[idx]
                services.append({
                    'name': doc.get('title', 'Unknown Service'),
                    'title': doc.get('title', 'Unknown Service'),
                    'ministry': doc.get('ministry', 'Government of India'),
                    'icon': doc.get('icon', '📋'),
                    'description': doc.get('text', '')[:200]
                })
        
        # Generate AI answer
        ai_response = generate_ai_answer(msg, services)
        
        # If no good matches, try keyword search
        if not services:
            keyword_results = keyword_search(msg, documents)
            for doc in keyword_results[:3]:
                services.append({
                    'name': doc.get('title', 'Unknown Service'),
                    'title': doc.get('title', 'Unknown Service'),
                    'ministry': doc.get('ministry', 'Government of India'),
                    'icon': doc.get('icon', '📋')
                })
        
        # Generate suggestions based on found services
        suggestions = []
        for service in services[:3]:
            suggestions.append(f"Tell me more about {service['name']}")
        
        if not suggestions:
            suggestions = ['Apply for passport', 'Get driving license', 'Start over']
        
        return {
            'reply': ai_response['answer'],
            'stage': 'AI_SEARCH',
            'services': services,
            'suggestions': suggestions
        }
        
    except Exception as e:
        print(f"AI Search error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'reply': "I apologize, but I couldn't find specific information for that query. Please try asking in a different way or be more specific about the government service you need.",
            'stage': 'AI_SEARCH',
            'suggestions': ['Apply for passport', 'Get driving license', 'Register business']
        }

# ========================================
# MAIN CHAT ENDPOINT
# ========================================

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint with conversation flow
    
    States:
    - GREETING: Initial greeting
    - ASK_HELP: Ask what help is needed
    - AI_SEARCH: Use RAG to answer questions
    """
    try:
        data = request.get_json()
        user_msg = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_msg:
            return jsonify({
                'success': False,
                'error': 'Message is required'
            }), 400
        
        # Get or create session
        session_state = get_session(session_id)
        
        # Get username from authenticated user if available
        user = get_current_user()
        if user and user.get('name'):
            session_state['username'] = user.get('name')
        elif user and user.get('email'):
            session_state['username'] = user.get('email').split('@')[0].capitalize()
        
        # Check for reset command
        if user_msg.lower() in ['reset', 'start over', 'restart']:
            session_state['stage'] = 'GREETING'
            return jsonify({
                'success': True,
                'reply': "Conversation reset! 👋 Say Hi to start fresh.",
                'stage': 'GREETING',
                'suggestions': ['Hi', 'Hello']
            })
        
        # Route based on current stage
        current_stage = session_state.get('stage', 'GREETING')
        
        print(f"🤖 Chat: stage={current_stage}, msg='{user_msg}'")
        
        if current_stage == 'GREETING':
            response = handle_greeting(user_msg, session_state)
        elif current_stage == 'ASK_HELP':
            response = handle_help(user_msg, session_state)
        else:  # AI_SEARCH
            response = handle_ai_search(user_msg, session_state)
        
        # Log engagement if user is authenticated
        if user:
            try:
                current_app.db.engagements.insert_one({
                    'user_id': str(user['_id']),
                    'type': 'chatbot_message',
                    'message': user_msg,
                    'stage': current_stage,
                    'timestamp': datetime.now()
                })
            except:
                pass
        
        return jsonify({
            'success': True,
            **response
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your message',
            'reply': "I'm sorry, something went wrong. Please try again.",
            'suggestions': ['Hi', 'Start over']
        }), 500

@chat_bp.route('/chat/reset', methods=['POST'])
def reset_chat():
    """Reset chat session"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        if session_id in chat_sessions:
            del chat_sessions[session_id]
        
        return jsonify({
            'success': True,
            'message': 'Chat session reset',
            'reply': "Conversation reset! 👋 Say Hi to start.",
            'stage': 'GREETING',
            'suggestions': ['Hi', 'Hello']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
