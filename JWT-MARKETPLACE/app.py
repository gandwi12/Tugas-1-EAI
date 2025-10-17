from flask import Flask, request, jsonify, Response, g
import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv
import os
from flask_cors import CORS
import logging
import json


load_dotenv()
app = Flask(__name__)
CORS(app)

JWT_SECRET = os.getenv("JWT_SECRET")
PORT = int(os.getenv("PORT", 5000))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


USERS_DB = {
    "user1@example.com": {"name": "Helmi User", "password": "pass123", "role": "user"},
    "admin@example.com": {"name": "Admin User", "password": "adminpass", "role": "admin"}
}


ITEMS = [
    {"id": 1, "name": "Kopi Hitam", "price": 15000},
    {"id": 2, "name": "Teh Tarik", "price": 12000},
    {"id": 3, "name": "Es Coklat", "price": 18000}
]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = auth_header.split(" ")[1]
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            g.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role = g.user.get("role")
            if role != required_role:
                return jsonify({"error": "Forbidden, role not allowed"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(isinstance(data.get(k), str) and data.get(k) for k in ("email","password")):
        return jsonify({"error": "Invalid input"}), 400

    email = data["email"]
    password = data["password"]

    user = USERS_DB.get(email)
    if not user or user["password"] != password:
        logging.warning(f"Failed login attempt for {email}")
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": email,
        "email": email,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    logging.info(f"User '{email}' logged in")
    return Response(json.dumps({"access_token": token}, indent=4), mimetype="application/json"), 200

@app.route("/items", methods=["GET"])
def get_items():
    return Response(json.dumps({"items": ITEMS}, indent=4), mimetype="application/json"), 200

@app.route("/profile", methods=["PUT"])
@token_required
def update_profile():
    data = request.get_json()
    if not data or (not data.get("name") and not data.get("email")):
        return jsonify({"error": "At least one field required"}), 400

    email = g.user.get("email")
    user = USERS_DB.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    new_email = data.get("email")
    if new_email and new_email not in USERS_DB:
        return jsonify({"error": "User not found"}), 404

    if data.get("name"):
        user["name"] = data["name"]
    if data.get("email"):
        USERS_DB[data["email"]] = user
        del USERS_DB[email]

    logging.info(f"User updated profile: {user}")
    return Response(json.dumps({"message": "Profile updated", "profile": {"name": user["name"], "email": data.get('email', email)}}, indent=4), mimetype="application/json"), 200

@app.route("/auth/refresh", methods=["POST"])
@token_required
def refresh_token():
    email = g.user.get("email")
    user = USERS_DB.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    payload = {
        "sub": email,
        "email": email,
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    new_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    if isinstance(new_token, bytes):
        new_token = new_token.decode("utf-8")

    logging.info(f"Token refreshed for {email}")
    return Response(json.dumps({"access_token": new_token}, indent=4), mimetype="application/json"), 200


@app.route("/admin-only", methods=["GET"])
@token_required
@role_required("admin")
def admin_only():
    return Response(json.dumps({"message": "Welcome admin!"}, indent=4), mimetype="application/json"), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
