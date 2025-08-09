from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import swisseph as swe
import datetime

from name_matcher import name_compatibility
from rashi_matcher import rashi_compatibility
from lagna_matcher import lagna_compatibility
from swisseph_utils import datetime_to_julian, get_moon_rashi, get_lagna_sign

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Set Swiss Ephemeris path
swe.set_ephe_path('./ephe')  # Change to your actual ephe folder

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


# Helper function for compatibility description
def get_description(name1, name2, compatibility_percent):
    if compatibility_percent >= 91:
        return f"{name1} and {name2} share a balanced ascendant (Lagna) connection that creates an atmosphere of mutual respect, where both appreciate each other’s perspectives. This harmony encourages open dialogue, reduces misunderstandings, and allows for healthy compromises, fostering emotional security and long-term cooperation."
    elif compatibility_percent >= 81:
        return f"{name1} and {name2} share a balanced ascendant (Lagna) connection. When ascendants align in a balanced way, it becomes easier to bridge differences without conflict. Both feel understood and valued, leading to deeper bonds, emotional harmony, and shared goals."
    elif compatibility_percent >= 71:
        return f"{name1} and {name2} share a balanced ascendant (Lagna) connection that naturally promotes cooperation by highlighting shared values and empathy. Differences are handled with patience, turning disagreements into opportunities for growth, and creating a supportive, trust-filled environment."
    elif compatibility_percent >= 61:
        return f"{name1} and {name2} share a balanced ascendant (Lagna). This symbolizes a meeting point of energies that complement each other, allowing smooth communication and intuitive understanding. Both are willing to adapt, compromise, and nurture a lasting relationship."
    elif compatibility_percent >= 51:
        return f"{name1} and {name2} share a balanced ascendant (Lagna). The strength lies in maintaining equality, ensuring neither dominates. Mutual respect becomes the foundation for productive collaboration, leading to shared success and fulfillment."
    elif compatibility_percent >= 41:
        return f"{name1} and {name2} share a balanced ascendant (Lagna). A well-balanced alignment creates space for emotional safety, open communication, and teamwork, enabling both to face challenges together and grow."
    else:
        return f"{name1} and {name2} share a balanced ascendant (Lagna). This connection weaves together understanding, patience, and shared purpose, helping both grow in harmony while respecting each other’s uniqueness."


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
        # Placeholder: replace with actual compatibility logic
        compatibility_percent = 75
        description = get_description(name1, name2, compatibility_percent)

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
        # Placeholder: replace with actual compatibility logic
        compatibility_percent = 55
        description = get_description(name1, name2, compatibility_percent)

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
# 🚀 Run the App
# ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)