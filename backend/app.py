from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil

from backend.pipeline.main_pipeline import run_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Medical AI API running"}

@app.post("/analyze-text")
async def analyze_text(data: dict):
    return run_pipeline(data["text"])

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return run_pipeline(path, is_image=True)