import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils.rnn import pad_packed_sequence, pad_sequence, pack_padded_sequence
from datasets import load_dataset
from rouge_score import rouge_scorer
from collections import Counter
import random

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------------------------------
# LOAD DATA (subset for speed)
# -------------------------------
dataset = load_dataset("cnn_dailymail", "3.0.0", split="train[:5000]")

texts = [x["article"][:300] for x in dataset]
summaries = [x["highlights"][:100] for x in dataset]

# -------------------------------
# SIMPLE TOKENIZER
# -------------------------------
def tokenize(text):
    return text.lower().split()

vocab = Counter()
for text in texts + summaries:
    vocab.update(tokenize(text))

word2idx = {w: i+2 for i, (w, _) in enumerate(vocab.most_common(20000))}
word2idx["<pad>"] = 0
word2idx["<unk>"] = 1
idx2word = {i: w for w, i in word2idx.items()}

def encode(text):
    return torch.tensor([word2idx.get(w, 1) for w in tokenize(text)])

# -------------------------------
# DATASET
# -------------------------------
pairs = [(encode(t), encode(s)) for t, s in zip(texts, summaries)]

def collate(batch):
    src, tgt = zip(*batch)
    src_lens = [len(x) for x in src]
    src_pad = pad_sequence(src, batch_first=True)
    tgt_pad = pad_sequence(tgt, batch_first=True)
    return src_pad, tgt_pad, src_lens

loader = torch.utils.data.DataLoader(
    pairs, batch_size=32, shuffle=True, collate_fn=collate
)

# -------------------------------
# MODEL
# -------------------------------
class Encoder(nn.Module):
    def __init__(self, vocab_size, emb=256, hid=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb)
        self.lstm = nn.LSTM(emb, hid, num_layers=2, batch_first=True)

    def forward(self, x, lengths):
        x = self.embedding(x)
        packed = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        packed_outputs, (h, c) = self.lstm(packed)
        outputs, _ = pad_packed_sequence(packed_outputs, batch_first=True)
        return outputs, (h, c)

class Attention(nn.Module):
    def __init__(self, hid):
        super().__init__()

    def forward(self, hidden, encoder_outputs, src_mask=None):
        scores = torch.bmm(encoder_outputs, hidden.unsqueeze(2)).squeeze(2)
        if src_mask is not None:
            scores = scores.masked_fill(~src_mask, -1e9)
        weights = torch.softmax(scores, dim=1)
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context

class Decoder(nn.Module):
    def __init__(self, vocab_size, emb=256, hid=512, use_attention=False):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, emb)
        self.lstm = nn.LSTM(emb, hid, num_layers=2, batch_first=True)
        self.fc = nn.Linear(hid, vocab_size)
        self.use_attention = use_attention
        if use_attention:
            self.attn = Attention(hid)

    def forward(self, x, hidden, encoder_outputs=None, src_mask=None):
        x = self.embedding(x).unsqueeze(1)
        out, hidden = self.lstm(x, hidden)

        if self.use_attention:
            if encoder_outputs is None:
                raise ValueError("encoder_outputs are required when attention is enabled")
            context = self.attn(out.squeeze(1), encoder_outputs, src_mask)
            out = out.squeeze(1) + context
        else:
            out = out.squeeze(1)

        return self.fc(out), hidden

def make_src_mask(src, lengths):
    max_len = src.size(1)
    lens = torch.tensor(lengths, device=src.device).unsqueeze(1)
    return torch.arange(max_len, device=src.device).unsqueeze(0) < lens

# -------------------------------
# TRAIN FUNCTION
# -------------------------------
def train_model(use_attention=False, epochs=2):
    encoder = Encoder(len(word2idx)).to(DEVICE)
    decoder = Decoder(len(word2idx), use_attention=use_attention).to(DEVICE)

    optim_all = optim.Adam(list(encoder.parameters()) + list(decoder.parameters()))
    loss_fn = nn.CrossEntropyLoss(ignore_index=0)

    for epoch in range(epochs):
        for src, tgt, lens in loader:
            src, tgt = src.to(DEVICE), tgt.to(DEVICE)

            encoder_outputs, hidden = encoder(src, lens)
            src_mask = make_src_mask(src, lens)

            loss = 0
            input_tok = tgt[:, 0]

            for t in range(1, tgt.size(1)):
                output, hidden = decoder(input_tok, hidden, encoder_outputs, src_mask)
                loss += loss_fn(output, tgt[:, t])

                teacher = random.random() < 0.5
                input_tok = tgt[:, t] if teacher else output.argmax(1)

            optim_all.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(encoder.parameters(), 1.0)
            optim_all.step()

        print(f"Epoch {epoch} Loss: {loss.item()}")

    return encoder, decoder

# -------------------------------
# GENERATE SUMMARY
# -------------------------------
def generate_summary(encoder, decoder, text):
    encoder.eval()
    decoder.eval()

    src = encode(text).unsqueeze(0).to(DEVICE)
    lengths = [len(src[0])]
    encoder_outputs, hidden = encoder(src, lengths)
    src_mask = make_src_mask(src, lengths)

    input_tok = torch.tensor([1]).to(DEVICE)
    result = []

    for _ in range(30):
        out, hidden = decoder(input_tok, hidden, encoder_outputs, src_mask)
        pred = out.argmax(1)
        word = idx2word.get(pred.item(), "")

        if word == "<pad>":
            break

        result.append(word)
        input_tok = pred

    return " ".join(result)

# -------------------------------
# EVALUATION — ROUGE-1, ROUGE-2, ROUGE-L
# -------------------------------
def evaluate(encoder, decoder, num_samples=100):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

    rouge1_scores, rouge2_scores, rougeL_scores = [], [], []

    for i in range(min(num_samples, len(texts))):
        pred = generate_summary(encoder, decoder, texts[i])
        ref = summaries[i]

        score = scorer.score(ref, pred)
        rouge1_scores.append(score["rouge1"].fmeasure)
        rouge2_scores.append(score["rouge2"].fmeasure)
        rougeL_scores.append(score["rougeL"].fmeasure)

    return {
        "rouge1": sum(rouge1_scores) / len(rouge1_scores),
        "rouge2": sum(rouge2_scores) / len(rouge2_scores),
        "rougeL": sum(rougeL_scores) / len(rougeL_scores),
    }

# -------------------------------
# RUN EXPERIMENT
# -------------------------------
if __name__ == "__main__":
    print("Training LSTM (no attention)...")
    enc1, dec1 = train_model(use_attention=False)

    print("Training LSTM + Attention...")
    enc2, dec2 = train_model(use_attention=True)

    print("Evaluating LSTM (no attention)...")
    scores1 = evaluate(enc1, dec1)

    print("Evaluating LSTM + Attention...")
    scores2 = evaluate(enc2, dec2)

    print("\n" + "="*55)
    print(f"{'Model':<25} {'ROUGE-1':>8} {'ROUGE-2':>8} {'ROUGE-L':>8}")
    print("-"*55)
    print(
        f"{'LSTM (no attention)':<25}"
        f" {scores1['rouge1']:>8.3f}"
        f" {scores1['rouge2']:>8.3f}"
        f" {scores1['rougeL']:>8.3f}"
    )
    print(
        f"{'LSTM + Attention':<25}"
        f" {scores2['rouge1']:>8.3f}"
        f" {scores2['rouge2']:>8.3f}"
        f" {scores2['rougeL']:>8.3f}"
    )
    print("="*55)

    # Optionally save trained weights for use in pipeline.py
    import torch
    torch.save(enc2.state_dict(), "encoder.pt")
    torch.save(dec2.state_dict(), "decoder.pt")
    print("\nSaved LSTM+Attention weights → encoder.pt, decoder.pt")
