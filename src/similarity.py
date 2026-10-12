from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_text):
    """Compute cosine similarity for a single resume-job pair."""
    if not resume_text or not job_text:
        return 0.0

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([resume_text, job_text])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return float(similarity)


def calculate_multiple_similarities(resume_text, job_texts):
    """Compute TF-IDF cosine similarities across all job descriptions."""
    if not isinstance(job_texts, list):
        job_texts = list(job_texts)

    if not resume_text or not job_texts:
        return []

    documents = [resume_text] + [job_text or "" for job_text in job_texts]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    vectors = vectorizer.fit_transform(documents)
    similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]
    return similarities.tolist()
