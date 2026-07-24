from flask import Blueprint
from flask_jwt_extended import jwt_required
from models.lease import Lease
from models.maintenance import MaintenanceRequest
from models.property import Property
from models.unit import Unit
from utils.permissions import current_user
from utils.responses import success

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard():
    user = current_user()
    properties = Property.query if user.role == "admin" else Property.query.filter_by(owner_id=user.id)
    ids = [item.id for item in properties.all()]
    unit_count = Unit.query.filter(Unit.property_id.in_(ids)).count() if ids else 0
    occupied = Unit.query.filter(Unit.property_id.in_(ids), Unit.status == "occupied").count() if ids else 0
    active = Lease.query.join(Unit).filter(Unit.property_id.in_(ids), Lease.status == "active").count() if ids else 0
    open_requests = MaintenanceRequest.query.filter(MaintenanceRequest.property_id.in_(ids), MaintenanceRequest.status == "open").count() if ids else 0
    return success({"dashboard": {"properties": len(ids), "units": unit_count, "occupied_units": occupied, "active_leases": active, "open_maintenance": open_requests}})
