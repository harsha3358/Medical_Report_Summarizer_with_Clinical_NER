def compute_confidence(summary, entities, medical):

    if not summary:
        return 0.0

    medical_count = (
        len(medical["DISEASE"]) +
        len(medical["DRUG"]) +
        len(medical["SYMPTOM"])
    )

    medical_score = min(0.6, medical_count * 0.2)

    word_count = len(summary.split())
    length_score = min(0.3, word_count / 25)

    entity_score = min(0.1, len(entities) * 0.02)

    return round(medical_score + length_score + entity_score, 2)