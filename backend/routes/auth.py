from flask import Blueprint, request, jsonify, current_app
from models.user import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps

bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_model = User(current_app.db)
            current_user = user_model.find_by_id(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        print(f"Registration request received: {data}")  # Debug log
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name']
        email = data['email'].lower().strip()
        password = data['password']
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Check if user already exists
        user_model = User(current_app.db)
        existing_user = user_model.find_by_email(email)
        
        if existing_user:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Create user with new fields
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password.decode('utf-8'),
            'age': data.get('age'),  # NEW: Age field
            'location': data.get('location'),  # NEW: Location field
            'job': data.get('job'),  # NEW: Job field
            'role': 'citizen',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'ai_categories': [],
            'search_count': 0,
            'ad_clicks': 0
        }
        
        user_id = user_model.create(user_data)
        
        # Generate token
        token = jwt.encode(
            {
                'user_id': user_id,
                'email': email,
                'exp': datetime.utcnow() + timedelta(days=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        print(f"User created successfully: {email}")  # Debug log
        
        return jsonify({
            'success': True,  # Added success flag
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'name': name,
                'email': email,
                'role': 'citizen'
            }
        }), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Registration failed: {str(e)}'}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        print(f"Login request received: {data.get('email', 'N/A')}")  # Debug log
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user
        user_model = User(current_app.db)
        user = user_model.find_by_email(email)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = jwt.encode(
            {
                'user_id': str(user['_id']),
                'email': user['email'],
                'exp': datetime.utcnow() + timedelta(days=30)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        
        print(f"User logged in successfully: {email}")  # Debug log
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'role': user.get('role', 'citizen')
            }
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Login failed: {str(e)}'}), 500

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    try:
        return jsonify({
            'user': {
                'id': str(current_user['_id']),
                'name': current_user['name'],
                'email': current_user['email'],
                'role': current_user.get('role', 'citizen'),
                'ai_categories': current_user.get('ai_categories', []),
                'search_count': current_user.get('search_count', 0),
                'ad_clicks': current_user.get('ad_clicks', 0)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/change-password', methods=['POST'])
@token_required
def change_password(current_user):
    try:
        data = request.get_json()
        
        if 'current_password' not in data or 'new_password' not in data:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), current_user['password'].encode('utf-8')):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        if len(new_password) < 6:
            return jsonify({'error': 'New password must be at least 6 characters'}), 400
        
        # Hash new password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
        
        # Update password
        user_model = User(current_app.db)
        user_model.update(str(current_user['_id']), {
            'password': hashed_password.decode('utf-8'),
            'updated_at': datetime.utcnow()
        })
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500