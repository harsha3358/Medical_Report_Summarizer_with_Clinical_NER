from transformers import pipeline
from ocr_correction import correct_text

# Load summarizer (safe fallback included)
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except:
    summarizer = None


# -------------------------------
# ENTITY EXTRACTION (ROBUST)
# -------------------------------
def extract_entities(text):
    t = text.lower()

    entities = {
        "disease": [],
        "drug": [],
        "symptom": [],
        "treatment": []
    }

    # diseases
    if "diabetes" in t or "glucose" in t:
        entities["disease"].append("diabetes")

    if "cholesterol" in t or "ldl" in t:
        entities["disease"].append("dyslipidemia")

    if "cancer" in t or "tumor" in t:
        entities["disease"].append("cancer")

    if "copd" in t:
        entities["disease"].append("copd")

    # symptoms
    for s in ["fever", "cough", "nausea", "fatigue", "chest pain", "shortness of breath"]:
        if s in t:
            entities["symptom"].append(s)

    # drugs
    for d in ["aspirin", "ibuprofen", "paracetamol", "ondansetron", "metformin", "tiotropium"]:
        if d in t:
            entities["drug"].append(d)

    # treatments
    if "chemotherapy" in t:
        entities["treatment"].append("chemotherapy")
    if "surgery" in t:
        entities["treatment"].append("surgery")

    # deduplicate
    for k in entities:
        entities[k] = list(set(entities[k]))

    return entities


# -------------------------------
# SUMMARIZATION (SAFE)
# -------------------------------
def generate_summary(text):
    if summarizer:
        try:
            result = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]["summary_text"]
            sentences = list(dict.fromkeys(result.split(".")))
            return ". ".join([s.strip() for s in sentences if s.strip()])
        except:
            pass

    return text[:200]


# -------------------------------
# CONFIDENCE (FIXED)
# -------------------------------
def confidence_score(text, entities):
    score = 0

    score += len(entities["disease"]) * 0.4
    score += len(entities["drug"]) * 0.3
    score += len(entities["symptom"]) * 0.2
    score += len(entities["treatment"]) * 0.1

    if score == 0:
        if any(k in text for k in ["fever", "cough", "glucose", "cholesterol"]):
            return 0.4

    return round(min(score, 1.0), 2)


# -------------------------------
# FINAL PIPELINE
# -------------------------------
def process_text(text):
    text = correct_text(text)

    summary = generate_summary(text)
    entities = extract_entities(text)
    confidence = confidence_score(text, entities)

    return {
        "clinical_summary": summary,
        "entities": entities,
        "confidence": confidence,
        "disclaimer": "AI-generated summary. Not a medical diagnosis."
    }