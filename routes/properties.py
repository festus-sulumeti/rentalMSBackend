from flask import Blueprint, jsonify, request

from extensions import db
from models.property import Property

properties_bp = Blueprint(
    "properties",
    __name__,
    url_prefix="/properties"
)


@properties_bp.route("/", methods=["POST"])
def create_property():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body required"
        }), 400

    required_fields = [
        "name",
        "address",
        "city",
        "county",
        "property_type"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"{field} is required"
            }), 400

    # Temporary owner for development
    owner_id = 3

    property = Property(
        name=data["name"],
        description=data.get("description"),
        address=data["address"],
        city=data["city"],
        county=data["county"],
        property_type=data["property_type"],
        total_units=data.get("total_units", 1),
        owner_id=owner_id
    )

    db.session.add(property)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Property created successfully",
        "property": property.to_dict()
    }), 201


@properties_bp.route("/", methods=["GET"])
def get_properties():

    properties = Property.query.all()

    return jsonify({
        "status": "success",
        "properties": [
            property.to_dict()
            for property in properties
        ]
    }), 200


@properties_bp.route("/<int:id>", methods=["GET"])
def get_property(id):

    property = Property.query.get_or_404(id)

    return jsonify({
        "status": "success",
        "property": property.to_dict()
    }), 200


@properties_bp.route("/<int:id>", methods=["PUT"])
def update_property(id):

    property = Property.query.get_or_404(id)

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Request body required"
        }), 400

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

    return jsonify({
        "status": "success",
        "message": "Property updated successfully",
        "property": property.to_dict()
    }), 200


@properties_bp.route("/<int:id>", methods=["DELETE"])
def delete_property(id):

    property = Property.query.get_or_404(id)

    db.session.delete(property)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "Property deleted successfully"
    }), 200