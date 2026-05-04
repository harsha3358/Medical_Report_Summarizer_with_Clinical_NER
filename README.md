# Medical Report Summarizer with Clinical NER

## What This Project Does

This project is a medical-report assistant. A user can paste a medical note or upload an image of a medical report. The system then reads the content, creates a shorter summary, and highlights important medical words such as symptoms, medicines, diseases, and treatments.

The goal is to make long clinical notes easier to understand at a glance.

## Who This Is For

This project is useful for:

- Students learning artificial intelligence and natural language processing.
- People who want to understand how medical text summarization works.
- Demonstrations of OCR, summarization, and clinical entity extraction.
- Academic projects comparing traditional deep learning with transformer models.

This project is not a replacement for a doctor, hospital system, or medical diagnosis.

## What The User Can Do

The app supports two main input types:

| Input Type | What It Means |
| --- | --- |
| Text | The user types or pastes a medical note into the chat box. |
| Image | The user uploads an image of a report, and the system tries to read the text from the image. |

Supported image formats:

```text
PNG, JPG, JPEG, BMP, TIF, TIFF
```

## What The App Gives Back

After the user submits text or an image, the app returns:

| Output | Meaning |
| --- | --- |
| Clinical summary | A shorter version of the medical note. |
| Diseases | Conditions found in the text, such as diabetes. |
| Drugs | Medicines found in the text, such as aspirin or metformin. |
| Symptoms | Symptoms found in the text, such as fever or cough. |
| Treatments | Treatments found in the text, such as chemotherapy. |
| Confidence score | A simple score showing how much useful medical information was found. |

Example input:

```text
Diabetes patient has fatigue and uses metformin.
```

Example output:

```text
Summary: Diabetes patient has fatigue and uses metformin.
Disease: diabetes
Drug: metformin
Symptom: fatigue
```

## How The Project Works In Simple Words

The project has two parts:

| Part | Job |
| --- | --- |
| Frontend | The screen the user sees and interacts with. |
| Backend | The system that reads, summarizes, and analyzes the report. |

When the user submits a note:

1. The frontend sends the note to the backend.
2. If the input is an image, the backend first extracts text from the image.
3. The backend cleans the text.
4. The backend creates a summary.
5. The backend finds medical entities such as symptoms and medicines.
6. The frontend shows the final result in a readable chat view.

## Main Technologies Used

| Technology | Purpose |
| --- | --- |
| Next.js | Builds the user interface. |
| FastAPI | Runs the backend API. |
| Transformers | Generates summaries using a pretrained model. |
| Tesseract OCR | Reads text from uploaded images. |
| OpenCV | Cleans images before OCR. |
| SQLite | Stores analysis history. |
| PyTorch | Supports the LSTM and attention model experiments. |

## AI And Machine Learning Work

This project includes two types of summarization work.

### 1. App-Time Summarization

The live app uses a transformer summarization model:

```text
sshleifer/distilbart-cnn-12-6
```

This model is used because it is faster and lighter than very large transformer models, which makes it more practical for a working web app.

### Disease And Medical Term Detection

The app does not need full sentences to detect many common diseases. It first checks the text with a dictionary-style medical term detector. This means short inputs such as these can work:

```text
HIV
AIDS
malaria
diabetes asthma covid
tb pneumonia bronchitis
```

The detector supports common disease names, abbreviations, symptoms, medicines, and treatments. It also has an optional biomedical NER model:

```text
d4data/biomedical-ner-all
```

That model can be enabled with:

```text
MEDAI_ENABLE_BIOMED_NER=1
```

The optional model can recognize a wider range of biomedical terms, but it is larger and may make the first request slower because the model has to load.

### 2. Academic Model Comparison

The project also includes experiment scripts to compare:

| Model | Purpose |
| --- | --- |
| LSTM without attention | A basic deep learning baseline. |
| LSTM with attention | An improved LSTM that learns which words to focus on. |
| BART-Large-CNN | A strong transformer comparison model. |

## Attention Mechanism Explained Simply

An attention mechanism helps the model decide which words in the original report are most important while generating the summary.

Without attention, the LSTM has to compress the whole input into a small internal memory. That can make it forget useful details.

With attention, the model can look back at different parts of the original text while writing each word of the summary. This usually helps it create better summaries.

In this project, the LSTM with attention now uses:

- Encoder outputs from every input word.
- A mask so the model ignores empty padded positions.
- The same attention path during training, evaluation, and inference.

## Accuracy And Testing

For summarization accuracy, the project uses ROUGE scores.

ROUGE compares a generated summary with a reference summary and checks how many important words and phrases overlap.

The project supports:

| Metric | Meaning |
| --- | --- |
| ROUGE-1 | Word-level overlap. |
| ROUGE-2 | Two-word phrase overlap. |
| ROUGE-L | Longest matching sequence of words. |

The following checks were completed locally:

- The frontend builds successfully.
- The backend starts successfully.
- Text input works.
- Image OCR input works.
- Empty input gives a friendly error.
- Unsupported file uploads give a friendly error.
- The attention model path was tested with a small shape test.
- The frontend and backend response formats now match.

## Live Links

| Service | Link |
| --- | --- |
| Frontend on Vercel | https://frontend-khaki-five-70.vercel.app |
| Render backend deploy link | arey we will add this soon move on :)|


## Deployment

This repository now includes files that make cloud deployment easier:

| File | Purpose |
| --- | --- |
| `frontend/vercel.json` | Helps deploy the frontend on Vercel. |
| `render.yaml` | Helps create the backend service on Render. |
| `backend/Dockerfile` | Builds the backend with Tesseract OCR support. |


Current deployment links:

| Service | Link |
| --- | --- |
| Frontend on Vercel | https://frontend-khaki-five-70.vercel.app |
| Render backend setup | https://render.com/deploy?repo=https://github.com/harsha3358/Medical_Report_Summarizer_with_Clinical_NER |

## Project Folder Guide

```text
backend/
  app.py
  pipeline.py
  ocr_utils.py
  ocr_correction.py
  database.py
  lstm_summarization.py
  lstm_inference.py
  bart_evaluation.py
  compare_models.py
  requirements.txt
  Dockerfile

frontend/
  src/
  package.json
  vercel.json

render.yaml
README.md
```

## How To Run The Project Locally

This section is for developers who want to run the project on their own computer.

Start the backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --host 127.0.0.1 --port 10000
```

Start the frontend:

```bash
cd frontend
npm install
npm run build
npm run start
```

The frontend runs on port `3000`, and the backend runs on port `10000`.

## Important Safety Note

This project is for learning and demonstration only.

The summary and extracted medical terms are AI-generated. They may be incomplete or wrong. Do not use this project for real medical decisions.

Always consult a qualified medical professional for diagnosis, treatment, or urgent health concerns.

## Limitations

- OCR may fail if the image is blurry, handwritten, tilted, or low resolution.
- The clinical entity extraction is rule-based and limited.
- The system may miss rare disease names unless the optional biomedical NER model is enabled.
- Summaries should be reviewed by a human.
- Full model training can take time and may need a good GPU.

## Future Improvements

Useful improvements would include:

- A stronger medical NER model.
- Better support for PDF reports.
- Better handling of handwritten reports.
- More clinical terms in the entity extraction system.
- Final Render backend URL after the backend service is created.
- Authentication and privacy controls for real-world use.

