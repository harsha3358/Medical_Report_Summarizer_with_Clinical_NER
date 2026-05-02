from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pipeline import process_text
import pytesseract
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Medical AI API running"}

@app.post("/analyze")
async def analyze(text: str = Form(None), file: UploadFile = File(None)):
    try:
        if file:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            text = pytesseract.image_to_string(image)

        if not text or text.strip() == "":
            return {
                "clinical_summary": "",
                "entities": {},
                "confidence": 0,
                "error": "No input provided",
                "disclaimer": "AI-generated summary. Not a medical diagnosis."
            }

        return process_text(text)

    except Exception as e:
        return {
            "clinical_summary": "",
            "entities": {},
            "confidence": 0,
            "error": str(e),
            "disclaimer": "AI-generated summary. Not a medical diagnosis."
        }