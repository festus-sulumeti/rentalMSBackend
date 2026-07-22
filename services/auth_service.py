import os

from models.user import User
from extensions import db


def create_default_admin():
    admin = User.query.filter_by(
        email=os.getenv("ADMIN_EMAIL")
    ).first()

    if admin:
        return

    admin = User(
        first_name="System",
        last_name="Administrator",
        email=os.getenv("ADMIN_EMAIL"),
        role="admin"
    )

    admin.set_password(
        os.getenv("ADMIN_PASSWORD")
    )

    db.session.add(admin)
    db.session.commit()

    print("✓ Default admin created.")