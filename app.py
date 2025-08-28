from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import swisseph as swe
import datetime

# Import local modules
from name_matcher import name_compatibility
from rashi_matcher import rashi_compatibility
from lagna_matcher import lagna_compatibility
from swisseph_utils import get_moon_rashi, get_lagna_sign

# ----------------------
# Initialize Flask App
# ----------------------
app = Flask(__name__)
CORS(app)

# Set Swiss Ephemeris path
swe.set_ephe_path("./ephe")  # change path if required


@app.route("/")
def home():
    env_type = "Render" if os.environ.get("RENDER") else "Localhost"
    return jsonify({
        "message": "Server is running",
        "environment": env_type,
        "url": "https://loveapi.onrender.com" if env_type == "Render" else f"http://{os.getenv('HOST','localhost')}:{os.getenv('PORT','5000')}"
    })


# ----------------------
# Helper: Description generator
# ----------------------
def get_description(name1, name2, compatibility_percent):
    if compatibility_percent >= 91:
          return (
              
            f"{name1} और {name2} एक संतुलित लग्न संबंध साझा करते हैं "
            f"जो आपसी सम्मान का वातावरण बनाता है, जहाँ दोनों एक-दूसरे के दृष्टिकोण "
            f"की सराहना करते हैं। यह सामंजस्य खुली बातचीत को प्रोत्साहित करता है, "
            f"गलतफहमियों को कम करता है और स्वस्थ समझौतों की अनुमति देता है, "
            f"जिससे भावनात्मक सुरक्षा और दीर्घकालिक सहयोग मजबूत होता है।\n\n"
            f"{name1} and {name2} share a balanced ascendant connection that creates "
            f"an atmosphere of mutual respect, where both appreciate each other’s perspectives. "
            f"This harmony encourages open dialogue, reduces misunderstandings, and allows for "
            f"healthy compromises, fostering emotional security and long-term cooperation."
           
        )
    elif compatibility_percent >= 81:
        return (
            
            f"{name1} और {name2} एक संतुलित लग्न संबंध साझा करते हैं। "
            f"जब लग्न संतुलित होते हैं, तो बिना टकराव के मतभेदों को पाटना आसान हो जाता है। "
            f"दोनों को समझा और सराहा हुआ महसूस होता है, जिससे गहरे संबंध, भावनात्मक सामंजस्य "
            f"और साझा लक्ष्य बनते हैं।\n\n"
            f"{name1} and {name2} share a balanced ascendant connection. "
            f"When ascendants align in a balanced way, it becomes easier to bridge differences without conflict. "
            f"Both feel understood and valued, leading to deeper bonds, emotional harmony, and shared goals."
           
        )
    elif compatibility_percent >= 71:
        return (
            f"{name1} और {name2} एक संतुलित लग्न संबंध साझा करते हैं "
            f"जो स्वाभाविक रूप से सहयोग को बढ़ावा देता है और साझा मूल्यों तथा सहानुभूति को उजागर करता है। "
            f"अंतर को धैर्य से संभाला जाता है, असहमति को विकास के अवसर में बदला जाता है और "
            f"सहायक, विश्वास से भरा माहौल बनता है।\n\n"
            f"{name1} and {name2} share a balanced ascendant connection that naturally promotes cooperation "
            f"by highlighting shared values and empathy. Differences are handled with patience, turning disagreements "
            f"into opportunities for growth, and creating a supportive, trust-filled environment."
        )
    elif compatibility_percent >= 61:
        return (
            f"{name1} और {name2} एक संतुलित लग्न साझा करते हैं। "
            f"यह ऐसी ऊर्जाओं का मिलन है जो एक-दूसरे को पूरक करती हैं, जिससे सहज संवाद और सहज समझ बनती है। "
            f"दोनों अनुकूलन, समझौता और लंबे समय तक चलने वाले संबंध को पोषित करने के लिए तैयार रहते हैं।\n\n"
            f"{name1} and {name2} share a balanced ascendant . "
            f"This symbolizes a meeting point of energies that complement each other, allowing smooth communication and intuitive understanding. "
            f"Both are willing to adapt, compromise, and nurture a lasting relationship."
        )
    elif compatibility_percent >= 51:
        return (
            f"{name1} और {name2} एक संतुलित लग्न साझा करते हैं। "
            f"इसकी ताकत समानता बनाए रखने में है, ताकि कोई भी हावी न हो। "
            f"आपसी सम्मान सहयोग का आधार बनता है, जिससे साझा सफलता और संतुष्टि मिलती है।\n\n"
            f"{name1} and {name2} share a balanced ascendant . "
            f"The strength lies in maintaining equality, ensuring neither dominates. "
            f"Mutual respect becomes the foundation for productive collaboration, leading to shared success and fulfillment."
        )
    elif compatibility_percent >= 41:
        return (
            f"{name1} और {name2} एक संतुलित लग्न साझा करते हैं। "
            f"एक अच्छा संतुलित संबंध भावनात्मक सुरक्षा, खुली बातचीत और टीमवर्क की जगह बनाता है, "
            f"जिससे दोनों मिलकर चुनौतियों का सामना कर सकें और आगे बढ़ें।\n\n"
            f"{name1} and {name2} share a balanced ascendant . "
            f"A well-balanced alignment creates space for emotional safety, open communication, and teamwork, "
            f"enabling both to face challenges together and grow."
        )
    else:
        return (
            f"{name1} और {name2} एक संतुलित लग्न साझा करते हैं। "
            f"यह संबंध समझ, धैर्य और साझा उद्देश्य को जोड़ता है, जिससे दोनों आपसी सम्मान के साथ "
            f"सामंजस्य में आगे बढ़ते हैं।\n\n"
            f"{name1} and {name2} share a balanced ascendant . "
            f"This connection weaves together understanding, patience, and shared purpose, "
            f"helping both grow in harmony while respecting each other’s uniqueness."
        )

# ----------------------
# 🔤 NAME MATCH ENDPOINT
# ----------------------
@app.route("/name-match", methods=["POST"])
def name_match():
    data = request.get_json()
    if not data or "name1" not in data or "name2" not in data:
        return jsonify({"error": "Missing 'name1' or 'name2'"}), 400

    result = name_compatibility(data["name1"], data["name2"])
    compatibility_percent = result.get("compatibility_percent", 0)

    description = get_description(data["name1"], data["name2"], compatibility_percent)

    return jsonify({
        "name1": data["name1"],
        "name2": data["name2"],
        "compatibility_percent": compatibility_percent,
        "description": description
    })


# ----------------------
# ♈ RASHI MATCH ENDPOINT
# ----------------------
@app.route("/rashi-match", methods=["POST"])
def rashi_match():
    data = request.get_json()
    try:
        name1 = data["name1"]
        name2 = data["name2"]
        dob1 = datetime.datetime.fromisoformat(data["dob1"])
        dob2 = datetime.datetime.fromisoformat(data["dob2"])
        lat1, lon1 = float(data["lat1"]), float(data["lon1"])
        lat2, lon2 = float(data["lat2"]), float(data["lon2"])
    except Exception:
        return jsonify({"error": "Invalid or missing parameters"}), 400

    jd1 = swe.julday(dob1.year, dob1.month, dob1.day, dob1.hour + dob1.minute / 60)
    jd2 = swe.julday(dob2.year, dob2.month, dob2.day, dob2.hour + dob2.minute / 60)

    rashi1 = get_moon_rashi(jd1, lat1, lon1)
    rashi2 = get_moon_rashi(jd2, lat2, lon2)

    compatibility_percent, _ = rashi_compatibility(rashi1, rashi2)
    description = get_description(name1, name2, compatibility_percent)

    return jsonify({
        "name1": name1,
        "rashi1": rashi1,
        "name2": name2,
        "rashi2": rashi2,
        "compatibility_percent": compatibility_percent,
        "description": description
    })


# ----------------------
# ♋ LAGNA MATCH ENDPOINT
# ----------------------
@app.route("/lagna-match", methods=["POST"])
def lagna_match():
    data = request.get_json()
    try:
        name1 = data.get("name1", "Person A")
        name2 = data.get("name2", "Person B")
        dob1 = datetime.datetime.fromisoformat(data["dob1"])
        dob2 = datetime.datetime.fromisoformat(data["dob2"])
        lat1, lon1 = float(data["lat1"]), float(data["lon1"])
        lat2, lon2 = float(data["lat2"]), float(data["lon2"])
    except Exception:
        return jsonify({"error": "Invalid or missing parameters"}), 400

    jd1 = swe.julday(dob1.year, dob1.month, dob1.day, dob1.hour + dob1.minute / 60)
    jd2 = swe.julday(dob2.year, dob2.month, dob2.day, dob2.hour + dob2.minute / 60)

    lagna1 = get_lagna_sign(jd1, lat1, lon1)
    lagna2 = get_lagna_sign(jd2, lat2, lon2)

    compatibility_percent, _ = lagna_compatibility(lagna1, lagna2)
    description = get_description(name1, name2, compatibility_percent)

    return jsonify({
        "name1": name1,
        "lagna1": lagna1,
        "name2": name2,
        "lagna2": lagna2,
        "compatibility_percent": compatibility_percent,
        "description": description
    })


# ----------------------
# 🚀 Run the App
# ----------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)