from lstm_summarization import train_model, evaluate
from bart_evaluation import evaluate_bart

print("Training LSTM...")
enc1, dec1 = train_model(use_attention=False)

print("Training LSTM + Attention...")
enc2, dec2 = train_model(use_attention=True)

print("Evaluating LSTM...")
lstm_score = evaluate(enc1, dec1)

print("Evaluating LSTM + Attention...")
attn_score = evaluate(enc2, dec2)

print("Evaluating BART...")
bart_scores = evaluate_bart()

# -------------------------------
# FINAL TABLE
# -------------------------------
print("\n=== FINAL COMPARISON ===")

print(f"LSTM ROUGE-L: {lstm_score:.3f}")
print(f"LSTM+Attention ROUGE-L: {attn_score:.3f}")

print(f"BART ROUGE-1: {bart_scores['rouge1']:.3f}")
print(f"BART ROUGE-2: {bart_scores['rouge2']:.3f}")
print(f"BART ROUGE-L: {bart_scores['rougeL']:.3f}")