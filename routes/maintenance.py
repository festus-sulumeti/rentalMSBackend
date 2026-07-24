from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.maintenance import MaintenanceRequest
from models.property import Property
from models.unit import Unit
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body

maintenance_bp = Blueprint("maintenance", __name__, url_prefix="/maintenance")

@maintenance_bp.route("/", methods=["POST"])
@jwt_required()
def create_request():
    data, response = json_body(("property_id", "title", "description"))
    if response: return response
    property = db.session.get(Property, data["property_id"]); user = current_user()
    if not property: return error("Property not found", 404)
    unit_id = data.get("unit_id")
    if unit_id and (not db.session.get(Unit, unit_id) or db.session.get(Unit, unit_id).property_id != property.id): return error("Unit does not belong to property")
    request_record = MaintenanceRequest(property_id=property.id, unit_id=unit_id, requested_by_id=user.id, title=data["title"], description=data["description"], priority=data.get("priority", "medium"))
    db.session.add(request_record); db.session.commit(); return success({"maintenance": request_record.to_dict()}, "Maintenance request created", 201)

@maintenance_bp.route("/", methods=["GET"])
@jwt_required()
def list_requests():
    user = current_user(); query = MaintenanceRequest.query
    if user.role == "tenant": query = query.filter_by(requested_by_id=user.id)
    elif user.role != "admin": query = query.join(Property).filter(Property.owner_id == user.id)
    return success({"maintenance": [item.to_dict() for item in query.order_by(MaintenanceRequest.id.desc()).all()]})

@maintenance_bp.route("/<int:request_id>", methods=["PATCH"])
@jwt_required()
def update_request(request_id):
    item = db.get_or_404(MaintenanceRequest, request_id); user = current_user()
    if user.role != "admin" and item.property.owner_id != user.id: return error("Maintenance request not found", 404)
    data, response = json_body()
    if response: return response
    for field in ("status", "priority"):
        if field in data: setattr(item, field, data[field])
    db.session.commit(); return success({"maintenance": item.to_dict()}, "Maintenance request updated")
