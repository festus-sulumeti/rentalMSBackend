import os
from sqlalchemy import inspect

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
        return

    if "users" not in inspect(db.engine).get_table_names():
        return

    admin = User.query.filter_by(
        email=admin_email
    ).first()

    if admin:
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
