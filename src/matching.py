from src.skill_extraction import extract_skills


def parse_job_skills(required_skills):

    if not isinstance(required_skills, str):
        return []

    skills = required_skills.lower()

    skills = (
        skills
        .replace(",", " ")
        .replace("|", " ")
        .replace(";", " ")
    )

    return extract_skills(skills)


def calculate_skill_match(
    resume_text,
    required_skills
):

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        parse_job_skills(required_skills)
    )

    matched = resume_skills.intersection(
        job_skills
    )

    missing = job_skills.difference(
        resume_skills
    )

    if len(job_skills) == 0:
        score = 0

    else:
        score = (
            len(matched)
            / len(job_skills)
        )

    return {
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(job_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "skill_match_score": score
    }