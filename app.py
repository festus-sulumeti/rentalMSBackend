from flask import Flask, jsonify
from extensions import bcrypt, db, jwt
from routes import register_blueprints
from services.auth_service import create_default_admin
from config import Config

def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    register_blueprints(app)

    @app.route("/")
    def welcome():
        return jsonify({"status": "success", "message": "Welcome to the Rental Management System API"})

    with app.app_context():
        create_default_admin()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
