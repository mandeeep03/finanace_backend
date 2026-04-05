from models.user import User

def validate_create_user(data):
    errors = {}
    if not data.get("name") or not str(data["name"]).strip():
        errors["name"] = "required"
    if data.get("role") not in User.ROLES:
        errors["role"] = f"must be one of {User.ROLES}"
    return errors

def validate_update_status(data):
    errors = {}
    if data.get("status") not in ["active", "inactive"]:
        errors["status"] = "must be 'active' or 'inactive'"
    return errors
