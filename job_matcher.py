import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_job_roles():
    return pd.read_csv("data/job_roles.csv")


def calculate_match_scores(resume_text):
    jobs = load_job_roles()

    documents = [resume_text]

    for skills in jobs["skills"]:
        documents.append(skills)

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    resume_vector = vectors[0]

    job_vectors = vectors[1:]

    similarities = cosine_similarity(
        resume_vector,
        job_vectors
    )[0]

    jobs["score"] = similarities * 100

    jobs = jobs.sort_values(
        "score",
        ascending=False
    )

    return jobs.reset_index(drop=True)


def find_missing_skills(resume_skills, required_skills):
    resume_skills_lower = [
        skill.lower()
        for skill in resume_skills
    ]

    missing = []

    for skill in required_skills:

        if skill.lower() not in resume_skills_lower:
            missing.append(skill)

    return missing