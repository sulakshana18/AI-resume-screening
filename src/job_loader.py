import pandas as pd


def load_jobs(file_path):

    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    required_columns = [
        "job_title",
        "company",
        "location",
        "experience_level",
        "salary",
        "industry",
        "required_skills"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing columns: {missing}"
        )

    return df