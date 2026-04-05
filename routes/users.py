from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from schemas.user_schema import validate_create_user, validate_update_status
from services.auth_service import requires_role

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    errors = validate_create_user(data)
    if errors:
        return jsonify({"errors": errors}), 400
    user = User(name=data["name"].strip(), role=data["role"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@users_bp.route("", methods=["GET"])
@requires_role("admin")
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@users_bp.route("/<user_id>/status", methods=["PATCH"])
@requires_role("admin")
def update_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    data = request.get_json() or {}
    errors = validate_update_status(data)
    if errors:
        return jsonify({"errors": errors}), 400
    user.status = data["status"]
    db.session.commit()
    return jsonify(user.to_dict())
