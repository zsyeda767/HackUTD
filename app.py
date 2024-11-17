from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a blueprint for app-specific routes
app_routes = Blueprint('app_routes', __name__)

# Assuming SQLAlchemy `db` object is initialized in `main.py`
from main import db

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

# Route to Check Balance
@app_routes.route('/balance', methods=['GET'])
def check_balance():
    user_id = request.args.get('user_id')  # Extract user_id from query params
    user = User.query.filter_by(user_id=user_id).first()
    if user:
        return jsonify({'balance': user.balance})
    else:
        return jsonify({'error': 'User not found'}), 404

# Route to Add Money
@app_routes.route('/add_money', methods=['POST'])
def add_money():
    data = request.get_json()  # Parse JSON request body
    user_id = data.get('user_id')
    amount = data.get('amount')

    if not user_id or not amount or amount <= 0:
        return jsonify({'error': 'Invalid request data'}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if user:
        user.balance += amount
        db.session.commit()
        return jsonify({'new_balance': user.balance, 'message': 'Money added successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404

# Route to Make a Transaction
@app_routes.route('/make_transaction', methods=['POST'])
def make_transaction():
    data = request.get_json()  # Parse JSON request body
    user_id = data.get('user_id')
    amount = data.get('amount')

    if not user_id or not amount or amount <= 0:
        return jsonify({'error': 'Invalid request data'}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if user:
        if user.balance >= amount:
            user.balance -= amount
            db.session.commit()
            return jsonify({'new_balance': user.balance, 'message': 'Transaction successful'})
        else:
            return jsonify({'error': 'Insufficient balance'}), 400
    else:
        return jsonify({'error': 'User not found'}), 404




    


