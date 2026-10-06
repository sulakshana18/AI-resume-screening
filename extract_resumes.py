from src.pdf_extractor import extract_all_resumes


PDF_FOLDER = "data/raw/resumes"

OUTPUT_FILE = "data/processed/resumes.csv"


df = extract_all_resumes(
    PDF_FOLDER,
    OUTPUT_FILE
)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst resume:")
print(df.iloc[0]["resume_text"][:1000])