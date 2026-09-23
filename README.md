# AI Resume Analyzer and Job Recommendation System

## Project Overview

The AI Resume Analyzer and Job Recommendation System is a Python-based application that analyzes resumes and recommends suitable job roles based on the skills found in the resume.

The system extracts text from PDF and DOCX resumes, cleans the extracted text, identifies technical skills, compares the resume with different job roles, and provides job recommendations along with missing skills and a learning roadmap.

## Objectives

- Extract text from PDF and DOCX resumes.
- Clean and preprocess resume text.
- Identify technical skills from resumes.
- Match resumes with suitable job roles.
- Calculate a match score for different job roles.
- Display the top 3 recommended job roles.
- Identify missing skills for a selected role.
- Generate a learning roadmap for missing skills.
- Provide an interactive Streamlit dashboard.

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- PyPDF
- Python-docx
- TF-IDF
- Cosine Similarity

## Project Structure

```text
ai_resume_analyzer/
│
├── app.py
├── resume_parser.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── data/
│   ├── job_roles.csv
│   └── skill_dictionary.csv
│
├── sample_resumes/
│
├── reports/
│
└── tests/
    └── test_cases.csv