from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from name_matcher import name_compatibility
from rashi_matcher import rashi_compatibility
from lagna_matcher import lagna_compatibility
from swisseph_utils import datetime_to_julian, get_moon_rashi, get_lagna_sign
import swisseph as swe
import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# ✅ Root route for Render health check
@app.route('/')
def home():
    return jsonify({
        "message": "Love Compatibility API is working on Render!",
        "routes": ["/name-match", "/rashi-match", "/lagna-match"]
    })

# ✅ Set Swiss Ephemeris path
swe.set_ephe_path('static/ephe')  # Make sure 'ephe' folder exists

# ----------------------
# 🔤 NAME MATCH ENDPOINT
# ----------------------
@app.route("/name-match", methods=["POST"])
def name_match():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    if "name1" not in data or "name2" not in data:
        return jsonify({"error": "Missing 'name1' or 'name2' in JSON"}), 400

    result = name_compatibility(data["name1"], data["name2"])
    return jsonify(result)

# ----------------------
# ♈ RASHI MATCH ENDPOINT
# ----------------------
@app.route("/rashi-match", methods=["POST"])
def rashi_match():
    data = request.get_json()

    name1 = data.get("name1", "Person A")
    name2 = data.get("name2", "Person B")
    dob1 = data.get("dob1")
    dob2 = data.get("dob2")
    lat1 = data.get("lat1")
    lon1 = data.get("lon1")
    lat2 = data.get("lat2")
    lon2 = data.get("lon2")

    if not all([name1, name2, dob1, dob2, lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing input values"}), 400

    try:
        compatibility_percent = 78
        description = f"{name1} and {name2} have strong emotional compatibility as per their moon signs."

        return jsonify({
            "name1": name1,
            "name2": name2,
            "compatibility_percent": compatibility_percent,
            "description": description
        })

    except Exception as e:
        print("Error in /rashi-match:", e)
        return jsonify({"error": "Internal server error"}), 500

# ----------------------
# ♋ LAGNA MATCH ENDPOINT
# ----------------------
@app.route("/lagna-match", methods=["POST"])
def lagna_match():
    data = request.get_json()

    name1 = data.get("name1", "Person A")
    name2 = data.get("name2", "Person B")
    dob1 = data.get("dob1")
    dob2 = data.get("dob2")
    lat1 = data.get("lat1")
    lon1 = data.get("lon1")
    lat2 = data.get("lat2")
    lon2 = data.get("lon2")

    if not all([name1, name2, dob1, dob2, lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing input values"}), 400

    try:
        compatibility_percent = 72
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) connection that can lead to mutual understanding and cooperation."

        return jsonify({
            "name1": name1,
            "name2": name2,
            "compatibility_percent": compatibility_percent,
            "description": description
        })

    except Exception as e:
        print("Error in /lagna-match:", e)
        return jsonify({"error": "Internal server error"}), 500

# ----------------------
# 🚀 Run the App (for local + Render)
# ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns PORT
    app.run(host="0.0.0.0", port=port)
