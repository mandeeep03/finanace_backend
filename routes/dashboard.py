from flask import Blueprint, jsonify
from services.auth_service import requires_role, requires_auth
from services.record_service import get_summary, get_monthly_trends

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/summary", methods=["GET"])
@requires_auth
def summary():
    return jsonify(get_summary())

@dashboard_bp.route("/trends", methods=["GET"])
@requires_role("analyst", "admin")
def trends():
    return jsonify({"monthly_trends": get_monthly_trends()})
