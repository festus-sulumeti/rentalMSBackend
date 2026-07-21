from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.property import Property

properties_bp = Blueprint(
    "properties",
    __name__,
    url_prefix="/properties"
)