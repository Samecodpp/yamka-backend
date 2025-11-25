from flask import request, jsonify
from ..services.user_service import register_user, authenticate_user
from . import auth_bp

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not username or not email or not password:
        return jsonify({"message": "username, email and password required"}), 400

    user = register_user(username, email, password)
    if user is None:
        return jsonify({"message": "User already exists or could not be created"}), 409

    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = authenticate_user(email, password)
    if user is None:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200
