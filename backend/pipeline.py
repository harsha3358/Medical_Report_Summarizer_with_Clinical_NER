from transformers import pipeline
from ocr_correction import correct_text

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

_summarizer = None


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        try:
            _summarizer = pipeline("summarization", model=MODEL_NAME)
        except:
            _summarizer = None
    return _summarizer


# 🔥 Warm-up function (fixes your previous error)
def warm_up_models():
    model = get_summarizer()
    if model:
        try:
            model("warm up text", max_length=20, min_length=5)
        except:
            pass


# -------------------------------
# ENTITY EXTRACTION (FAST RULES)
# -------------------------------
def contains_any(text, phrases):
    return any(phrase in text for phrase in phrases)


def extract_entities(text):
    t = text.lower()

    entities = {
        "disease": [],
        "drug": [],
        "symptom": [],
        "treatment": []
    }

    if "diabetes" in t or "glucose" in t:
        entities["disease"].append("diabetes")

    if "cholesterol" in t:
        entities["disease"].append("dyslipidemia")

    if "cancer" in t:
        entities["disease"].append("cancer")

    if "copd" in t:
        entities["disease"].append("copd")

    symptom_rules = {
        "fever": ["fever", "high temperature"],
        "cough": ["cough"],
        "nausea": ["nausea", "vomiting"],
        "fatigue": ["fatigue", "tiredness", "weakness"],
        "chest pain": ["chest pain"],
        "shortness of breath": ["shortness of breath", "breathlessness"],
        "skin rash": ["skin rash", "skin rashes", "rash", "rashes"],
        "itching": ["itching", "itchy skin", "pruritus"],
        "redness": ["redness", "red skin"],
        "swelling": ["swelling", "swollen"],
    }

    for symptom, phrases in symptom_rules.items():
        if contains_any(t, phrases):
            entities["symptom"].append(symptom)

    for d in ["aspirin", "ibuprofen", "paracetamol", "ondansetron", "metformin", "tiotropium"]:
        if d in t:
            entities["drug"].append(d)

    if "chemotherapy" in t:
        entities["treatment"].append("chemotherapy")

    for k in entities:
        entities[k] = list(set(entities[k]))

    return entities


# -------------------------------
# FAST SUMMARY
# -------------------------------
def generate_summary(text):
    words = text.split()

    # ⚡ FAST PATH
    if len(words) < 40:
        return text.capitalize()

    summarizer = get_summarizer()
    if summarizer:
        try:
            result = summarizer(
                text,
                max_length=120,
                min_length=30,
                do_sample=False
            )[0]["summary_text"]

            sentences = list(dict.fromkeys(result.split(".")))
            return ". ".join([s.strip() for s in sentences if s.strip()])
        except:
            pass

    return text[:200]


# -------------------------------
# CONFIDENCE
# -------------------------------
def confidence_score(text, entities):
    score = (
        len(entities["disease"]) * 0.4 +
        len(entities["drug"]) * 0.3 +
        len(entities["symptom"]) * 0.2 +
        len(entities["treatment"]) * 0.1
    )

    if score == 0 and any(k in text.lower() for k in ["fever", "cough", "glucose", "rash", "rashes", "itching"]):
        return 0.4

    return round(min(score, 1.0), 2)


# -------------------------------
# MAIN PIPELINE
# -------------------------------
def process_text(text):
    text = correct_text(text)

    entities = extract_entities(text)
    summary = generate_summary(text)
    confidence = confidence_score(text, entities)

    return {
        "clinical_summary": summary,
        "entities": entities,
        "confidence": confidence,
        "disclaimer": "AI-generated summary. Not a medical diagnosis."
    }
