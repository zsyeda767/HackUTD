from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import db  # Use the shared db object

savings_routes = Blueprint('savings_routes', __name__)


class SavingsPlan(db.Model):
    db.model=extend_existing=True
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    last_saved_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@savings_routes.route('/create_savings_plan', methods=['POST'])
def create_savings_plan():
    data = request.get_json()
    user_id = data['user_id']
    user = db.User.query.filter_by(user_id=user_id).first()

    if user:
        new_plan = SavingsPlan(user_id=user.id)
        db.session.add(new_plan)
        db.session.commit()
        return jsonify({'message': 'Savings plan created successfully'}), 201
    else:
        return jsonify({'error': 'User not found'}), 404

@savings_routes.route('/save_daily_income', methods=['POST'])
def save_daily_income():
    data = request.get_json()
    user_id = data['user_id']
    amount = data['amount']
    user = db.User.query.filter_by(user_id=user_id).first()

    if user:
        savings_plan = SavingsPlan.query.filter_by(user_id=user.id).first()
        if savings_plan:
            savings_plan.amount += amount
            savings_plan.last_saved_date = datetime.utcnow()
            db.session.commit()
            return jsonify({'message': 'Savings updated successfully', 'new_balance': savings_plan.amount})
        else:
            return jsonify({'error': 'Savings plan not found'}), 404
    else:
        return jsonify({'error': 'User not found'}), 404
