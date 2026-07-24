from datetime import datetime
from extensions import db


class MaintenanceRequest(db.Model):
    __tablename__ = "maintenance_requests"
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), nullable=False, index=True)
    unit_id = db.Column(db.Integer, db.ForeignKey("units.id"), index=True)
    requested_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), nullable=False, default="medium")
    status = db.Column(db.String(20), nullable=False, default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    property = db.relationship("Property", backref=db.backref("maintenance_requests", lazy=True))
    unit = db.relationship("Unit", backref=db.backref("maintenance_requests", lazy=True))
    requested_by = db.relationship("User", foreign_keys=[requested_by_id])
    def to_dict(self): return {"id": self.id, "property_id": self.property_id, "unit_id": self.unit_id, "requested_by_id": self.requested_by_id, "title": self.title, "description": self.description, "priority": self.priority, "status": self.status, "created_at": self.created_at.isoformat()}
