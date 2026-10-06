from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(
    resume_text,
    job_text
):

    documents = [
        resume_text,
        job_text
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return similarity


def calculate_multiple_similarities(
    resume_text,
    job_texts
):

    documents = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(
        documents
    )

    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    return similarities