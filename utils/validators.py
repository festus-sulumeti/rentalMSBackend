import re

from utils.responses import error

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def json_body(required=()):
    from flask import request
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, error("A JSON request body is required")
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return None, error("Missing required fields", details=missing)
    return data, None


def valid_email(value):
    return isinstance(value, str) and bool(EMAIL_PATTERN.match(value.strip().lower()))


def positive_number(value):
    try:
        return float(value) >= 0
    except (TypeError, ValueError):
        return False
