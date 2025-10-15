from flask import Flask, request, jsonify, render_template
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os
from flask_cors import CORS
import json

load_dotenv()
app = Flask(__name__)
CORS(app)

JWT_SECRET = os.getenv("JWT_SECRET")
PORT = int(os.getenv("PORT", 5000))

USER = {
    "email": "user1@example.com",
    "password": "pass123",
    "name": "Demo User"
}

ITEMS = [
    {"id": 1, "name": "Kopi Hitam", "price": 15000},
    {"id": 2, "name": "Teh Tarik", "price": 12000},
    {"id": 3, "name": "Es Coklat", "price": 18000}
]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        token = auth_header.split(" ")[1]
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated



@app.route("/")
def home():
    return render_template("index.html")



@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if email == USER["email"] and password == USER["password"]:
        payload = {
            "sub": email,
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        return app.response_class(
            response=json.dumps({"access_token": token}, separators=(',', ': ')),
            status=200,
            mimetype="application/json"
        )
    else:
        return app.response_class(
            response=json.dumps({"error": "Invalid credentials"}, separators=(',', ': ')),
            status=401,
            mimetype="application/json"
        )



@app.route("/items", methods=["GET"])
def get_items():
    return app.response_class(
        response=json.dumps({"items": ITEMS}, separators=(',', ': ')),
        status=200,
        mimetype="application/json"
    )



@app.route("/profile", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name and not email:
        return app.response_class(
            response=json.dumps({"error": "At least one field (name/email) required"}, separators=(',', ': ')),
            status=400,
            mimetype="application/json"
        )

    USER["name"] = name or USER["name"]
    USER["email"] = email or USER["email"]

    return app.response_class(
        response=json.dumps({
            "message": "Profile updated",
            "profile": {"name": USER["name"], "email": USER["email"]}
        }, separators=(',', ': ')),
        status=200,
        mimetype="application/json"
    )



@app.route("/auth/refresh", methods=["POST"])
@token_required
def refresh_token():
    user_email = request.user.get("email")
    payload = {
        "sub": user_email,
        "email": user_email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    new_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return app.response_class(
        response=json.dumps({"access_token": new_token}, separators=(',', ': ')),
        status=200,
        mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
