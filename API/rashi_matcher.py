import swisseph as swe

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

    if rashi1 == rashi2:
        return 75, "Both share similar emotional traits."
    elif (rashi1, rashi2) in good_pairs or (rashi2, rashi1) in good_pairs:
        return 90, "Emotionally aligned. Great bonding possible."
    else:
        return 50, "Some emotional differences may exist."