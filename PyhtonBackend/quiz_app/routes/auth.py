from flask import Blueprint, request, jsonify
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.models import User, db

bp = Blueprint('auth_blueprint', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'username': user.username}),200
    return jsonify({'error': 'Invalid credentials'}), 401