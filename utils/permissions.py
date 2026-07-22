from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models.user import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):

        user = User.query.get(get_jwt_identity())

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        if user.role != "admin":
            return jsonify({
                "message": "Administrator access required"
            }), 403

        return fn(*args, **kwargs)

    return wrapper