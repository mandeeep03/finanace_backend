from models.record import Record

def validate_create_record(data):
    errors = {}
    if data.get("amount") is None:
        errors["amount"] = "required"
    else:
        try:
            if float(data["amount"]) <= 0:
                errors["amount"] = "must be a positive number"
        except (ValueError, TypeError):
            errors["amount"] = "must be a valid number"
    if data.get("type") not in Record.TYPES:
        errors["type"] = f"must be one of {Record.TYPES}"
    if not data.get("category") or not str(data["category"]).strip():
        errors["category"] = "required"
    return errors

def validate_update_record(data):
    errors = {}
    if "amount" in data:
        try:
            if float(data["amount"]) <= 0:
                errors["amount"] = "must be a positive number"
        except (ValueError, TypeError):
            errors["amount"] = "must be a valid number"
    if "type" in data and data["type"] not in Record.TYPES:
        errors["type"] = f"must be one of {Record.TYPES}"
    return errors
