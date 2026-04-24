from backend.pipeline.ocr import extract_text
from backend.pipeline.preprocess import clean_text
from backend.pipeline.summarizer import generate_summary
from backend.pipeline.ner import extract_entities
from backend.pipeline.medical import map_medical_from_text
from backend.pipeline.scoring import compute_confidence


def run_pipeline(input_data, is_image=False):

    # Step 1: OCR (if image)
    text = extract_text(input_data) if is_image else input_data

    # Step 2: Clean text
    cleaned = clean_text(text)

    # Step 3: Generate summary
    summary = generate_summary(cleaned)

    # Step 4: Extract entities
    entities = normalize_entities(entities)

    # Step 5: Extract medical info
    medical = map_medical_from_text(summary)

    # Step 6: Confidence score
    confidence = compute_confidence(summary, entities, medical)

    return {
        "raw_text": text,
        "cleaned_text": cleaned,
        "summary": summary,
        "entities": entities,
        "medical": medical,
        "confidence": confidence
    }

def normalize_entities(entities):
    mapping = {
        "Disease_disorder": "DISEASE",
        "Medication": "DRUG",
        "Sign_symptom": "SYMPTOM"
    }

    for e in entities:
        if e["entity"] in mapping:
            e["entity"] = mapping[e["entity"]]

    return entities