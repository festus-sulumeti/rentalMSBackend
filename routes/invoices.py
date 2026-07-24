from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.invoice import Invoice
from models.lease import Lease
from models.unit import Unit
from utils.helpers import parse_date
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, positive_number

invoices_bp = Blueprint("invoices", __name__, url_prefix="/invoices")

@invoices_bp.route("/", methods=["POST"])
@jwt_required()
def create_invoice():
    data, response = json_body(("lease_id", "invoice_number", "amount", "due_date"))
    if response: return response
    lease = db.session.get(Lease, data["lease_id"]); user = current_user()
    if not lease or (user.role != "admin" and lease.unit.property.owner_id != user.id): return error("Lease not found", 404)
    if Invoice.query.filter_by(invoice_number=data["invoice_number"]).first(): return error("Invoice number already exists", 409)
    if not positive_number(data["amount"]): return error("amount must be non-negative")
    try: due_date = parse_date(data["due_date"], "due_date")
    except ValueError as exc: return error(str(exc))
    invoice = Invoice(lease_id=lease.id, invoice_number=data["invoice_number"], amount=data["amount"], due_date=due_date)
    db.session.add(invoice); db.session.commit()
    return success({"invoice": invoice.to_dict()}, "Invoice created", 201)

@invoices_bp.route("/", methods=["GET"])
@jwt_required()
def list_invoices():
    user = current_user(); query = Invoice.query.join(Lease)
    if user.role == "tenant": query = query.filter(Lease.tenant_id == user.id)
    elif user.role != "admin": query = query.join(Unit).filter(Unit.property.has(owner_id=user.id))
    return success({"invoices": [item.to_dict() for item in query.order_by(Invoice.due_date).all()]})
