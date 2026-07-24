from urllib.parse import urlparse

from flask import Flask, jsonify, request
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

    @app.after_request
    def add_cors_headers(response):
        """Allow configured browser clients to call the JSON API."""
        origin = request.headers.get("Origin")
        parsed_origin = urlparse(origin) if origin else None
        is_localhost = (
            app.config["CORS_ALLOW_LOCALHOST"]
            and parsed_origin is not None
            and parsed_origin.scheme in {"http", "https"}
            and parsed_origin.hostname in {"localhost", "127.0.0.1", "::1"}
        )
        if origin and (origin in app.config["CORS_ORIGINS"] or is_localhost):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response.headers["Vary"] = "Origin"
        return response

    @app.route("/")
    def welcome():
        return jsonify({"status": "success", "message": "Welcome to the Rental Management System API"})

    with app.app_context():
        create_default_admin()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
