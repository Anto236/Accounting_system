from flask import Blueprint, jsonify, request
from . import db
from .models.account import Account
from .models.transaction import Transaction
from .models.user import User
from flask_login import login_required, current_user
from sqlalchemy import desc

views = Blueprint('views', __name__)

@views.route('/')
def landing_page():
    return jsonify({"message": "Welcome to the accounting system!"})

@views.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Create a new User object
    new_user = User(username=username, email=email, password=password)

    # Add the new_user to the session
    db.session.add(new_user)

    # Commit the session to save the new user in the database
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@views.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    accounts = Account.query.all()
    account_list = []

    for account in accounts:
        account_data = {
            'id': account.id,
            'name': account.name,
            'balance': account.balance
        }
        account_list.append(account_data)

    return jsonify(account_list)

@views.route('/transactions', methods=['GET'])
@login_required
def get_transactions():
    transactions = Transaction.query.filter_by(account_id=current_user.id).order_by(desc(Transaction.date)).all()
    transaction_list = []

    for transaction in transactions:
        transaction_data = {
            'id': transaction.id,
            'amount': transaction.amount,
            'transaction_type': transaction.transaction_type,
            'date': transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
            'account_id': transaction.account_id
        }
        transaction_list.append(transaction_data)

    return jsonify(transaction_list)

@views.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    email = data.get('email')  # Add an 'email' parameter to the request data

    # Look up the user by email
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({"message": "Invalid deposit amount"}), 400

    # Check if the user already has an account
    account = Account.query.filter_by(user_id=user.id).first()

    if not account:
        # If the user doesn't have an account, create a new one
        account = Account(name="Default Account", user_id=user.id, balance=0.0)
        db.session.add(account)
        db.session.commit()

    # Perform the deposit for the found user and account
    account.balance += amount
    transaction = Transaction(amount=amount, transaction_type="deposit", account_id=account.id)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Deposit successful"})

@views.route('/withdrawal', methods=['POST'])
def withdrawal():
    data = request.get_json()
    amount = data.get('amount')

    if not amount or amount <= 0:
        return jsonify({"message": "Invalid withdrawal amount"}), 400

    account = Account.query.get(current_user.id)

    if not account:
        return jsonify({"message": "Account not found"}), 404

    if account.balance < amount:
        return jsonify({"message": "Insufficient balance"}), 400

    account.balance -= amount
    transaction = Transaction(amount=amount, transaction_type="withdrawal", account_id=current_user.id)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Withdrawal successful"})
