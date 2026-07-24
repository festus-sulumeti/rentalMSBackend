from flask import jsonify


def success(data=None, message=None, status=200):
    payload = {"status": "success"}
    if message:
        payload["message"] = message
    if data:
        payload.update(data)
    return jsonify(payload), status


def error(message, status=400, details=None):
    payload = {"status": "error", "message": message}
    if details:
        payload["details"] = details
    return jsonify(payload), status
