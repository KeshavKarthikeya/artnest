from flask import Flask, render_template
from flask_bcrypt import Bcrypt
import os
from config import Config

# -------- Create App FIRST --------

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config.from_object(Config)

bcrypt = Bcrypt(app)
# -------- Upload Folder --------
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------- Import Blueprints AFTER app created --------
from routes.auth import auth_bp
from routes.artwork import artwork_bp
from routes.order import order_bp
from routes.cart import cart_bp

# -------- Register Blueprints --------
app.register_blueprint(auth_bp)
app.register_blueprint(artwork_bp)
app.register_blueprint(order_bp)
app.register_blueprint(cart_bp)

# -------- Pages --------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register-page")
def register_page():
    return render_template("register.html")

@app.route("/login-page")
def login_page():
    return render_template("login.html")

@app.route("/artist-dashboard")
def artist_dashboard():
    return render_template("artist-dashboard.html")

@app.route("/buyer-dashboard")
def buyer_dashboard():
    return render_template("buyer-dashboard.html")
@app.route("/cart-page")
def cart_page():
    return render_template("cart.html")


# -------- Run --------
if __name__ == "__main__":
    app.run()

