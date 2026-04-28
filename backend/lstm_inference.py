import torch
from lstm_summarization import Encoder, Decoder, encode, idx2word

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load trained weights (after training once)
encoder = Encoder(len(idx2word)).to(DEVICE)
decoder = Decoder(len(idx2word), use_attention=True).to(DEVICE)

encoder.load_state_dict(torch.load("encoder.pt", map_location=DEVICE))
decoder.load_state_dict(torch.load("decoder.pt", map_location=DEVICE))

encoder.eval()
decoder.eval()

def lstm_generate(text):
    src = encode(text).unsqueeze(0).to(DEVICE)
    _, hidden = encoder(src, [len(src[0])])

    input_tok = torch.tensor([1]).to(DEVICE)
    result = []

    for _ in range(30):
        out, hidden = decoder(input_tok, hidden)
        pred = out.argmax(1)
        word = idx2word.get(pred.item(), "")

        if word == "<pad>":
            break

        result.append(word)
        input_tok = pred

    return " ".join(result)