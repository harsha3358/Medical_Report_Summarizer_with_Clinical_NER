import torch
from transformers import pipeline
from rouge_score import rouge_scorer
from datasets import load_dataset

DEVICE = 0 if torch.cuda.is_available() else -1

# -------------------------------
# LOAD DATA (same as LSTM)
# -------------------------------
dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:500]")

texts = [x["article"][:300] for x in dataset]
summaries = [x["highlights"][:100] for x in dataset]

# -------------------------------
# LOAD BART MODEL
# -------------------------------
print("Loading BART model...")
bart = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=DEVICE
)

# -------------------------------
# GENERATE SUMMARY
# -------------------------------
def bart_summary(text):
    try:
        output = bart(
            text,
            max_length=100,
            min_length=30,
            do_sample=False
        )[0]["summary_text"]
        return output
    except:
        return ""

# -------------------------------
# EVALUATION
# -------------------------------
def evaluate_bart():
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeL"],
        use_stemmer=True
    )

    scores = {
        "rouge1": [],
        "rouge2": [],
        "rougeL": []
    }

    for i in range(len(texts)):
        pred = bart_summary(texts[i])
        ref = summaries[i]

        score = scorer.score(ref, pred)

        scores["rouge1"].append(score["rouge1"].fmeasure)
        scores["rouge2"].append(score["rouge2"].fmeasure)
        scores["rougeL"].append(score["rougeL"].fmeasure)

        if i % 50 == 0:
            print(f"Processed {i}/{len(texts)}")

    avg_scores = {
        k: sum(v) / len(v)
        for k, v in scores.items()
    }

    return avg_scores

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    results = evaluate_bart()

    print("\nBART RESULTS:")
    print(f"ROUGE-1: {results['rouge1']:.3f}")
    print(f"ROUGE-2: {results['rouge2']:.3f}")
    print(f"ROUGE-L: {results['rougeL']:.3f}")