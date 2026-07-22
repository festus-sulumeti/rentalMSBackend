import os

from extensions import db
from models.user import User


def create_default_admin():
    """
    Creates the default administrator
    if one does not already exist.
    """

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        print("Default admin credentials not configured.")
        return

    admin = User.query.filter_by(
        email=admin_email
    ).first()

    if admin:
        print("Default admin already exists.")
        return

    admin = User(
        first_name="System",
        last_name="Administrator",
        email=admin_email,
        role="admin"
    )

    admin.set_password(admin_password)

    db.session.add(admin)
    db.session.commit()

    print("Default administrator created successfully.")