from flask import Flask, jsonify, request
from flask_cors import CORS
from extensions import db  # Import db from extensions.py
from app import app_routes
from savings import savings_routes

# Initialize the Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banking.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Enable CORS for all routes
CORS(app)

# Register blueprints
app.register_blueprint(app_routes, url_prefix="/app")
app.register_blueprint(savings_routes, url_prefix="/savings")

# Create database tables
with app.app_context():
    db.create_all()
    print("Database initialized!")

# General API routes
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Flask!"})

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({"received": data})

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)








