from flask import Blueprint, request, jsonify
from extensions import db
from models.record import Record
from schemas.record_schema import validate_create_record, validate_update_record
from services.auth_service import requires_role, requires_auth
from services.record_service import get_active_records

records_bp = Blueprint("records", __name__, url_prefix="/records")

@records_bp.route("", methods=["POST"])
@requires_role("admin")
def create_record():
    data = request.get_json() or {}
    errors = validate_create_record(data)
    if errors:
        return jsonify({"errors": errors}), 400
    record = Record(
        amount=float(data["amount"]),
        type=data["type"],
        category=data["category"].strip(),
        date=data.get("date", ""),
        notes=data.get("notes", ""),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@records_bp.route("", methods=["GET"])
@requires_auth
def list_records():
    records = get_active_records(
        type_filter=request.args.get("type"),
        category_filter=request.args.get("category"),
        date_filter=request.args.get("date"),
    )
    return jsonify([r.to_dict() for r in records])

@records_bp.route("/<record_id>", methods=["PUT"])
@requires_role("admin")
def update_record(record_id):
    record = Record.query.filter_by(id=record_id, deleted=False).first()
    if not record:
        return jsonify({"error": "record not found"}), 404
    data = request.get_json() or {}
    errors = validate_update_record(data)
    if errors:
        return jsonify({"errors": errors}), 400
    if "amount" in data:
        record.amount = float(data["amount"])
    for field in ["type", "category", "date", "notes"]:
        if field in data:
            setattr(record, field, data[field])
    db.session.commit()
    return jsonify(record.to_dict())

@records_bp.route("/<record_id>", methods=["DELETE"])
@requires_role("admin")
def delete_record(record_id):
    record = Record.query.filter_by(id=record_id, deleted=False).first()
    if not record:
        return jsonify({"error": "record not found"}), 404
    record.deleted = True
    db.session.commit()
    return jsonify({"message": "record deleted", "id": record_id})
