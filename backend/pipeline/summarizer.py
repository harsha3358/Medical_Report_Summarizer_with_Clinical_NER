def generate_summary(text):
    if not text.strip():
        return ""

    result = summarizer(
        text,
        max_length=60,
        min_length=20,
        do_sample=False,
        repetition_penalty=2.0
    )

    summary = result[0]["summary_text"]

    # Remove repeated words
    words = summary.split()
    seen = []
    for w in words:
        if w not in seen:
            seen.append(w)

    return " ".join(seen)
