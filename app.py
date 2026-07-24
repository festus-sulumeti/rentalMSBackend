import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from extensions import bcrypt, db, jwt
from routes import register_blueprints
from services.auth_service import create_default_admin

load_dotenv()

app = Flask(__name__)

database_url = os.getenv("DATABASE_URL")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

register_blueprints(app)

with app.app_context():
    create_default_admin()

@app.route("/")
def welcome():
    return jsonify({
        "status": "success",
        "message": "Welcome to the Rental Management System API"
    })

if __name__ == "__main__":
    app.run(debug=True)