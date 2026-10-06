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
    try:
        reader = PdfReader(pdf_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return clean_text(" ".join(pages))

    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


def extract_all_resumes(pdf_folder, output_file):

    records = []

    pdf_files = [
        file for file in os.listdir(pdf_folder)
        if file.lower().endswith(".pdf")
    ]

    print(f"Found {len(pdf_files)} PDF files.")

    for index, filename in enumerate(
        tqdm(pdf_files, desc="Extracting resumes")
    ):

        pdf_path = os.path.join(pdf_folder, filename)

        resume_text = extract_text_from_pdf(pdf_path)

        if resume_text:

            records.append({
                "resume_id": index + 1,
                "file_name": filename,
                "resume_text": resume_text,
                "text_length": len(resume_text)
            })

    df = pd.DataFrame(records)

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8"
    )

    print("\nResume extraction completed.")
    print(f"Total resumes extracted: {len(df)}")

    return df