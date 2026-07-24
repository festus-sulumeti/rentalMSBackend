from datetime import datetime
from extensions import db


class Unit(db.Model):
    __tablename__ = "units"
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False, index=True)
    unit_number = db.Column(db.String(50), nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False, default=0)
    bathrooms = db.Column(db.Numeric(3, 1), nullable=False, default=1)
    monthly_rent = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="vacant")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    property = db.relationship("Property", backref=db.backref("units", lazy=True, cascade="all, delete-orphan"))
    __table_args__ = (db.UniqueConstraint("property_id", "unit_number", name="uq_unit_property_number"),)

    def to_dict(self):
        return {"id": self.id, "property_id": self.property_id, "unit_number": self.unit_number, "bedrooms": self.bedrooms, "bathrooms": float(self.bathrooms), "monthly_rent": float(self.monthly_rent), "status": self.status, "created_at": self.created_at.isoformat()}
