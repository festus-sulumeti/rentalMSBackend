from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.lease import Lease
from models.payment import Payment
from models.unit import Unit
from utils.helpers import parse_date
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, positive_number

payments_bp = Blueprint("payments", __name__, url_prefix="/payments")

def _permitted(lease):
    user = current_user()
    return user.role == "admin" or lease.tenant_id == user.id or lease.unit.property.owner_id == user.id

@payments_bp.route("/", methods=["POST"])
@jwt_required()
def record_payment():
    data, response = json_body(("lease_id", "amount", "paid_on", "method"))
    if response: return response
    lease = db.session.get(Lease, data["lease_id"])
    if not lease or not _permitted(lease): return error("Lease not found", 404)
    if not positive_number(data["amount"]): return error("amount must be non-negative")
    if data.get("reference") and Payment.query.filter_by(reference=data["reference"]).first(): return error("Payment reference already exists", 409)
    try: paid_on = parse_date(data["paid_on"], "paid_on")
    except ValueError as exc: return error(str(exc))
    payment = Payment(lease_id=lease.id, amount=data["amount"], paid_on=paid_on, method=data["method"], reference=data.get("reference"), notes=data.get("notes"))
    db.session.add(payment); db.session.commit()
    return success({"payment": payment.to_dict()}, "Payment recorded successfully", 201)

@payments_bp.route("/", methods=["GET"])
@jwt_required()
def list_payments():
    user = current_user(); query = Payment.query.join(Lease)
    if user.role == "tenant": query = query.filter(Lease.tenant_id == user.id)
    elif user.role != "admin": query = query.join(Unit).filter(Unit.property.has(owner_id=user.id))
    return success({"payments": [payment.to_dict() for payment in query.order_by(Payment.paid_on.desc()).all()]})
