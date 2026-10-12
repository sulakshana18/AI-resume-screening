# AI Resume Screening & Job Matching

This project provides a lightweight Python application for:

- uploading a resume PDF,
- extracting text from readable pages,
- cleaning and preprocessing the resume,
- detecting technical skills,
- comparing the resume against job listings with TF-IDF similarity and skill coverage,
- ranking job opportunities by match score,
- surfacing missing skills and suggested improvements,
- optionally generating AI insights through OpenAI when an API key is configured.

## How to run

1. Create and activate a virtual environment if desired.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Start the app:
   `streamlit run app.py`
4. Upload a resume PDF and use a jobs CSV file if available.

## Job dataset expectations

The app accepts a CSV file with columns such as:

- job_title
- company
- location
- experience_level
- salary
- industry
- required_skills

If the file has different column names, the loader normalizes them automatically and falls back to sensible defaults when optional columns are missing.

## Matching heuristic

The final match score is a heuristic value combining:

- TF-IDF cosine similarity between the resume and the job text,
- skill coverage percentage based on the number of required skills found in the resume.

The formula is:

`match_score = (0.6 * text_similarity) + (0.4 * skill_coverage)`

This is expressed as a percentage and is intended for ranking candidates relative to a job list. It is not a calibrated probability of getting hired.

## OpenAI integration

The AI summary is optional and is only used when the environment variable `OPENAI_API_KEY` is set. The app still works without it and falls back to a simple explanation when the API is unavailable.

## Notes

- PDF extraction gracefully handles unreadable or image-only PDFs by returning a clear message.
- The resume text is kept separate from the cleaned text used for matching.
- Skill extraction intentionally avoids unsafe substring patterns such as matching the letter `c` inside unrelated words.
