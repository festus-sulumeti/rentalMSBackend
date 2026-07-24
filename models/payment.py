from datetime import datetime
from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey("leases.id"), nullable=False, index=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    paid_on = db.Column(db.Date, nullable=False)
    method = db.Column(db.String(40), nullable=False)
    reference = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), nullable=False, default="completed")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lease = db.relationship("Lease", backref=db.backref("payments", lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {"id": self.id, "lease_id": self.lease_id, "amount": float(self.amount), "paid_on": self.paid_on.isoformat(), "method": self.method, "reference": self.reference, "status": self.status, "notes": self.notes, "created_at": self.created_at.isoformat()}
