from functools import wraps
from flask import request, jsonify
from models.user import User

def get_current_user():
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return None
    return User.query.get(user_id)

def requires_role(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user:
                return jsonify({"error": "unauthorized — send X-User-Id header"}), 401
            if user.status == "inactive":
                return jsonify({"error": "account is inactive"}), 403
            if user.role not in roles:
                return jsonify({"error": f"forbidden — requires one of: {list(roles)}"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({"error": "unauthorized — send X-User-Id header"}), 401
        if user.status == "inactive":
            return jsonify({"error": "account is inactive"}), 403
        return f(*args, **kwargs)
    return wrapper
