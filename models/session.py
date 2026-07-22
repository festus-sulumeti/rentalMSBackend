from datetime import datetime

from extensions import db


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    jti = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    expires_at = db.Column(
        db.DateTime,
        nullable=False,
    )

    is_revoked = db.Column(
        db.Boolean,
        default=False,
    )