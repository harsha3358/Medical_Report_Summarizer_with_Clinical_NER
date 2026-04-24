from backend.utils.config import summarizer

def generate_summary(text):
    if len(text.split()) < 30:
        return text

    max_len = int(len(text.split()) * 0.5)
    min_len = max(10, int(len(text.split()) * 0.2))

    try:
        result = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )
        return result[0]['summary_text']
    except:
        return text