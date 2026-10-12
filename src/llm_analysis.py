import os

from openai import OpenAI


def generate_ai_summary(resume_text, job_title, company, matched_skills, missing_skills):
    """Generate optional AI guidance when an OpenAI API key is configured.

    The app works without this key; if it is absent or a request fails, a plain-language
    fallback is returned.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "OpenAI API key not configured. The app is still functional without it. "
            "Use the heuristic match score and skill-gap list to identify the most relevant improvements."
        )

    try:
        client = OpenAI(api_key=api_key)
        prompt = (
            "You are helping analyze a resume against a job opening. "
            "Use only the resume content and skill information provided below. "
            "Do not invent qualifications, experience, or skills that are not present. "
            "Respond with concise but useful guidance.\n\n"
            f"Job title: {job_title}\nCompany: {company}\n"
            f"Matched skills: {', '.join(matched_skills) if matched_skills else 'None'}\n"
            f"Missing skills: {', '.join(missing_skills) if missing_skills else 'None'}\n\n"
            f"Resume excerpt:\n{resume_text[:3000]}"
        )

        response = client.responses.create(
            model="gpt-4o-mini",
            input=[{"role": "user", "content": prompt}],
        )
        return response.output_text.strip() if hasattr(response, "output_text") else str(response)
    except Exception:
        return (
            "AI analysis could not run because the API request failed or the key is invalid. "
            "The skill-gap recommendations remain available without AI assistance."
        )
