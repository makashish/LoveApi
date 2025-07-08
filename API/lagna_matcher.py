import swisseph as swe

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
        ("Mesha", "Simha"), ("Vrishabha", "Kanya"), ("Tula", "Kumbha"),
        ("Karka", "Meena"), ("Vrischika", "Karka")
    ]

    if (lagna1, lagna2) in good_pairs or (lagna2, lagna1) in good_pairs:
        return 75, "Complementary personalities with balance."
    
    return 60, "Some work needed in mutual understanding."