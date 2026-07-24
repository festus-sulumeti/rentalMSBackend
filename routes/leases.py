from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.lease import Lease
from models.unit import Unit
from models.user import User
from utils.helpers import parse_date
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, positive_number

leases_bp = Blueprint("leases", __name__, url_prefix="/leases")

def _can_manage(lease):
    user = current_user()
    return user.role == "admin" or lease.unit.property.owner_id == user.id

@leases_bp.route("/", methods=["POST"])
@jwt_required()
def create_lease():
    data, response = json_body(("unit_id", "tenant_id", "start_date", "end_date", "monthly_rent"))
    if response: return response
    unit = db.session.get(Unit, data["unit_id"]); tenant = db.session.get(User, data["tenant_id"])
    user = current_user()
    if not unit or not tenant: return error("Unit or tenant not found", 404)
    if user.role != "admin" and unit.property.owner_id != user.id: return error("Unit not found", 404)
    if unit.status != "vacant": return error("Unit is not vacant", 409)
    if not positive_number(data["monthly_rent"]): return error("monthly_rent must be non-negative")
    try: start, end = parse_date(data["start_date"], "start_date"), parse_date(data["end_date"], "end_date")
    except ValueError as exc: return error(str(exc))
    if end <= start: return error("end_date must be after start_date")
    lease = Lease(unit_id=unit.id, tenant_id=tenant.id, start_date=start, end_date=end, monthly_rent=data["monthly_rent"], deposit_amount=data.get("deposit_amount", 0))
    unit.status = "occupied"; db.session.add(lease); db.session.commit()
    return success({"lease": lease.to_dict()}, "Lease created successfully", 201)

@leases_bp.route("/", methods=["GET"])
@jwt_required()
def list_leases():
    user = current_user(); query = Lease.query.join(Unit)
    if user.role == "tenant": query = query.filter(Lease.tenant_id == user.id)
    elif user.role != "admin": query = query.filter(Unit.property.has(owner_id=user.id))
    return success({"leases": [lease.to_dict() for lease in query.order_by(Lease.id.desc()).all()]})

@leases_bp.route("/<int:lease_id>", methods=["PUT"])
@jwt_required()
def update_lease(lease_id):
    lease = db.get_or_404(Lease, lease_id)
    if not _can_manage(lease): return error("Lease not found", 404)
    data, response = json_body()
    if response: return response
    for field in ("monthly_rent", "deposit_amount", "status"):
        if field in data: setattr(lease, field, data[field])
    if data.get("status") in {"terminated", "expired"}: lease.unit.status = "vacant"
    db.session.commit(); return success({"lease": lease.to_dict()}, "Lease updated successfully")
