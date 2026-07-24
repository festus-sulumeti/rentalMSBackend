from decimal import Decimal
from extensions import db
from models.payment import Payment


def lease_payment_total(lease_id):
    total = db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0)).filter_by(lease_id=lease_id, status="completed").scalar()
    return Decimal(total)
