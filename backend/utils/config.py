from transformers import pipeline
import easyocr

print("⏳ Loading models...")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
ocr_reader = easyocr.Reader(['en'], gpu=False)

print("✅ Models Loaded")