import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    text = re.sub(r'\W+', ' ', text)
    return text.lower()

def rank_resumes(job_description, resumes):
    job_description = clean_text(job_description)
    documents = [job_description] + [clean_text(resume) for resume in resumes]

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    # Cosine similarity
    similarity_scores = cosine_similarity(vectors[0:1], vectors[1:])
    return similarity_scores[0]
