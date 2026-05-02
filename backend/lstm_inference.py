import torch
from lstm_summarization import Encoder, Decoder, encode, idx2word, make_src_mask

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
