from .auth import auth_bp
from .properties import properties_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)