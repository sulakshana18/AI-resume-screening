import re


def clean_resume_text(text):

    if not isinstance(text, str):
        return ""

    text = text.lower()

    # Remove email
    text = re.sub(
        r'\S+@\S+',
        ' ',
        text
    )

    # Remove URLs
    text = re.sub(
        r'http\S+|www\S+',
        ' ',
        text
    )

    # Remove special characters
    text = re.sub(
        r'[^a-zA-Z0-9\s]',
        ' ',
        text
    )

    # Remove extra spaces
    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text.strip()