from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from extensions import db
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body required"
        }), 400


    required_fields = [
        "first_name",
        "last_name",
        "email",
        "password"
    ]


    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"{field} is required"
            }), 400


    existing_user = User.query.filter_by(
        email=data["email"]
    ).first()


    if existing_user:
        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 409


    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"]
    )


    user.set_password(
        data["password"]
    )


    db.session.add(user)
    db.session.commit()


    return jsonify({
        "status": "success",
        "message": "User created successfully",
        "user": user.to_dict()
    }), 201



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()


    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body required"
        }), 400


    user = User.query.filter_by(
        email=data.get("email")
    ).first()


    if not user:
        return jsonify({
            "status": "error",
            "message": "Invalid credentials"
        }), 401


    if not user.check_password(
        data.get("password")
    ):
        return jsonify({
            "status": "error",
            "message": "Invalid credentials"
        }), 401



    token = create_access_token(
        identity=str(user.id)
    )


    return jsonify({
        "status": "success",
        "message": "Login successful",
        "access_token": token,
        "user": user.to_dict()
    }), 200