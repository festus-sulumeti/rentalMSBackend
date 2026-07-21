import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

# Load environment variables from the .env file
load_dotenv(dotenv_path=".env")

app = Flask(__name__)


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

    # Debug (remove these in production)
    print(f"Expected Email: {admin_email}")
    print(f"Expected Password: {admin_password}")
    print(f"Received Email: {email}")
    print(f"Received Password: {password}")

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
    app.run(debug=True)