from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_resumes(job_description, resumes):
    # Combine job description with candidate resumes for comparison
    all_texts = [job_description] + [resume.resume_file.read().decode('utf-8') for resume in resumes]  # Assuming resumes are text files
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarity between job description and each resume
    cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    # Rank based on similarity score (higher score means more relevant)
    similarity_scores = cos_sim.flatten()
    ranked_resumes = sorted(zip(resumes, similarity_scores), key=lambda x: x[1], reverse=True)
    
    return [{"candidate": resume.candidate.username, "score": score} for resume, score in ranked_resumes]
