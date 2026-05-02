import re
from symspellpy import SymSpell, Verbosity
import os

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

dictionary_path = os.path.join(os.path.dirname(__file__), "frequency_dictionary_en_82_765.txt")
sym_spell.load_dictionary(dictionary_path, 0, 1)


def normalize_chars(text):
    replacements = {
        "0": "o", "1": "l", "3": "e",
        "5": "s", "@": "a", "$": "s"
    }
    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def merge_fragments(text):
    words = text.split()
    merged = []
    buffer = ""

    for w in words:
        if len(w) <= 2:
            buffer += w
        else:
            if buffer:
                merged.append(buffer + w)
                buffer = ""
            else:
                merged.append(w)

    if buffer:
        merged.append(buffer)

    return " ".join(merged)


def expand_medical(text):
    mapping = {
        "pt": "patient",
        "c/o": "complains of",
        "sob": "shortness of breath",
        "doe": "dyspnea on exertion",
        "hx": "history",
        "copd": "chronic obstructive pulmonary disease",
        "rx": "prescribed",
        "hba1c": "glycated hemoglobin"
    }

    for k, v in mapping.items():
        text = re.sub(rf"\b{k}\b", v, text)

    return text


def spell_correct(text):
    words = text.split()
    corrected = []

    for word in words:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        corrected.append(suggestions[0].term if suggestions else word)

    return " ".join(corrected)


def correct_text(text):
    text = normalize_chars(text)
    text = merge_fragments(text)
    text = expand_medical(text)

    text = re.sub(r'[^a-z\s./-]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    text = spell_correct(text)
    return text