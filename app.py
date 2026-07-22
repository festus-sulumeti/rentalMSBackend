import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from extensions import bcrypt, db, jwt
from routes import register_blueprints
from services.auth_service import create_default_admin

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ----------------------------
# Database Configuration
# ----------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ----------------------------
# JWT Configuration
# ----------------------------
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# ----------------------------
# Initialize Extensions
# ----------------------------
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# ----------------------------
# Register Blueprints
# ----------------------------
register_blueprints(app)

# ----------------------------
# Create Default Admin
# ----------------------------
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