from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.property import Property
from models.unit import Unit
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, positive_number

units_bp = Blueprint("units", __name__, url_prefix="/units")

def _property_for_user(property_id):
    property = db.session.get(Property, property_id)
    user = current_user()
    return property if property and (user.role == "admin" or property.owner_id == user.id) else None

@units_bp.route("/", methods=["POST"])
@jwt_required()
def create_unit():
    data, response = json_body(("property_id", "unit_number", "monthly_rent"))
    if response: return response
    if not positive_number(data["monthly_rent"]): return error("monthly_rent must be a non-negative number")
    if not _property_for_user(data["property_id"]): return error("Property not found", 404)
    if Unit.query.filter_by(property_id=data["property_id"], unit_number=str(data["unit_number"])).first(): return error("Unit number already exists for this property", 409)
    unit = Unit(property_id=data["property_id"], unit_number=str(data["unit_number"]), bedrooms=data.get("bedrooms", 0), bathrooms=data.get("bathrooms", 1), monthly_rent=data["monthly_rent"], status=data.get("status", "vacant"))
    db.session.add(unit); db.session.commit()
    return success({"unit": unit.to_dict()}, "Unit created successfully", 201)

@units_bp.route("/", methods=["GET"])
@jwt_required()
def list_units():
    property_id = request.args.get("property_id", type=int)
    user = current_user(); query = Unit.query.join(Property)
    if user.role != "admin": query = query.filter(Property.owner_id == user.id)
    if property_id: query = query.filter(Unit.property_id == property_id)
    return success({"units": [unit.to_dict() for unit in query.order_by(Unit.id.desc()).all()]})

@units_bp.route("/<int:unit_id>", methods=["PUT"])
@jwt_required()
def update_unit(unit_id):
    unit = db.get_or_404(Unit, unit_id)
    if not _property_for_user(unit.property_id): return error("Unit not found", 404)
    data, response = json_body()
    if response: return response
    for field in ("unit_number", "bedrooms", "bathrooms", "monthly_rent", "status"):
        if field in data: setattr(unit, field, data[field])
    db.session.commit(); return success({"unit": unit.to_dict()}, "Unit updated successfully")
