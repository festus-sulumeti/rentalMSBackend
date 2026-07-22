import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from extensions import bcrypt, db, jwt
from routes import register_blueprints

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

register_blueprints(app)


@app.route("/")
def welcome():
    return jsonify({
        "message": "Welcome to Rental Management System API",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(debug=True)