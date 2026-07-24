from extensions import db
from models.expense import Expense
from models.payment import Payment
from models.lease import Lease
from models.unit import Unit


def property_financial_summary(property_id):
    income = db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0)).join(Lease).join(Unit).filter(Unit.property_id == property_id).scalar()
    expenses = db.session.query(db.func.coalesce(db.func.sum(Expense.amount), 0)).filter_by(property_id=property_id).scalar()
    return {"income": float(income), "expenses": float(expenses), "net": float(income - expenses)}
