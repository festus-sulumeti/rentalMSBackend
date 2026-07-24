from datetime import datetime
from extensions import db


class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    incurred_on = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    property = db.relationship("Property", backref=db.backref("expenses", lazy=True, cascade="all, delete-orphan"))
    def to_dict(self): return {"id": self.id, "property_id": self.property_id, "category": self.category, "amount": float(self.amount), "incurred_on": self.incurred_on.isoformat(), "description": self.description, "created_at": self.created_at.isoformat()}
