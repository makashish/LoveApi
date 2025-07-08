import swisseph as swe
import datetime

# SET THIS TO WHERE YOU DOWNLOADED EPHEMERIS FILES
EPHE_PATH = '/path/to/ephemeris'  # Update this path correctly

swe.set_ephe_path(EPHE_PATH)

def datetime_to_julian(dt: datetime.datetime):
    """Convert datetime to Julian Day"""
    return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60)

import swisseph as swe

def get_moon_rashi(jd, lat, lon):
    swe.set_topo(lon, lat, 0)

    # 🔥 FIX HERE: Use [0][0] to get longitude only
    moon_long = swe.calc_ut(jd, swe.MOON)[0][0]

    rashi_index = int(moon_long / 30)
    rashis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    return rashis[rashi_index]
def get_lagna_sign(jd, lat, lon):
    """Get Lagna sign (Ascendant) using house calculation"""
    asc = swe.houses_ex(jd, lat, lon, b'A')[0][0]  # Ascendant degree
    lagna_index = int(asc / 30)
    rashis = [
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena"
    ]
    return rashis[lagna_index]