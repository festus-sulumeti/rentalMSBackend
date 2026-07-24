from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from extensions import db
from models.property import Property
from utils.permissions import current_user, roles_required
from utils.responses import error, success
from utils.validators import json_body

properties_bp = Blueprint(
    "properties",
    __name__,
    url_prefix="/properties"
)


@properties_bp.route("/", methods=["POST"])
@jwt_required()
def create_property():
    data, response = json_body(("name", "address", "city", "county", "property_type"))
    if response: return response
    user = current_user()

    property = Property(
        name=data["name"],
        description=data.get("description"),
        address=data["address"],
        city=data["city"],
        county=data["county"],
        property_type=data["property_type"],
        total_units=data.get("total_units", 1),
        owner_id=user.id
    )

    db.session.add(property)
    db.session.commit()

    return success({"property": property.to_dict()}, "Property created successfully", 201)


@properties_bp.route("/", methods=["GET"])
@jwt_required()
def get_properties():
    user = current_user()
    query = Property.query if user.role == "admin" else Property.query.filter_by(owner_id=user.id)
    return success({"properties": [property.to_dict() for property in query.order_by(Property.id.desc()).all()]})


@properties_bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_property(id):
    property = db.get_or_404(Property, id)
    user = current_user()
    if user.role != "admin" and property.owner_id != user.id: return error("Property not found", 404)
    return success({"property": property.to_dict()})


@properties_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_property(id):
    property = db.get_or_404(Property, id); user = current_user()
    if user.role != "admin" and property.owner_id != user.id: return error("Property not found", 404)
    data, response = json_body()
    if response: return response

    property.name = data.get("name", property.name)
    property.description = data.get(
        "description",
        property.description
    )
    property.address = data.get(
        "address",
        property.address
    )
    property.city = data.get(
        "city",
        property.city
    )
    property.county = data.get(
        "county",
        property.county
    )
    property.property_type = data.get(
        "property_type",
        property.property_type
    )
    property.total_units = data.get(
        "total_units",
        property.total_units
    )

    db.session.commit()

    return success({"property": property.to_dict()}, "Property updated successfully")


@properties_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_property(id):
    property = db.get_or_404(Property, id); user = current_user()
    if user.role != "admin" and property.owner_id != user.id: return error("Property not found", 404)

    db.session.delete(property)
    db.session.commit()

    return success(message="Property deleted successfully")
