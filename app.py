from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "dev_secret_key")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

#Dummy user
USER = {
    "email": "user1@example.com",
    "password": "pass123",
    "name": "User Satu"
}

#Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = USER if USER["email"] == data["email"] else None
            if not current_user:
                return jsonify({"error": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


#Endpoint 1
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    # Validasi input non-empty & tipe data benar
    if not data or not isinstance(data, dict):
        return jsonify({"error": "Invalid input format, must be JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({"error": "Email and password must be strings"}), 400

    # Autentikasi user dummy
    if email == USER["email"] and password == USER["password"]:
        token = jwt.encode(
            {
                "sub": USER["email"],
                "email": USER["email"],
                "exp": datetime.utcnow() + timedelta(minutes=15)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


#Endpoint 2 — ITEMS 

@app.route("/items", methods=["GET"])
def get_items():
    items = [
        {"id": 1, "name": "Laptop", "price": 12000000},
        {"id": 2, "name": "Mouse", "price": 250000},
        {"id": 3, "name": "Keyboard", "price": 500000},
    ]
    return jsonify({"items": items}), 200



#Endpoint 3 — PROFILE 
@app.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    name = data.get("name")
    email = data.get("email")

    if not name and not email:
        return jsonify({"error": "At least one field (name or email) must be provided"}), 400

    if name:
        USER["name"] = name
    if email:
        USER["email"] = email

    return jsonify({
        "message": "Profile updated",
        "profile": {"name": USER["name"], "email": USER["email"]}
    }), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
