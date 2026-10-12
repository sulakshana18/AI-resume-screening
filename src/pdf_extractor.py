import os
import re

import pandas as pd
from pypdf import PdfReader
from tqdm import tqdm


def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\x00-\x7F]+", " ", text)
    return text.strip()


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF and return an empty string if text extraction fails."""
    try:
        reader = PdfReader(pdf_path)
        pages = []

        for page in reader.pages:
            try:
                page_text = page.extract_text()
            except Exception:
                page_text = ""

            if page_text and page_text.strip():
                pages.append(page_text)

        extracted = " ".join(pages)
        cleaned = clean_text(extracted)

        if not cleaned:
            return "", "No extractable text found. This PDF may be scanned, image-only, or password protected; OCR may be required."

        return cleaned, ""
    except Exception as exc:
        return "", f"Could not read the PDF: {exc}"


def extract_all_resumes(pdf_folder, output_file):
    if not os.path.isdir(pdf_folder):
        raise FileNotFoundError(f"PDF folder not found: {pdf_folder}")

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.lower().endswith(".pdf")
    ]

    if not pdf_files:
        raise FileNotFoundError(f"No PDF resumes were found in {pdf_folder}.")

    records = []
    for index, filename in enumerate(tqdm(pdf_files, desc="Extracting resumes")):
        pdf_path = os.path.join(pdf_folder, filename)
        resume_text, error_message = extract_text_from_pdf(pdf_path)

        if resume_text:
            records.append({
                "resume_id": index + 1,
                "file_name": filename,
                "resume_text": resume_text,
                "text_length": len(resume_text),
            })

    df = pd.DataFrame(records)
    df.to_csv(output_file, index=False, encoding="utf-8")
    return df
