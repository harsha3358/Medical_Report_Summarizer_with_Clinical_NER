"""
compare_models.py
-----------------
Runs the full ablation study:
  • LSTM (no attention)   — ROUGE-1, ROUGE-2, ROUGE-L
  • LSTM + Attention      — ROUGE-1, ROUGE-2, ROUGE-L
  • BART-Large-CNN        — ROUGE-1, ROUGE-2, ROUGE-L

Prints a side-by-side comparison table.
"""

from lstm_summarization import train_model, evaluate
from bart_evaluation import evaluate_bart

print("Training LSTM (no attention)...")
enc1, dec1 = train_model(use_attention=False)

print("Training LSTM + Attention...")
enc2, dec2 = train_model(use_attention=True)

print("Evaluating LSTM (no attention)...")
lstm_scores = evaluate(enc1, dec1)

print("Evaluating LSTM + Attention...")
attn_scores = evaluate(enc2, dec2)

print("Evaluating BART-Large-CNN...")
bart_scores = evaluate_bart()

# -------------------------------
# FINAL COMPARISON TABLE
# -------------------------------
print("\n" + "=" * 60)
print(f"{'Model':<28} {'ROUGE-1':>8} {'ROUGE-2':>8} {'ROUGE-L':>8}")
print("-" * 60)
print(
    f"{'LSTM (no attention)':<28}"
    f" {lstm_scores['rouge1']:>8.3f}"
    f" {lstm_scores['rouge2']:>8.3f}"
    f" {lstm_scores['rougeL']:>8.3f}"
)
print(
    f"{'LSTM + Attention':<28}"
    f" {attn_scores['rouge1']:>8.3f}"
    f" {attn_scores['rouge2']:>8.3f}"
    f" {attn_scores['rougeL']:>8.3f}"
)
print(
    f"{'BART-Large-CNN':<28}"
    f" {bart_scores['rouge1']:>8.3f}"
    f" {bart_scores['rouge2']:>8.3f}"
    f" {bart_scores['rougeL']:>8.3f}"
)
print("=" * 60)