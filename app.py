import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# === API KEY (UPDATED) ===
API_KEY = os.environ.get("API_KEY", "6442851093:7ocdcXMi")

LIMIT = 300
LANG = "ru"
URL = "https://leakosintapi.com/"

@app.route("/")
def home():
    return {"status": "running"}

# === LEAK LOOKUP API (PLAIN JSON) ===
@app.route("/leak", methods=["GET"])
def leak_lookup():
    key = request.args.get("key")
    query = request.args.get("id")

    # Validate key
    if not key:
        return jsonify({"error": "key required"}), 400

    if key != API_KEY:
        return jsonify({"error": "invalid key"}), 401

    # Validate id
    if not query:
        return jsonify({"error": "id required"}), 400

    payload = {
        "token": API_KEY,
        "request": query.strip(),
        "limit": LIMIT,
        "lang": LANG
    }

    try:
        r = requests.post(URL, json=payload, timeout=25)
        data = r.json()
    except Exception as e:
        return jsonify({"error": f"api error: {e}"}), 500

    if "Error code" in data:
        return jsonify({"error": data.get("Error code")}), 400

    return jsonify(data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)