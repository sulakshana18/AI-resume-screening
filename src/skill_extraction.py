import re


COMMON_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "nlp",
    "natural language processing",
    "pandas",
    "numpy",
    "scikit-learn",
    "sklearn",
    "tensorflow",
    "pytorch",
    "keras",
    "matplotlib",
    "seaborn",
    "plotly",
    "data analysis",
    "data science",
    "statistics",
    "exploratory data analysis",
    "excel",
    "power bi",
    "tableau",
    "sql server",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "ci/cd",
    "git",
    "github",
    "devops",
    "java",
    "javascript",
    "typescript",
    "react",
    "node.js",
    "nodejs",
    "html",
    "css",
    "flask",
    "django",
    "fastapi",
    "streamlit",
    "api",
    "rest api",
    "microservices",
    "spark",
    "hadoop",
    "airflow",
    "dbt",
    "c++",
    "c#",
    "r",
    "sas",
    "spark sql",
    "computer vision",
    "opencv",
    "pyspark",
    "linux",
    "shell scripting",
    "bash",
    "machine vision",
    "business intelligence",
    "etl",
    "data warehousing",
]


def extract_skills(text):
    """Extract notable technical skills from a resume or job description.

    The implementation intentionally uses exact multi-word and domain-specific skill names,
    avoiding ambiguous single-letter matches such as 'c' inside unrelated words.
    """
    if not isinstance(text, str):
        return []

    normalized = text.lower()
    normalized = re.sub(r"[_/]+", " ", normalized)

    detected = []
    for skill in COMMON_SKILLS:
        pattern = re.escape(skill.lower())
        if re.search(rf"(?<![a-z0-9#.+]){pattern}(?![a-z0-9#.+])", normalized):
            detected.append(skill)

    return sorted(set(detected))
