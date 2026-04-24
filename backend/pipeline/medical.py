def normalize_text(text):
    text = text.lower()

    replacements = {
        "bp": "blood pressure",
        "sugar": "diabetes",
        "high sugar": "diabetes"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text


def map_medical_from_text(text):
    text = normalize_text(text)

    diseases = [
        "diabetes", "hypertension", "asthma",
        "covid", "cancer", "infection"
    ]

    drugs = [
        "insulin", "metformin", "paracetamol",
        "aspirin", "antibiotics"
    ]

    symptoms = [
        "fever", "fatigue", "pain",
        "cough", "headache", "dizziness"
    ]

    result = {"DISEASE": [], "DRUG": [], "SYMPTOM": []}

    for d in diseases:
        if d in text:
            result["DISEASE"].append(d)

    for d in drugs:
        if d in text:
            result["DRUG"].append(d)

    for s in symptoms:
        if s in text:
            result["SYMPTOM"].append(s)

    return result