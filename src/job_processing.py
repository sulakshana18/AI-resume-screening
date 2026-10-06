def create_job_text(row):
    
    job_title = str(
        row.get("job_title", "")
    )

    industry = str(
        row.get("industry", "")
    )

    experience = str(
        row.get("experience_level", "")
    )

    skills = str(
        row.get("required_skills", "")
    )

    job_text = (
        job_title + " "
        + industry + " "
        + experience + " "
        + skills
    )

    return job_text