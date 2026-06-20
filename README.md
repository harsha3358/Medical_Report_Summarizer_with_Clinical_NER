# Medical Report Summarizer with Clinical NER

A web application that reads medical text or report images, creates a short summary, and highlights diseases, medicines, symptoms, and treatments.

## Why it matters

Clinical documents can be long and difficult to scan. This project explores how OCR and language models can make important information easier to review.

## How it works

1. The user enters text or uploads an image.
2. OCR extracts text when needed.
3. A transformer produces a summary.
4. Clinical entity detection identifies important terms.
5. The result and analysis history are shown in the web interface.

## Technology

Next.js, FastAPI, Transformers, Tesseract OCR, OpenCV, PyTorch, and SQLite.

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --port 10000
```

```bash
cd frontend
npm install
npm run dev
```

This is an educational project and must not be used for diagnosis or treatment decisions.
