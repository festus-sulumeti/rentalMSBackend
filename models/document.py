from datetime import datetime
from extensions import db


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    lease_id = db.Column(db.Integer, db.ForeignKey("leases.id"), index=True)
    property_id = db.Column(db.Integer, db.ForeignKey("properties.id"), index=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(500), nullable=False)
    document_type = db.Column(db.String(50), nullable=False, default="other")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    uploaded_by = db.relationship("User")
    lease = db.relationship("Lease", backref=db.backref("documents", lazy=True, cascade="all, delete-orphan"))
    property = db.relationship("Property", backref=db.backref("documents", lazy=True, cascade="all, delete-orphan"))
    def to_dict(self): return {"id": self.id, "uploaded_by_id": self.uploaded_by_id, "lease_id": self.lease_id, "property_id": self.property_id, "filename": self.filename, "path": self.path, "document_type": self.document_type, "created_at": self.created_at.isoformat()}
