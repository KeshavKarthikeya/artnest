from flask import Blueprint, jsonify
import mysql.connector
from config import Config

order_bp = Blueprint("order", __name__)

db = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE
)

@order_bp.route("/buy-artwork/<int:art_id>", methods=["POST"])
def buy_artwork(art_id):

    buyer_id = 2  # temporary

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT price FROM artworks WHERE id=%s", (art_id,))
    artwork = cursor.fetchone()

    if not artwork:
        return jsonify({"message": "Artwork not found"}), 404

    price = artwork["price"]

    cursor.execute(
        "INSERT INTO orders (artwork_id, buyer_id, price) VALUES (%s,%s,%s)",
        (art_id, buyer_id, price)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "Artwork purchased successfully"})
