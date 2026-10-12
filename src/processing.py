import re


def normalize_whitespace(text):
    """Collapse repeated whitespace while preserving meaningful text."""
    if not isinstance(text, str):
        return ""
    return re.sub(r"\s+", " ", text).strip()


def clean_resume_text(text):
    """Clean resume text while preserving technical terms and skills."""
    if not isinstance(text, str):
        return ""

    cleaned = text.replace("\r", " ").replace("\n", " ")
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)
    cleaned = re.sub(r"[^A-Za-z0-9+#.\s/:_-]", " ", cleaned)
    cleaned = normalize_whitespace(cleaned)
    return cleaned.lower()
