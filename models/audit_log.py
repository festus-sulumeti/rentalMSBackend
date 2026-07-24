from datetime import datetime
from extensions import db


class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(80), nullable=False)
    entity_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user = db.relationship("User", backref=db.backref("audit_logs", lazy=True))
    def to_dict(self): return {"id": self.id, "user_id": self.user_id, "action": self.action, "entity_type": self.entity_type, "entity_id": self.entity_id, "details": self.details, "created_at": self.created_at.isoformat()}
