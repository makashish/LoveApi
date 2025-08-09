from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import swisseph as swe
import datetime

# Load .env for local development
load_dotenv()

app = Flask(__name__)
CORS(app)

# ----------------------
# Swiss Ephemeris setup
# ----------------------
swe.set_ephe_path('./ephe')  # make sure ephe folder exists in your project

def get_moon_rashi(jd, lat, lon):
    swe.set_topo(lon, lat, 0)
    moon_long = swe.calc_ut(jd, swe.MOON)[0][0]
    rashi_index = int(moon_long / 30)
    rashis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    return rashis[rashi_index]

def rashi_compatibility(rashi1, rashi2):
    good_pairs = [
        ("Karka", "Vrischika"), ("Mesha", "Dhanu"), ("Tula", "Kumbha")
    ]
    match_pairs = [
        ("Mesha", "Vrischika"), ("Vrishabha", "Kanya"), ("Tula", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Karka")
    ]
    love_pairs = [
        ("Mesha", "Karka"), ("Vrishabha", "Meena"), ("Dhanu", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Simha")
    ]

    if rashi1 == rashi2:
        return 90, "Both share similar emotional traits."
    elif (rashi1, rashi2) in good_pairs or (rashi2, rashi1) in good_pairs:
        return 81, "Create an ascendant harmony that bridges differences and strengthens partnership."
    elif (rashi1, rashi2) in match_pairs or (rashi2, rashi1) in match_pairs:
        return 71, "Emotionally aligned. Great bonding possible."
    elif (rashi1, rashi2) in love_pairs or (rashi2, rashi1) in love_pairs:
        return 61, "Foster a supportive ascendant alignment that deepens trust and unity."
    else:
        return 50, "Some emotional differences may exist."

# ----------------------
# Home route
# ----------------------
@app.route("/")
def home():
    env_type = "Render" if os.environ.get("RENDER") else "Localhost"
    return jsonify({
        "message": "Server is running",
        "environment": env_type,
        "url": "https://loveapi.onrender.com" if env_type == "Render" else f"http://{os.getenv('HOST')}:{os.getenv('PORT')}"
    })

# ----------------------
# Rashi Match Endpoint
# ----------------------
@app.route("/rashi-match", methods=["POST"])
def rashi_match():
    data = request.get_json()

    try:
        name1 = data["name1"]
        name2 = data["name2"]
        dob1 = datetime.datetime.fromisoformat(data["dob1"])
        dob2 = datetime.datetime.fromisoformat(data["dob2"])
        lat1 = float(data["lat1"])
        lon1 = float(data["lon1"])
        lat2 = float(data["lat2"])
        lon2 = float(data["lon2"])
    except Exception:
        return jsonify({"error": "Invalid or missing parameters"}), 400

    jd1 = swe.julday(dob1.year, dob1.month, dob1.day, dob1.hour + dob1.minute / 60)
    jd2 = swe.julday(dob2.year, dob2.month, dob2.day, dob2.hour + dob2.minute / 60)

    rashi1 = get_moon_rashi(jd1, lat1, lon1)
    rashi2 = get_moon_rashi(jd2, lat2, lon2)

    percent, description = rashi_compatibility(rashi1, rashi2)

    return jsonify({
        "name1": name1,
        "rashi1": rashi1,
        "name2": name2,
        "rashi2": rashi2,
        "compatibility_percent": percent,
        "description": description
    })

# ----------------------
# Run app
# ----------------------
if __name__ == "__main__":
    if os.environ.get("RENDER"):
        # Render settings
        port = int(os.environ.get("PORT", 10000))
        app.run(host="0.0.0.0", port=port, debug=False)
    else:
        # Localhost settings from .env
        host = os.getenv("HOST", "localhost")
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("FLASK_DEBUG", "True").lower() == "true"
        app.run(host=host, port=port, debug=debug)