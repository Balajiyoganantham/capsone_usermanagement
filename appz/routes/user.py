from flask import Blueprint, request, jsonify
from ..db import db
from ..models import User
from ..extensions import auth  # Import the shared auth instance
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_dict() for user in users]}), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    if 'username' in data:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Username already taken'}), 409
        user.username = data['username']

    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({'error': 'Email already taken'}), 409
        user.email = data['email']

    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    if 'name' in data:
        user.name = data['name']

    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200
