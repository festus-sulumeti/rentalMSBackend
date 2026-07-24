from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from models.user import User
from extensions import db


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if user is None:
            return jsonify({
                "status": "error",
                "message": "User not found"
            }), 404

        if user.role != "admin":
            return jsonify({
                "status": "error",
                "message": "Administrator access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper


def current_user():
    verify_jwt_in_request()
    return db.session.get(User, int(get_jwt_identity()))


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user()
            if user is None:
                return jsonify({"status": "error", "message": "User not found"}), 404
            if not user.is_active:
                return jsonify({"status": "error", "message": "User account is inactive"}), 403
            if user.role not in roles:
                return jsonify({"status": "error", "message": "Insufficient permissions"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
