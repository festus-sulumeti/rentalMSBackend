from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.user import User
from utils.permissions import current_user, roles_required
from utils.responses import error, success
from utils.validators import json_body

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/", methods=["GET"])
@roles_required("admin", "manager")
def list_users():
    return success({"users": [user.to_dict() for user in User.query.order_by(User.id.desc()).all()]})

@users_bp.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
def update_user(user_id):
    target = db.get_or_404(User, user_id); actor = current_user()
    if actor.id != target.id and actor.role != "admin": return error("User not found", 404)
    data, response = json_body()
    if response: return response
    for field in ("first_name", "last_name"):
        if field in data: setattr(target, field, data[field])
    if actor.role == "admin":
        for field in ("role", "is_active"):
            if field in data: setattr(target, field, data[field])
    db.session.commit()
    return success({"user": target.to_dict()}, "User updated successfully")
