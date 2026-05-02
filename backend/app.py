import os
import tempfile
from pathlib import Path

import pytesseract
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pipeline import process_text, warm_up_models
from ocr_utils import preprocess_image
from database import clear_all_history, get_all_history, save_result

TESSERACT_EXE = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if TESSERACT_EXE.exists():
    pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_EXE)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 Warm up model once (optional but recommended)
@app.on_event("startup")
async def startup_event():
    warm_up_models()


@app.get("/")
def home():
    return {"message": "Medical AI API (fast text version) running"}


def analyze_and_save(text: str):
    result = process_text(text)
    save_result(text, result.get("clinical_summary", ""), result.get("entities", {}))
    return result


def extract_text_from_image(path: str) -> str:
    processed_image = preprocess_image(path)
    return pytesseract.image_to_string(processed_image).strip()


@app.post("/analyze")
async def analyze(text: str = Form(""), file: UploadFile | None = File(None)):
    try:
        if file is not None:
            suffix = Path(file.filename or "").suffix.lower()
            if suffix not in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}:
                return {
                    "clinical_summary": "",
                    "entities": {"disease": [], "drug": [], "symptom": [], "treatment": []},
                    "confidence": 0,
                    "error": "Unsupported file type. Please upload a PNG, JPG, JPEG, BMP, TIF, or TIFF image.",
                    "disclaimer": "AI-generated summary. Not a medical diagnosis."
                }

            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            try:
                text = extract_text_from_image(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        if not text or text.strip() == "":
            return {
                "clinical_summary": "",
                "entities": {"disease": [], "drug": [], "symptom": [], "treatment": []},
                "confidence": 0,
                "error": "No readable text provided",
                "disclaimer": "AI-generated summary. Not a medical diagnosis."
            }

        return analyze_and_save(text)

    except Exception as e:
        return {
            "clinical_summary": "",
            "entities": {"disease": [], "drug": [], "symptom": [], "treatment": []},
            "confidence": 0,
            "error": str(e),
            "disclaimer": "AI-generated summary. Not a medical diagnosis."
        }


@app.get("/history")
def history():
    return get_all_history()


@app.delete("/history/clear")
def clear_history():
    clear_all_history()
    return {"message": "History cleared"}
