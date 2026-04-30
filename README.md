# 🏥 Medical Report Summarizer with Clinical NER

A production-grade AI system for **medical text summarization** and **clinical named entity recognition (NER)**, featuring a FastAPI backend and a modern Next.js chat interface.

---

## 📋 Project Overview

| Objective | Description |
|-----------|-------------|
| **Objective 1** | Medical report summarization — comparing LSTM (baseline) vs. Flan-T5-Large (transformer) using ROUGE metrics |
| **Objective 2** | Clinical Named Entity Recognition — extracting diseases, drugs, and symptoms from medical text |

---

## 📂 Repository Structure

```
Medical_Report_Summarizer_with_Clinical_NER/
├── backend/
│   ├── lstm_summarization.py   # Objective 1 — LSTM & LSTM+Attention training + evaluation
│   ├── bart_evaluation.py      # Objective 1 — BART/Flan-T5 evaluation
│   ├── compare_models.py       # Objective 1 — Side-by-side model comparison script
│   ├── pipeline.py             # Objective 2 — Clinical NER + Flan-T5 summarization pipeline
│   ├── lstm_inference.py       # LSTM inference helper
│   ├── app.py                  # FastAPI server (REST API)
│   ├── database.py             # SQLite history store
│   ├── ocr_utils.py            # Image preprocessing utility
│   └── requirements.txt        # Python dependencies
└── frontend/
    ├── src/
    │   ├── app/                # Next.js pages (page.tsx, layout.tsx, globals.css)
    │   ├── components/         # UI components (ChatWindow, Sidebar, EntityChips, etc.)
    │   └── lib/                # API client + TypeScript types
    └── package.json
```

---

## 📦 Dataset

**Dataset used:** [CNN / DailyMail (3.0.0)](https://huggingface.co/datasets/cnn_dailymail)

- **No manual download required** — the dataset is fetched automatically via 🤗 HuggingFace `datasets` when you run the scripts.
- Training subset: `train[:5000]` articles (Objective 1 — LSTM)
- Evaluation subset: `test[:500]` articles (Objective 1 — BART)
- Dataset size on disk: ~1.5 GB (well under 500 MB committed — streamed, not committed)

```python
# Automatic download (handled inside scripts):
from datasets import load_dataset
dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:5000]")
```

---

## 🚀 Setup & Reproducibility

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) CUDA GPU for faster training

### 1. Clone the repo
```bash
git clone https://github.com/harsha3358/Medical_Report_Summarizer_with_Clinical_NER.git
cd Medical_Report_Summarizer_with_Clinical_NER
```

### 2. Install Python dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Objective 1 — LSTM vs BART Summarization
```bash
# Train LSTM & LSTM+Attention, then evaluate both
python lstm_summarization.py

# Evaluate BART (facebook/bart-large-cnn)
python bart_evaluation.py

# Full side-by-side comparison table
python compare_models.py
```

### 4. Run Objective 2 — Clinical NER + Transformer Pipeline
The NER pipeline runs via the FastAPI server:
```bash
# Start the backend API
uvicorn app:app --reload --port 8000
```

API endpoint: `POST /analyze`  
Payload: `{ "text": "<medical report text>" }`  
Returns: `{ "lstm_summary": "...", "bart_summary": "...", "entities": { "disease": [...], "drug": [...], "symptom": [...] } }`

### 5. Run the Frontend (Chat UI)
```bash
cd ../frontend
npm install
npm run dev
```
Visit: `http://localhost:3000`

---

## 🧪 Evaluation Metrics

See **Results Summary** below. All metrics computed using `rouge-score` library on CNN/DailyMail test set.

---

## 📊 Results Summary

| Model | ROUGE-1 | ROUGE-2 | ROUGE-L |
|-------|---------|---------|---------|
| LSTM (no attention) | — | — | ~0.082 |
| LSTM + Attention | — | — | ~0.095 |
| Flan-T5-Large | ~0.38 | ~0.17 | ~0.35 |
| BART-Large-CNN | ~0.44 | ~0.21 | ~0.41 |

> Note: LSTM models report only ROUGE-L (as implemented in `lstm_summarization.py`). Run `compare_models.py` to generate live values.

---

## 🤖 Models Used

| Model | HuggingFace ID | Purpose |
|-------|----------------|---------|
| Flan-T5-Large | `google/flan-t5-large` | Transformer summarization (production pipeline) |
| BART-Large-CNN | `facebook/bart-large-cnn` | Evaluation baseline |
| Custom LSTM | Built from scratch | Sequence-to-sequence baseline |

---

## 📜 License

MIT License — open for academic and research use.
