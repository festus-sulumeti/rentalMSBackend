from flask import Blueprint
from flask_jwt_extended import create_access_token, jwt_required

from extensions import db
from models.user import User
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, valid_email


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@auth_bp.route("/signup", methods=["POST"])
def signup():

    data, response = json_body(("first_name", "last_name", "email", "password"))
    if response: return response
    if not valid_email(data["email"]): return error("A valid email is required")
    if len(data["password"]) < 8: return error("Password must be at least 8 characters")


    existing_user = User.query.filter_by(
        email=data["email"].strip().lower()
    ).first()


    if existing_user:
        return error("Email already exists", 409)


    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"].strip().lower()
    )


    user.set_password(
        data["password"]
    )


    db.session.add(user)
    db.session.commit()


    return success({"user": user.to_dict()}, "User created successfully", 201)



@auth_bp.route("/login", methods=["POST"])
def login():

    data, response = json_body(("email", "password"))
    if response: return response


    user = User.query.filter_by(
        email=data["email"].strip().lower()
    ).first()


    if not user:
        return error("Invalid credentials", 401)


    if not user.check_password(
        data["password"]
    ):
        return error("Invalid credentials", 401)

    if not user.is_active:
        return error("User account is inactive", 403)



    token = create_access_token(
        identity=str(user.id)
    )


    return success({"access_token": token, "user": user.to_dict()}, "Login successful")


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user = current_user()
    if user is None: return error("User not found", 404)
    return success({"user": user.to_dict()})
