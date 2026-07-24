from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.notification import Notification
from utils.permissions import current_user, roles_required
from utils.responses import error, success
from utils.validators import json_body

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def list_notifications():
    user = current_user()
    return success({"notifications": [item.to_dict() for item in Notification.query.filter_by(user_id=user.id).order_by(Notification.id.desc()).all()]})

@notifications_bp.route("/<int:notification_id>/read", methods=["PATCH"])
@jwt_required()
def mark_read(notification_id):
    item = db.get_or_404(Notification, notification_id)
    if item.user_id != current_user().id: return error("Notification not found", 404)
    item.is_read = True; db.session.commit()
    return success({"notification": item.to_dict()})

@notifications_bp.route("/", methods=["POST"])
@roles_required("admin", "manager")
def send_notification():
    data, response = json_body(("user_id", "title", "message"))
    if response: return response
    item = Notification(user_id=data["user_id"], title=data["title"], message=data["message"], notification_type=data.get("notification_type", "general"))
    db.session.add(item); db.session.commit()
    return success({"notification": item.to_dict()}, "Notification created", 201)
