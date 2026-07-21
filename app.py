import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


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

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
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