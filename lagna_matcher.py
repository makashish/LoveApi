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

def get_lagna(jd, lat, lon):
    houses, ascmc = swe.houses_ex(jd, lat, lon, b'A')
    asc = ascmc[0]
    lagna_index = int(asc / 30)
    rashis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    return rashis[lagna_index]

def lagna_compatibility(lagna1, lagna2):
    if lagna1 == lagna2:
        return 85, "Excellent physical and mental resonance."
    
    good_pairs = [
        ("Mesha", "Simha"), ("Vrishabha", "Tula"), ("Tula", "Makara"),
        ("Karka", "Meena"), ("Vrischika", "Karka")
    ]
    match_pairs = [
        ("Mesha", "Vrischika"), ("Vrishabha", "Kanya"), ("Tula", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Karka")
    ]
    love_pairs = [
        ("Mesha", "Karka"), ("Vrishabha", "Meena"), ("Dhanu", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Simha")
    ]

    if (lagna1, lagna2) in good_pairs or (lagna2, lagna1) in good_pairs:
        return 90, "Cultivate a harmonious ascendant bond that fosters trust and collaboration."
    elif (lagna1, lagna2) in match_pairs or (lagna2, lagna1) in match_pairs:
        return 81, "Build an ascendant relationship rooted in balance, paving the way for shared respect and unity."
    elif (lagna1, lagna2) in love_pairs or (lagna2, lagna1) in love_pairs:
        return 71, "Nurture a well-balanced ascendant link that promotes openness and collective growth."
    else:
        return 41, "Maintain a stable ascendant connection that encourages empathy and teamwork."