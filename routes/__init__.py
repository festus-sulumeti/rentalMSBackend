from .auth import auth_bp
from .properties import properties_bp
from .units import units_bp
from .leases import leases_bp
from .payments import payments_bp
from .expenses import expenses_bp
from .maintenance import maintenance_bp
from .notifications import notifications_bp
from .invoices import invoices_bp
from .users import users_bp
from .dashboard import dashboard_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(properties_bp)
    app.register_blueprint(units_bp)
    app.register_blueprint(leases_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(maintenance_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(invoices_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(dashboard_bp)
