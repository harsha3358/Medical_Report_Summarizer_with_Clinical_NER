# backend/app.py

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

from pipeline import run_pipeline

app = FastAPI(title="Medical Report Summarizer API")

# -------------------------------
# CORS (for frontend connection)
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# ROOT CHECK
# -------------------------------
@app.get("/")
def root():
    return {"status": "Backend Running"}

# -------------------------------
# MAIN ANALYZE API
# -------------------------------
@app.post("/analyze")
async def analyze(
    text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        # If file is uploaded
        if file:
            temp_path = f"temp_{file.filename}"

            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            result = run_pipeline(file_path=temp_path)

            # clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

        # If text is provided
        else:
            result = run_pipeline(text=text)

        return result

    except Exception as e:
        print("API ERROR:", e)
        return {
            "lstm_summary": "",
            "bart_summary": "",
            "entities": {}
        }