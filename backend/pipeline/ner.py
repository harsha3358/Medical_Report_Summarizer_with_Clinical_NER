from transformers import pipeline

# Load biomedical NER model
ner_model = pipeline(
    "ner",
    model="d4data/biomedical-ner-all",
    aggregation_strategy="simple"
)

def extract_entities(text):
    if not text.strip():
        return []

    results = ner_model(text)

    entities = []
    for r in results:
        entities.append({
            "entity": r.get("entity_group", ""),
            "text": r.get("word", "")
        })
