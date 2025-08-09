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
    match_pairs = [
        ("Mesha", "Vrischika"), ("Vrishabha", "Kanya"), ("Tula", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Karka")
    ]
    love_pairs = [
        ("Mesha", "kark"), ("Vrishabha", "Meena"), ("Dhanu", "Kumbha"),
        ("kark", "Meena"), ("Vrischika", "Leo")
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