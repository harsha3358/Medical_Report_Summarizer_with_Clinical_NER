from backend.utils.config import ner_model

def extract_entities(text):
    results = ner_model(text)

    return [
        {
            "text": r["word"],
            "type": r["entity_group"],
            "confidence": round(r["score"], 3)
        }
        for r in results
    ]