import os
import re
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "6442851093:tfmX8vto")


def validate_key(req):
    key = (
        req.headers.get("X-API-KEY")
        or req.args.get("key")
        or (req.json.get("key") if req.is_json else None)
    )
    return key == API_KEY


def detect_type(value):
    value = value.strip()

    # Phone detection (10–15 digits)
    if re.fullmatch(r"[0-9]{10,15}", value):
        return "phone"

    # Email detection
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value):
        return "email"

    # Username (letters + numbers + _)
    if re.fullmatch(r"[A-Za-z0-9_\.]+", value):
        return "username"

    return "unknown"


@app.route("/leak", methods=["POST"])
def leak_lookup():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    body = request.get_json()

    if "id" not in body:
        return jsonify({"error": "id is required"}), 400

    if not validate_key(request):
        return jsonify({"error": "invalid api key"}), 401

    lookup_id = body["id"].strip()

    # Detect type
    dtype = detect_type(lookup_id)

    # Generate response based on type
    if dtype == "phone":
        info = {
            "type": "phone",
            "length": len(lookup_id),
            "formatted": f"+91{lookup_id}" if len(lookup_id) == 10 else lookup_id,
            "valid": True
        }

    elif dtype == "email":
        username, domain = lookup_id.split("@", 1)
        info = {
            "type": "email",
            "username": username,
            "domain": domain,
            "valid": True
        }

    elif dtype == "username":
        info = {
            "type": "username",
            "length": len(lookup_id),
            "valid": True
        }

    else:
        info = {
            "type": "unknown",
            "valid": False
        }

    return jsonify({
        "success": True,
        "input": lookup_id,
        "detected_type": dtype,
        "data": info
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
