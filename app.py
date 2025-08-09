from flask import Flask, request, jsonify
from flask_cors import CORS

from name_matcher import name_compatibility
from rashi_matcher import rashi_compatibility
from lagna_matcher import lagna_compatibility
from swisseph_utils import datetime_to_julian, get_moon_rashi, get_lagna_sign
import swisseph as swe
import datetime

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Set Swiss Ephemeris path
swe.set_ephe_path('./ephe')  # ✅ Change this to your actual ephe folder

# ----------------------
# 🔤 NAME MATCH ENDPOINT
# ----------------------
@app.route("/name-match", methods=["POST"])
def name_match():
    data = request.get_json()  # ✅ Correct method

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

    # ✅ Basic validation
    if not all([name1, name2, dob1, dob2, lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing input values"}), 400

    try:
        # ✅ Placeholder logic (can be replaced with real Rashi match logic)
        compatibility_percent = 78  # you can randomize or calculate this later
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

    # ✅ Basic validation
    if not all([name1, name2, dob1, dob2, lat1, lon1, lat2, lon2]):
        return jsonify({"error": "Missing input values"}), 400

    try:
        # ✅ Placeholder logic (replace with real Lagna logic later)
        compatibility_percent >= 91  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) connection that is A balanced ascendant connection can create an atmosphere of mutual respect, where both individuals appreciate each other’s perspectives. This harmony encourages open dialogue, reduces misunderstandings, and allows for healthy compromises. Such alignment fosters emotional security and strengthens the foundation for long-term cooperation in personal, professional, or creative partnerships."
        compatibility_percent >= 81  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) connection, explain by When ascendants align in a balanced way, it becomes easier to bridge differences without conflict. Each person feels understood and valued, leading to a deeper bond. This kind of connection not only nurtures emotional harmony but also inspires shared goals, trust, and a willingness to work together effectively."
        compatibility_percent >= 71  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) connection that is A harmonious ascendant relationship naturally promotes cooperation by highlighting shared values and mutual empathy. Differences are handled with patience, and disagreements transform into opportunities for growth. In such a connection, both individuals contribute equally to the relationship, building a supportive environment where trust and collaboration thrive without unnecessary tension."
        compatibility_percent >= 61  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) In astrology, a balanced ascendant connection symbolizes a meeting point of energies that complement each other. This alignment allows for smooth communication and an intuitive understanding of one anothers needs. As a result, both partners are more willing to adapt, compromise, and nurture a lasting relationship based on cooperation and harmony."

        compatibility_percent >= 51  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) The strength of a balanced ascendant connection lies in its ability to maintain equality between two individuals. It ensures neither dominates the relationship, allowing both to feel empowered and valued. Such mutual respect becomes the foundation for productive collaboration, where joint efforts consistently lead to shared success and fulfillment."
        compatibility_percent >= 41 # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna)A well-balanced ascendant alignment creates space for emotional safety, open communication, and teamwork. It supports each person’s individuality while reinforcing their shared vision. This combination of independence and unity enables both partners to face challenges together, turning obstacles into opportunities and strengthening their commitment to mutual growth and cooperation."
        compatibility_percent = 30  # adjust as needed
        description = f"{name1} and {name2} share a balanced ascendant (Lagna) A balanced ascendant connection weaves together understanding, patience, and shared purpose, enabling both individuals to grow in harmony while respecting each other’s uniqueness; this mutual alignment nurtures cooperation, reduces conflict, and transforms the relationship into a supportive partnership where both feel equally valued and inspired to achieve common dreams."

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
    app.run(debug=True)