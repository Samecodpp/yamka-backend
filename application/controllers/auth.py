from flask import request, jsonify
from marshmallow import ValidationError
from ..services.user_service import register_user, authenticate_user
from ..schemas import UserSchema, UserRegisterSchema, UserLoginSchema
from . import auth_bp

user_schema = UserSchema()
register_schema = UserRegisterSchema()
login_schema = UserLoginSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        validated_data = register_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = register_user(validated_data['username'], validated_data['email'], validated_data['password'])
    if user is None:
        return jsonify({"message": "User already exists or could not be created"}), 409

    return user_schema.dump(user), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        validated_data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    user = authenticate_user(validated_data['email'], validated_data['password'])
    if user is None:
        return jsonify({"message": "Invalid credentials"}), 401

    return user_schema.dump(user), 200
