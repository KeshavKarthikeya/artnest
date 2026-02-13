from flask import Blueprint, jsonify, session
import mysql.connector
from config import Config

cart_bp = Blueprint("cart", __name__)

db = mysql.connector.connect(
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DATABASE,
    port=Config.MYSQL_PORT
)


# ---------------- ADD TO CART ----------------
@cart_bp.route("/add-to-cart/<int:art_id>", methods=["POST"])
def add_to_cart(art_id):

    buyer_id = session.get("user_id")
    if not buyer_id:
        return jsonify({"message": "Not logged in"}), 401

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO cart (buyer_id, artwork_id) VALUES (%s,%s)",
        (buyer_id, art_id)
    )
    db.commit()
    cursor.close()

    return jsonify({"message": "Added to cart successfully"})


# ---------------- VIEW CART ----------------
@cart_bp.route("/cart", methods=["GET"])
def view_cart():

    buyer_id = session.get("user_id")
    if not buyer_id:
        return jsonify({"message": "Not logged in"}), 401

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT artworks.id, artworks.title, artworks.price, artworks.image
        FROM cart
        JOIN artworks ON cart.artwork_id = artworks.id
        WHERE cart.buyer_id = %s
    """, (buyer_id,))
    items = cursor.fetchall()
    cursor.close()

    return jsonify(items)


# ---------------- CHECKOUT ----------------
@cart_bp.route("/checkout", methods=["POST"])
def checkout():

    buyer_id = session.get("user_id")
    if not buyer_id:
        return jsonify({"message": "Not logged in"}), 401

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT artworks.id, artworks.price
        FROM cart
        JOIN artworks ON cart.artwork_id = artworks.id
        WHERE cart.buyer_id = %s
    """, (buyer_id,))
    items = cursor.fetchall()

    if not items:
        return jsonify({"message": "Cart is empty"}), 400

    total = sum(item["price"] for item in items)

    for item in items:
        cursor.execute(
            "INSERT INTO orders (artwork_id, buyer_id, price) VALUES (%s,%s,%s)",
            (item["id"], buyer_id, item["price"])
        )

    # Clear cart
    cursor.execute("DELETE FROM cart WHERE buyer_id=%s", (buyer_id,))
    db.commit()
    cursor.close()

    return jsonify({"message": "Payment successful", "total": total})
