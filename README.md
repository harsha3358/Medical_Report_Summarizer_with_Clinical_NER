# Medical Report Summarizer with Clinical NER

A FastAPI + Next.js application for analyzing clinical notes. The app accepts typed medical text or uploaded medical-report images, extracts text with OCR when needed, generates a clinical summary, and identifies simple clinical entities such as diseases, drugs, symptoms, and treatments.

This repository also includes Objective 1 experiment scripts for comparing a custom sequence-to-sequence LSTM baseline, an LSTM with attention, and transformer summarization baselines using ROUGE metrics.

## Features

- Text input through the web chat interface.
- Image input through upload: PNG, JPG, JPEG, BMP, TIF, and TIFF.
- OCR preprocessing with OpenCV and Tesseract.
- Clinical summary generation with a DistilBART summarization pipeline.
- Rule-based clinical NER for diseases, drugs, symptoms, and treatments.
- SQLite-backed history storage.
- LSTM baseline and LSTM + Attention training/evaluation scripts.
- BART evaluation and side-by-side model comparison scripts.

## Repository Structure

```text
Medical_Report_Summarizer_with_Clinical_NER/
  backend/
    app.py                  FastAPI server and API routes
    pipeline.py             Clinical summary + NER pipeline
    ocr_utils.py            Image preprocessing for OCR
    ocr_correction.py       OCR text normalization helpers
    database.py             SQLite history store
    lstm_summarization.py   LSTM and LSTM + Attention training/evaluation
    lstm_inference.py       LSTM + Attention inference helper
    bart_evaluation.py      BART ROUGE evaluation
    compare_models.py       LSTM vs Attention vs BART comparison
    requirements.txt        Python dependencies
  frontend/
    src/app/                Next.js app shell
    src/components/         Chat UI, sidebar, entity chips, analytics
    src/lib/                API client and TypeScript types
    package.json            Frontend dependencies and scripts
```

## Prerequisites

- Python 3.10+
- Node.js 18+
- Tesseract OCR installed for image upload support
- Optional: CUDA GPU for faster model training/evaluation

On Windows, the backend automatically uses:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If Tesseract is installed elsewhere, add it to PATH or update `TESSERACT_EXE` in `backend/app.py`.

## Setup

Clone the repository:

```bash
git clone https://github.com/harsha3358/Medical_Report_Summarizer_with_Clinical_NER.git
cd Medical_Report_Summarizer_with_Clinical_NER
```

Install backend dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app:app --host 127.0.0.1 --port 10000
```

Install frontend dependencies:

```bash
cd ../frontend
npm install
```

For development:

```bash
npm run dev
```

For a production-style local run:

```bash
npm run build
npm run start
```

Open:

```text
http://127.0.0.1:3000
```

The frontend talks to:

```text
http://127.0.0.1:10000
```

## API

### Health Check

```http
GET /
```

Returns:

```json
{
  "message": "Medical AI API (fast text version) running"
}
```

### Analyze Text

```http
POST /analyze
Content-Type: application/x-www-form-urlencoded

text=Patient has fever, fatigue and is on aspirin and metformin.
```

### Analyze Image

```http
POST /analyze
Content-Type: multipart/form-data

file=<medical_report_image.png>
```

Supported image formats:

```text
.png, .jpg, .jpeg, .bmp, .tif, .tiff
```

### Response Format

```json
{
  "clinical_summary": "Patient has fever fatigue and is on aspirin and metformin.",
  "entities": {
    "disease": [],
    "drug": ["metformin", "aspirin"],
    "symptom": ["fever", "fatigue"],
    "treatment": []
  },
  "confidence": 1.0,
  "disclaimer": "AI-generated summary. Not a medical diagnosis."
}
```

Errors are returned in the same shape with an `error` field:

```json
{
  "clinical_summary": "",
  "entities": {
    "disease": [],
    "drug": [],
    "symptom": [],
    "treatment": []
  },
  "confidence": 0,
  "error": "No readable text provided",
  "disclaimer": "AI-generated summary. Not a medical diagnosis."
}
```

### History

```http
GET /history
DELETE /history/clear
```

## Attention Mechanism

`backend/lstm_summarization.py` includes two sequence-to-sequence models:

- LSTM without attention
- LSTM with dot-product attention over encoder time steps

The attention decoder now receives padded encoder outputs plus a source mask, so it attends only over valid input tokens instead of padded positions. The same attention path is used for:

- training
- summary generation
- ROUGE evaluation
- `lstm_inference.py`

Run the LSTM experiments:

```bash
cd backend
python lstm_summarization.py
```

Run the full comparison:

```bash
python compare_models.py
```

These scripts download CNN/DailyMail from Hugging Face when run.

## Accuracy and Evaluation

Summarization quality is evaluated with ROUGE:

- ROUGE-1
- ROUGE-2
- ROUGE-L

The project includes:

```bash
python lstm_summarization.py
python bart_evaluation.py
python compare_models.py
```

Expected trend:

| Model | Expected Behavior |
| --- | --- |
| LSTM without attention | Baseline sequence-to-sequence model |
| LSTM + Attention | Should improve over the plain LSTM by focusing on relevant source tokens |
| BART-Large-CNN | Strong transformer summarization baseline |
| DistilBART pipeline | Fast app-time summary generation |

Note: exact ROUGE scores depend on machine, dataset cache, training time, random seed, and GPU availability.

## Verified Local Checks

The following checks were run locally:

- Frontend build succeeds with `npm run build`.
- Frontend serves successfully at `http://127.0.0.1:3000`.
- Backend health route responds at `http://127.0.0.1:10000`.
- Text input returns summary and entities.
- Empty input returns a friendly error.
- Unsupported file upload returns a friendly file-type error.
- PNG image upload is OCR'd and analyzed.
- LSTM + Attention shape test confirms encoder outputs, masks, decoder logits, and generation path work together.

Example text test:

```text
Diabetes patient has fatigue and uses metformin.
```

Expected extracted entities:

```json
{
  "disease": ["diabetes"],
  "drug": ["metformin"],
  "symptom": ["fatigue"],
  "treatment": []
}
```

Example image OCR test:

```text
Patient has fever cough and takes aspirin.
```

Expected extracted entities:

```json
{
  "disease": [],
  "drug": ["aspirin"],
  "symptom": ["cough", "fever"],
  "treatment": []
}
```

## Important Notes

- This app is for educational and research use.
- The generated output is not a diagnosis.
- Rule-based NER is intentionally simple and should be expanded with a clinical NER model for production accuracy.
- Image OCR accuracy depends on image quality, resolution, handwriting/printing style, and Tesseract installation.

## License

MIT License for academic and research use.
