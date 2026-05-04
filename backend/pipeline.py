import os
import re

from transformers import pipeline
from ocr_correction import correct_text

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"
NER_MODEL_NAME = "d4data/biomedical-ner-all"
ENABLE_BIOMED_NER = os.getenv("MEDAI_ENABLE_BIOMED_NER", "0") == "1"

_summarizer = None
_ner_model = None


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        try:
            _summarizer = pipeline("summarization", model=MODEL_NAME)
        except:
            _summarizer = None
    return _summarizer


def get_ner_model():
    global _ner_model
    if not ENABLE_BIOMED_NER:
        return None

    if _ner_model is None:
        try:
            _ner_model = pipeline(
                "ner",
                model=NER_MODEL_NAME,
                aggregation_strategy="simple",
            )
        except Exception:
            _ner_model = False

    return _ner_model or None


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
    return any(re.search(rf"\b{re.escape(phrase)}\b", text) for phrase in phrases)


def add_unique(items, value):
    value = value.strip()
    if value and value not in items:
        items.append(value)


def normalize_entity_text(text):
    text = text.replace("##", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,;:()[]{}")


def apply_biomedical_ner(text, entities):
    ner_model = get_ner_model()
    if not ner_model:
        return

    try:
        ner_results = ner_model(text)
    except Exception:
        return

    for item in ner_results:
        label = item.get("entity_group") or item.get("entity") or ""
        value = normalize_entity_text(item.get("word", ""))
        if not value:
            continue

        if "Disease_disorder" in label:
            add_unique(entities["disease"], value.lower())
        elif "Sign_symptom" in label:
            add_unique(entities["symptom"], value.lower())
        elif "Medication" in label:
            add_unique(entities["drug"], value.lower())
        elif "Therapeutic_procedure" in label:
            add_unique(entities["treatment"], value.lower())


def extract_entities(text):
    t = text.lower()

    entities = {
        "disease": [],
        "drug": [],
        "symptom": [],
        "treatment": []
    }

    disease_rules = {
        "HIV/AIDS": ["hiv", "aids", "human immunodeficiency virus", "acquired immunodeficiency syndrome"],
        "diabetes": ["diabetes", "glucose", "hyperglycemia"],
        "hypoglycemia": ["hypoglycemia"],
        "hypertension": ["hypertension", "high blood pressure", "htn"],
        "hypotension": ["hypotension", "low blood pressure"],
        "dyslipidemia": ["cholesterol", "dyslipidemia", "hyperlipidemia"],
        "cancer": ["cancer", "carcinoma", "malignancy", "tumor", "tumour"],
        "leukemia": ["leukemia", "leukaemia"],
        "lymphoma": ["lymphoma"],
        "melanoma": ["melanoma"],
        "COPD": ["copd", "chronic obstructive pulmonary disease"],
        "asthma": ["asthma"],
        "tuberculosis": ["tuberculosis", "tb"],
        "pneumonia": ["pneumonia"],
        "bronchitis": ["bronchitis"],
        "malaria": ["malaria"],
        "dengue": ["dengue"],
        "typhoid": ["typhoid"],
        "cholera": ["cholera"],
        "hepatitis": ["hepatitis"],
        "hepatitis A": ["hepatitis a"],
        "hepatitis B": ["hepatitis b", "hbv"],
        "hepatitis C": ["hepatitis c", "hcv"],
        "influenza": ["influenza", "flu"],
        "covid-19": ["covid", "covid-19", "coronavirus"],
        "anemia": ["anemia", "anaemia"],
        "sickle cell disease": ["sickle cell disease", "sickle cell anemia", "sickle cell anaemia"],
        "arthritis": ["arthritis"],
        "rheumatoid arthritis": ["rheumatoid arthritis"],
        "osteoarthritis": ["osteoarthritis"],
        "migraine": ["migraine"],
        "epilepsy": ["epilepsy", "seizure disorder"],
        "stroke": ["stroke", "cerebrovascular accident"],
        "heart disease": ["heart disease", "cardiac disease", "coronary artery disease"],
        "heart failure": ["heart failure"],
        "myocardial infarction": ["myocardial infarction", "heart attack"],
        "kidney disease": ["kidney disease", "renal disease"],
        "chronic kidney disease": ["chronic kidney disease", "ckd"],
        "liver disease": ["liver disease"],
        "cirrhosis": ["cirrhosis"],
        "depression": ["depression"],
        "anxiety disorder": ["anxiety disorder"],
        "bipolar disorder": ["bipolar disorder"],
        "schizophrenia": ["schizophrenia"],
        "alzheimer disease": ["alzheimer", "alzheimer's disease", "alzheimers disease"],
        "parkinson disease": ["parkinson", "parkinson's disease", "parkinsons disease"],
        "meningitis": ["meningitis"],
        "encephalitis": ["encephalitis"],
        "sepsis": ["sepsis"],
        "urinary tract infection": ["urinary tract infection", "uti"],
        "appendicitis": ["appendicitis"],
        "pancreatitis": ["pancreatitis"],
        "gastritis": ["gastritis"],
        "gastroenteritis": ["gastroenteritis"],
        "ulcer": ["ulcer", "peptic ulcer"],
        "eczema": ["eczema"],
        "psoriasis": ["psoriasis"],
        "dermatitis": ["dermatitis"],
        "measles": ["measles"],
        "mumps": ["mumps"],
        "rubella": ["rubella"],
        "chickenpox": ["chickenpox", "varicella"],
        "shingles": ["shingles", "herpes zoster"],
        "herpes": ["herpes", "hsv"],
        "syphilis": ["syphilis"],
        "gonorrhea": ["gonorrhea", "gonorrhoea"],
        "chlamydia": ["chlamydia"],
        "ebola": ["ebola"],
        "zika": ["zika"],
        "yellow fever": ["yellow fever"],
        "rabies": ["rabies"],
        "polio": ["polio", "poliomyelitis"],
        "tetanus": ["tetanus"],
        "diphtheria": ["diphtheria"],
        "whooping cough": ["whooping cough", "pertussis"],
        "obesity": ["obesity"],
        "osteoporosis": ["osteoporosis"],
        "thyroid disease": ["thyroid disease"],
        "hypothyroidism": ["hypothyroidism"],
        "hyperthyroidism": ["hyperthyroidism"],
        "goiter": ["goiter", "goitre"],
        "lupus": ["lupus", "systemic lupus erythematosus", "sle"],
        "multiple sclerosis": ["multiple sclerosis", "ms"],
        "celiac disease": ["celiac disease", "coeliac disease"],
        "crohn disease": ["crohn disease", "crohn's disease", "crohns disease"],
        "ulcerative colitis": ["ulcerative colitis"],
    }

    for disease, phrases in disease_rules.items():
        if contains_any(t, phrases):
            add_unique(entities["disease"], disease)

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
            add_unique(entities["symptom"], symptom)

    for d in ["aspirin", "ibuprofen", "paracetamol", "ondansetron", "metformin", "tiotropium"]:
        if contains_any(t, [d]):
            add_unique(entities["drug"], d)

    treatment_rules = {
        "chemotherapy": ["chemotherapy"],
        "radiotherapy": ["radiotherapy", "radiation therapy"],
        "surgery": ["surgery", "operation"],
        "dialysis": ["dialysis"],
        "physiotherapy": ["physiotherapy", "physical therapy"],
    }

    for treatment, phrases in treatment_rules.items():
        if contains_any(t, phrases):
            add_unique(entities["treatment"], treatment)

    apply_biomedical_ner(text, entities)

    for k in entities:
        entities[k] = sorted(set(entities[k]), key=str.lower)

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
