from datetime import datetime

from extensions import db


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    address = db.Column(
        db.String(255),
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    county = db.Column(
        db.String(100),
        nullable=False
    )

    property_type = db.Column(
        db.String(50),
        nullable=False
    )

    total_units = db.Column(
        db.Integer,
        default=1
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    owner = db.relationship(
        "User",
        backref=db.backref(
            "properties",
            lazy=True
        )
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "city": self.city,
            "county": self.county,
            "property_type": self.property_type,
            "total_units": self.total_units,
            "is_active": self.is_active,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat()
            if self.created_at
            else None,
        }