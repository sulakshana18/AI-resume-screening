import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.job_loader import load_jobs
from src.matching import calculate_skill_match, compute_final_match_score
from src.pdf_extractor import extract_text_from_pdf
from src.processing import clean_resume_text
from src.similarity import calculate_multiple_similarities
from src.skill_extraction import extract_skills
from src.llm_analysis import generate_ai_summary

load_dotenv()

st.set_page_config(page_title="AI Resume Screening", page_icon="📄", layout="wide")


def find_job_dataset():
    candidates = [
        Path("data/jobs.csv"),
        Path("data/processed/jobs.csv"),
        Path("jobs.csv"),
        Path("data/raw/jobs.csv"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_job_dataframe(uploaded_file=None):
    dataset_path = find_job_dataset()
    if uploaded_file is not None:
        temp_path = Path(".tmp_jobs_upload.csv")
        try:
            uploaded_file.seek(0)
            with open(temp_path, "wb") as output_file:
                output_file.write(uploaded_file.read())
            return load_jobs(str(temp_path))
        except Exception as exc:
            st.error(f"Unable to read the uploaded job dataset: {exc}")
            return None
        finally:
            try:
                os.remove(temp_path)
            except FileNotFoundError:
                pass

    if dataset_path is not None:
        try:
            return load_jobs(str(dataset_path))
        except Exception as exc:
            st.error(f"The job dataset could not be loaded: {exc}")
            return None

    return None


def extract_resume_from_pdf(file_obj):
    if file_obj is None:
        return "", "Please upload a PDF resume."

    try:
        temp_path = Path(".tmp_resume.pdf")
        with open(temp_path, "wb") as output_file:
            output_file.write(file_obj.read())

        raw_text, error_message = extract_text_from_pdf(str(temp_path))
        if raw_text:
            return raw_text, ""
        return "", error_message or "No text could be extracted from the PDF."
    except Exception as exc:  # pragma: no cover - defensive user-facing path
        return "", f"Could not process the uploaded PDF: {exc}"
    finally:
        try:
            os.remove(".tmp_resume.pdf")
        except FileNotFoundError:
            pass


def rank_jobs(resume_text, jobs_df):
    if jobs_df is None or jobs_df.empty:
        return []

    resume_clean = clean_resume_text(resume_text)
    job_texts = jobs_df["job_text"].fillna("").tolist()
    text_scores = calculate_multiple_similarities(resume_clean, job_texts)

    rankings = []
    for index, row in jobs_df.iterrows():
        skill_match = calculate_skill_match(resume_clean, row.get("required_skills", ""))
        similarity = float(text_scores[index]) if index < len(text_scores) else 0.0
        final_score = compute_final_match_score(similarity, skill_match["skill_match_score"])
        rankings.append(
            {
                "job_index": index,
                "job_title": str(row.get("job_title", "Unknown job")),
                "company": str(row.get("company", "")),
                "location": str(row.get("location", "")),
                "experience_level": str(row.get("experience_level", "")),
                "industry": str(row.get("industry", "")),
                "salary": str(row.get("salary", "")),
                "required_skills": str(row.get("required_skills", "")),
                "matched_skills": skill_match["matched_skills"],
                "missing_skills": skill_match["missing_skills"],
                "skill_coverage": skill_match["skill_coverage_percentage"],
                "text_similarity": round(similarity * 100, 2),
                "match_score": final_score,
                "description": str(row.get("description", row.get("job_text", ""))),
            }
        )

    return sorted(rankings, key=lambda item: item["match_score"], reverse=True)


st.title("AI Resume Screening & Job Matching")
st.caption("Upload a resume, compare it with job listings, and review match quality with a skill-gap view.")

sidebar = st.sidebar
sidebar.header("Controls")
job_csv = sidebar.file_uploader("Upload a jobs CSV (optional)", type=["csv"])

jobs_df = load_job_dataframe(job_csv)

if jobs_df is None:
    st.warning("No valid job dataset was found. Upload a CSV with columns like job_title, company, location, experience_level, salary, industry, and required_skills, or place one in data/jobs.csv.")
else:
    st.metric("Available Job Listings", len(jobs_df))

resume_file = st.file_uploader("Upload resume PDF", type=["pdf"])

summary_container = st.container()

if resume_file is not None:
    raw_resume_text, extraction_error = extract_resume_from_pdf(resume_file)
    if extraction_error:
        st.warning(extraction_error)

    if raw_resume_text:
        cleaned_resume_text = clean_resume_text(raw_resume_text)
        extracted_skills = extract_skills(cleaned_resume_text)

        summary_container.subheader("Resume analysis")
        st.write("Resume text preview:")
        st.text_area("", cleaned_resume_text[:4000], height=220, disabled=True)

        st.write(f"Detected skills ({len(extracted_skills)}):")
        if extracted_skills:
            st.write(", ".join(extracted_skills))
        else:
            st.info("No skills were detected. Add more project or technical details to improve matching.")

        if jobs_df is not None:
            matches = rank_jobs(raw_resume_text, jobs_df)

            if matches:
                st.subheader("Recommended jobs")
                selected_job = st.selectbox(
                    "Select a job to inspect",
                    options=[f"{item['job_title']} @ {item['company']}" for item in matches],
                )
                selected_detail = next(item for item in matches if f"{item['job_title']} @ {item['company']}" == selected_job)

                for item in matches[:10]:
                    with st.container():
                        col_title, col_score = st.columns([3, 1])
                        with col_title:
                            st.markdown(f"### {item['job_title']}")
                            st.caption(f"{item['company']} • {item['location']} • {item['industry']} • {item['experience_level']}")
                        with col_score:
                            st.metric("Match score", f"{item['match_score']}%")
                        st.write(f"Matched skills: {', '.join(item['matched_skills']) if item['matched_skills'] else 'None'}")
                        st.write(f"Missing skills: {', '.join(item['missing_skills']) if item['missing_skills'] else 'None'}")
                        if item['salary']:
                            st.write(f"Salary: {item['salary']}")
                        st.write(f"Text similarity: {item['text_similarity']}% | Skill coverage: {item['skill_coverage']}%")
                        st.markdown("---")

                st.subheader("Selected job details")
                st.write(f"Job title: {selected_detail['job_title']}")
                st.write(f"Company: {selected_detail['company']}")
                st.write(f"Location: {selected_detail['location']}")
                st.write(f"Experience level: {selected_detail['experience_level']}")
                st.write(f"Industry: {selected_detail['industry']}")
                st.write(f"Salary: {selected_detail['salary'] or 'Not specified'}")
                st.write(f"Matched skills: {', '.join(selected_detail['matched_skills']) if selected_detail['matched_skills'] else 'None'}")
                st.write(f"Missing skills: {', '.join(selected_detail['missing_skills']) if selected_detail['missing_skills'] else 'None'}")
                st.write(selected_detail['description'])

                ai_summary = generate_ai_summary(
                    resume_text=raw_resume_text,
                    job_title=selected_detail["job_title"],
                    company=selected_detail["company"],
                    matched_skills=selected_detail["matched_skills"],
                    missing_skills=selected_detail["missing_skills"],
                )
                st.subheader("AI-generated insight")
                st.write(ai_summary)
            else:
                st.info("No job matches were generated. Add more job data or improve the resume text quality.")
        else:
            st.info("Upload a job dataset to see job recommendations.")

else:
    st.info("Upload a PDF resume to begin analysis.")

st.sidebar.caption("This application uses a heuristic match score combining TF-IDF similarity and skill coverage. It is not a calibrated probability of getting hired.")
