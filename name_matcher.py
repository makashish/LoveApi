def name_compatibility(name1, name2):
    def name_score(name):
        return sum([ord(c.lower()) - 96 for c in name if c.isalpha()]) % 9 + 1

    score1 = name_score(name1)
    score2 = name_score(name2)

    base_compatibility = 100 - abs(score1 - score2) * 10
    length_penalty = abs(len(name1) - len(name2)) * 5

    final_score = base_compatibility - length_penalty
    compatibility_percent = max(40, min(final_score, 100))

    # Descriptive report
    if compatibility_percent >= 90:
        report = "Strong bond likely by name vibrations and sound resonance."
    elif compatibility_percent >= 81:
        report = "Create an ascendant harmony that bridges differences and strengthens partnership."
    elif compatibility_percent >= 71:
        report = "Sustain a balanced ascendant understanding that leads to lasting cooperation."
    elif compatibility_percent >= 61:
        report = "Foster a supportive ascendant alignment that deepens trust and unity."
    elif compatibility_percent >= 51:
        report = "Maintain a stable ascendant connection that encourages empathy and teamwork."
    elif compatibility_percent >= 41:
        report = "Develop a steady ascendant relationship that inspires cooperation and mutual respect."
    else:
        report = "Names show moderate compatibility impact."

    return {
        "name1": name1,
        "name2": name2,
        "score1": score1,
        "score2": score2,
        "compatibility_percent": compatibility_percent,
        "report": report
    }