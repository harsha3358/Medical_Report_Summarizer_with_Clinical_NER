def compute_confidence(summary, entities):
    if not summary:
        return 0.0

    entity_score = min(0.4, len(entities) * 0.05)
    length_score = min(0.6, len(summary.split()) / 50)

    return round(entity_score + length_score, 2)