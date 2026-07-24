from datetime import datetime
from extensions import db


class Invoice(db.Model):
    __tablename__ = "invoices"
    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey("leases.id"), nullable=False, index=True)
    invoice_number = db.Column(db.String(50), nullable=False, unique=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lease = db.relationship("Lease", backref=db.backref("invoices", lazy=True, cascade="all, delete-orphan"))
    def to_dict(self): return {"id": self.id, "lease_id": self.lease_id, "invoice_number": self.invoice_number, "amount": float(self.amount), "due_date": self.due_date.isoformat(), "status": self.status, "created_at": self.created_at.isoformat()}
