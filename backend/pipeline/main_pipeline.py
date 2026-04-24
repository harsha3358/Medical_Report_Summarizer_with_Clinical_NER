from backend.pipeline.ocr import extract_text
from backend.pipeline.preprocess import clean_text
from backend.pipeline.summarizer import generate_summary
from backend.pipeline.ner import extract_entities
from backend.pipeline.medical import map_medical_from_text
from backend.pipeline.scoring import compute_confidence


def run_pipeline(input_data, is_image=False):

    # Step 1: OCR or direct text
    text = extract_text(input_data) if is_image else input_data

    # Step 2: Cleaning
    cleaned = clean_text(text)

    # Step 3: Summarization
    summary = generate_summary(cleaned)

    # Step 4: NER (kept for demo purposes)
    entities = extract_entities(summary)

    # Step 5: Medical extraction (improved logic)
    medical = map_medical_from_text(summary)

    # Step 6: Confidence score
    confidence = compute_confidence(summary, entities)

    return {
        "raw_text": text,
        "cleaned_text": cleaned,
        "summary": summary,
        "entities": entities,
        "medical": medical,
        "confidence": confidence
    }
