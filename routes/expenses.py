from flask import Blueprint
from flask_jwt_extended import jwt_required
from extensions import db
from models.expense import Expense
from models.property import Property
from utils.helpers import parse_date
from utils.permissions import current_user
from utils.responses import error, success
from utils.validators import json_body, positive_number

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")

@expenses_bp.route("/", methods=["POST"])
@jwt_required()
def create_expense():
    data, response = json_body(("property_id", "category", "amount", "incurred_on"))
    if response: return response
    property = db.session.get(Property, data["property_id"]); user = current_user()
    if not property or (user.role != "admin" and property.owner_id != user.id): return error("Property not found", 404)
    if not positive_number(data["amount"]): return error("amount must be non-negative")
    try: incurred_on = parse_date(data["incurred_on"], "incurred_on")
    except ValueError as exc: return error(str(exc))
    expense = Expense(property_id=property.id, category=data["category"], amount=data["amount"], incurred_on=incurred_on, description=data.get("description"))
    db.session.add(expense); db.session.commit(); return success({"expense": expense.to_dict()}, "Expense created successfully", 201)

@expenses_bp.route("/", methods=["GET"])
@jwt_required()
def list_expenses():
    user = current_user(); query = Expense.query.join(Property)
    if user.role != "admin": query = query.filter(Property.owner_id == user.id)
    return success({"expenses": [expense.to_dict() for expense in query.order_by(Expense.incurred_on.desc()).all()]})
