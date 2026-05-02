import re

def correct_text(text):
    text = text.lower()

    # simple normalization
    text = text.replace("0", "o").replace("3", "e").replace("1", "l")

    mapping = {
        "pt": "patient",
        "c/o": "complains of",
        "sob": "shortness of breath",
        "hx": "history",
        "rx": "prescribed"
    }

    for k, v in mapping.items():
        text = re.sub(rf"\b{k}\b", v, text)

    text = re.sub(r'[^a-z0-9\s./-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text