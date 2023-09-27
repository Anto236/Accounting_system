from flask import Blueprint, request, jsonify
from . import db
from .models.account import Account
from .models.base_model import BaseModel
from .models.transaction import Transaction
from .models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    else:
        return jsonify({"message": "Incorrect email or password"}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"message": "Missing email, username, or password"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(email=email, username=username, password_hash=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully"}), 201
