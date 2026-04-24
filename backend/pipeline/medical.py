def map_medical_from_text(text):
    text = text.lower()

    result = {
        "DISEASE": [],
        "DRUG": [],
        "SYMPTOM": []
    }

    diseases = ["diabetes", "hypertension", "asthma", "infection"]
    drugs = ["insulin", "metformin", "paracetamol", "antibiotics"]
    symptoms = ["fever", "fatigue", "pain", "cough", "dizziness"]

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