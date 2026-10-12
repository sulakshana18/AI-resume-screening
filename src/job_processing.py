def create_job_text(row):
    """Build a searchable job text representation from whatever columns exist."""
    text_parts = []

    for key in [
        "job_title",
        "title",
        "role",
        "position",
        "company",
        "industry",
        "location",
        "experience_level",
        "experience",
        "description",
        "summary",
        "required_skills",
        "skills",
        "keywords",
    ]:
        value = row.get(key, "") if isinstance(row, dict) else getattr(row, key, "")
        if value is None:
            continue
        value = str(value).strip()
        if value and value.lower() != "nan":
            text_parts.append(value)

    return " ".join(text_parts)
