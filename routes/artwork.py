from flask import Blueprint, request, jsonify, current_app
import mysql.connector
from config import Config
from werkzeug.utils import secure_filename
import os

artwork_bp = Blueprint("artwork", __name__)

db = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE,
    port=Config.MYSQL_PORT
)


@artwork_bp.route("/add-artwork", methods=["POST"])
def add_artwork():
    title = request.form.get("title")
    description = request.form.get("description")
    price = request.form.get("price")
    image = request.files.get("image")

    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)
    else:
        filename = None

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO artworks (artist_id, title, description, price, image) VALUES (%s,%s,%s,%s,%s)",
        (1, title, description, price, filename)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "Artwork added successfully"})


@artwork_bp.route("/artworks", methods=["GET"])
def get_artworks():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM artworks")
    artworks = cursor.fetchall()
    cursor.close()

    return jsonify(artworks)
