import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from extensions import db

# Load environment variables
load_dotenv(dotenv_path=".env")

app = Flask(__name__)

# -----------------------------
# Database Configuration
# -----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db.init_app(app)


@app.route("/")
def welcome():
    return jsonify({
        "message": "Welcome to the Rental Management System API",
        "status": "success"
    })


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body is required."
        }), 400

    email = data.get("email")
    password = data.get("password")

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if email == admin_email and password == admin_password:
        return jsonify({
            "status": "success",
            "message": "Login successful.",
            "redirect": "/dashboard"
        }), 200

    return jsonify({
        "status": "error",
        "message": "Invalid email or password."
    }), 401


@app.route("/dashboard")
def dashboard():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Admin Dashboard."
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates tables if they don't already exist

    app.run(debug=True)