from flask import Blueprint, request, jsonify, g
from flask_bcrypt import Bcrypt
import re
from ..db import db
from ..models import User
from ..extensions import auth  # Import the shared auth instance

bcrypt = Bcrypt()

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email):
    return bool(EMAIL_REGEX.match(email))

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        g.current_user = user
        return True
    return False

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/users', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    required_fields = ['username', 'email', 'password', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400

    if not validate_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password, name=data['name'])
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user': new_user.to_dict()}), 201

@auth_bp.route('/login', methods=['GET'])
@auth.login_required
def login():
    return jsonify({'message': 'Login successful', 'user': g.current_user.to_dict()}), 200
