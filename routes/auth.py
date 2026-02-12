from flask import Blueprint, request, jsonify, session, current_app
import mysql.connector
from config import Config
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)

db = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE
)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    bcrypt = Bcrypt(current_app)

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s,%s,%s,%s)",
        (data["name"], data["email"], hashed_password, data["role"])
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "User registered successfully"})


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email=%s", (data["email"],))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"message": "User not found"}), 400

    bcrypt = Bcrypt(current_app)

    if not bcrypt.check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid password"}), 400

    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({
        "message": "Login successful",
        "role": user["role"]
    })


@auth_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})
