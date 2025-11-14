from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, db
import traceback

bp = Blueprint('auth_blueprint', __name__)

@bp.route('/register', methods=['POST'])
def register():
    current_app.logger.info("User registration attempt")
    
    try:
        # Validate request data
        if not request.is_json:
            current_app.logger.warning("Registration request missing JSON content type")
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        if not data:
            current_app.logger.warning("Registration request with empty JSON body")
            return jsonify({'error': 'Request body is empty'}), 400
        
        # Validate required fields
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            current_app.logger.warning(f"Registration attempt with missing fields - username: {bool(username)}, password: {bool(password)}")
            return jsonify({'error': 'Username and password are required'}), 400
        
        current_app.logger.info(f"Registration attempt for username: {username}")
        
        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            current_app.logger.warning(f"Registration failed - username already exists: {username}")
            return jsonify({'error': 'Username already exists'}), 400
        
        # Create new user
        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(user)
        db.session.commit()
        
        current_app.logger.info(f"User registered successfully: {username}")
        return jsonify({'message': 'User created successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Registration error: {str(e)}\nTraceback: {traceback.format_exc()}")
        return jsonify({'error': 'Registration failed'}), 500

@bp.route('/login', methods=['POST'])
def login():
    current_app.logger.info("User login attempt")
    
    try:
        # Validate request data
        if not request.is_json:
            current_app.logger.warning("Login request missing JSON content type")
            return jsonify({'error': 'Request must be JSON'}), 400
        
        data = request.get_json()
        
        if not data:
            current_app.logger.warning("Login request with empty JSON body")
            return jsonify({'error': 'Request body is empty'}), 400
        
        # Validate required fields
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            current_app.logger.warning(f"Login attempt with missing fields - username: {bool(username)}, password: {bool(password)}")
            return jsonify({'error': 'Username and password are required'}), 400
        
        current_app.logger.info(f"Login attempt for username: {username}")
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            current_app.logger.warning(f"Login failed - user not found: {username}")
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check password
        if check_password_hash(user.password_hash, password):
            login_user(user)
            current_app.logger.info(f"User logged in successfully: {username}")
            return jsonify({'username': user.username}), 200
        else:
            current_app.logger.warning(f"Login failed - incorrect password for user: {username}")
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}\nTraceback: {traceback.format_exc()}")
        return jsonify({'error': 'Login failed'}), 500