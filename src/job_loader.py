import os

import pandas as pd

from src.job_processing import create_job_text


def _normalize_columns(columns):
    normalized = []
    for column in columns:
        clean = str(column).strip().lower().replace(" ", "_")
        normalized.append(clean)
    return normalized


def _apply_aliases(df):
    alias_map = {
        "job_title": ["job_title", "title", "role", "position"],
        "company": ["company", "employer", "organization"],
        "location": ["location", "city", "work_location"],
        "experience_level": ["experience_level", "experience", "seniority"],
        "salary": ["salary", "salary_range", "compensation"],
        "industry": ["industry", "sector"],
        "required_skills": ["required_skills", "skills", "skill_set", "job_skills", "keywords"],
        "description": ["description", "job_description", "summary"],
    }

    for canonical_name, aliases in alias_map.items():
        match = next((alias for alias in aliases if alias in df.columns), None)
        if match is not None and canonical_name not in df.columns:
            df.rename(columns={match: canonical_name}, inplace=True)

    return df


def load_jobs(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Job dataset file not found: {file_path}")

    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("The supplied job dataset is empty.")

    df.columns = _normalize_columns(df.columns)
    df = _apply_aliases(df)

    if "job_title" not in df.columns:
        raise ValueError(
            "The job dataset must include a job title column (for example: job_title or title)."
        )

    for column in ["company", "location", "experience_level", "industry"]:
        if column not in df.columns:
            df[column] = ""

    if "required_skills" not in df.columns:
        df["required_skills"] = ""

    for column in ["company", "location", "experience_level", "industry", "required_skills", "salary", "description"]:
        if column not in df.columns:
            df[column] = ""

    df["required_skills"] = df["required_skills"].fillna("").astype(str)
    df["job_text"] = df.apply(create_job_text, axis=1)
    df = df[df["job_text"].fillna(" ").str.strip() != ""].copy()

    return df
