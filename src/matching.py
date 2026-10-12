from src.skill_extraction import extract_skills


def parse_job_skills(required_skills):
    if required_skills is None:
        return []

    if not isinstance(required_skills, str):
        required_skills = str(required_skills)

    normalized = required_skills.lower()
    separators = [",", "|", ";", "/", "\n"]
    for separator in separators:
        normalized = normalized.replace(separator, " ")

    return extract_skills(normalized)


def calculate_skill_match(resume_text, required_skills):
    resume_skills = set(extract_skills(resume_text or ""))
    job_skills = set(parse_job_skills(required_skills))

    matched = resume_skills.intersection(job_skills)
    missing = job_skills.difference(resume_skills)

    if not job_skills:
        coverage = 0.0
    else:
        coverage = len(matched) / len(job_skills)

    return {
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(job_skills),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "skill_match_score": coverage,
        "skill_coverage_percentage": round(coverage * 100, 2),
    }


def compute_final_match_score(text_similarity, skill_coverage):
    """Combine text similarity and skill coverage into a single heuristic score.

    The result is intentionally a heuristic ranking value, not a calibrated probability of
    receiving an interview or job offer.
    """
    text_similarity = max(0.0, min(float(text_similarity), 1.0))
    skill_coverage = max(0.0, min(float(skill_coverage), 1.0))
    score = (0.6 * text_similarity) + (0.4 * skill_coverage)
    return round(score * 100, 2)
