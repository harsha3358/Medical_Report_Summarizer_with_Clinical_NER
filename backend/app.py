from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pipeline import process_text, warm_up_models

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


@app.post("/analyze")
async def analyze(text: str = Form(...)):
    try:
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