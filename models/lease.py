from datetime import datetime
from extensions import db


class Lease(db.Model):
    __tablename__ = "leases"
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), nullable=False, index=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    monthly_rent = db.Column(db.Numeric(12, 2), nullable=False)
    deposit_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default="active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    unit = db.relationship("Unit", backref=db.backref("leases", lazy=True))
    tenant = db.relationship("User", foreign_keys=[tenant_id], backref=db.backref("leases", lazy=True))

    def to_dict(self):
        return {"id": self.id, "unit_id": self.unit_id, "tenant_id": self.tenant_id, "start_date": self.start_date.isoformat(), "end_date": self.end_date.isoformat(), "monthly_rent": float(self.monthly_rent), "deposit_amount": float(self.deposit_amount), "status": self.status, "created_at": self.created_at.isoformat()}
