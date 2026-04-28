# backend/pipeline.py

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

# -------------------------------
# DEVICE
# -------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------------
# MODEL (UPGRADED)
# -------------------------------
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-large").to(DEVICE)

# -------------------------------
# CLEAN TEXT
# -------------------------------
def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"[^\w\s.,]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# -------------------------------
# SUMMARIZATION (IMPROVED PROMPT)
# -------------------------------
def generate_summary(text):
    try:
        prompt = (
            "Extract and summarize the medical information in one sentence.\n"
            "Format: Disease + Symptoms + Treatment.\n\n"
            "Text:\n" + text[:512]
        )

        inputs = tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        ).to(DEVICE)

        outputs = model.generate(
            **inputs,
            max_length=60,
            min_length=20,
            num_beams=6,
            no_repeat_ngram_size=3,
            length_penalty=1.0,
            early_stopping=True
        )

        summary = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return summary.strip()

    except Exception as e:
        print("SUMMARY ERROR:", e)
        return ""

# -------------------------------
# LSTM BASELINE
# -------------------------------
def lstm_generate(text):
    return text[:80]

# -------------------------------
# ENTITY EXTRACTION (IMPROVED)
# -------------------------------
def extract_medical_entities(text):
    text = text.lower()

    entities = {
        "disease": [],
        "drug": [],
        "symptom": []
    }

    disease_list = ["diabetes", "cancer", "infection", "tumor"]
    drug_list = ["insulin", "aspirin", "paracetamol", "ibuprofen", "metformin"]
    symptom_list = ["fever", "pain", "cough", "fatigue", "thirst", "urination"]

    for d in disease_list:
        if d in text:
            entities["disease"].append(d)

    for d in drug_list:
        if d in text:
            entities["drug"].append(d)

    for s in symptom_list:
        if s in text:
            entities["symptom"].append(s)

    return entities

# -------------------------------
# MAIN PIPELINE
# -------------------------------
def run_pipeline(text=None, file_path=None):
    try:
        if not text:
            text = ""

        text = clean_text(text)

        print("FINAL TEXT:", text)

        if len(text) < 10:
            return {
                "lstm_summary": "",
                "bart_summary": "",
                "entities": {}
            }

        # LSTM baseline
        lstm_summary = lstm_generate(text)

        # Transformer summary
        summary = generate_summary(text)

        # Entities
        entities = extract_medical_entities(summary)

        return {
            "lstm_summary": lstm_summary,
            "bart_summary": summary,
            "entities": entities
        }

    except Exception as e:
        print("PIPELINE ERROR:", e)
        return {
            "lstm_summary": "",
            "bart_summary": "",
            "entities": {}
        }