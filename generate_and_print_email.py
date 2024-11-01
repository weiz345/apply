# generate_and_print_emails_from_db.py

import os
import re
import openai
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Resume, Posting
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords', quiet=True)

def preprocess_text(text):
    # Remove non-alphabetic characters
    text = re.sub('[^a-zA-Z]', ' ', text)
    # Lowercase
    text = text.lower()
    # Tokenize and remove stopwords
    words = text.split()
    ps = PorterStemmer()
    words = [ps.stem(w) for w in words if w not in set(stopwords.words('english'))]
    return ' '.join(words)

def fetch_resumes(session, num_resumes=2):
    resumes = session.query(Resume).order_by(Resume.id).limit(num_resumes).all()
    return resumes

def fetch_postings(session, num_postings=2):
    postings = session.query(Posting).order_by(Posting.id).limit(num_postings).all()
    return postings

def generate_cold_email(resume_text, job_posting_text):
    messages = [
        {
            "role": "system",
            "content": "You are an experienced career advisor and expert in crafting professional emails."
        },
        {
            "role": "user",
            "content": f"Based on the following resume and job posting, please draft a concise and persuasive cold email to the hiring manager, expressing interest in the position and highlighting the relevant skills and experiences.\n\nResume:\n{resume_text}\n\nJob Posting:\n{job_posting_text}\n\nCold Email:"
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use 'gpt-3.5-turbo' if 'gpt-4' is not available
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    email = response['choices'][0]['message']['content'].strip()
    return email

def main():
    # Set your OpenAI API key
    openai.api_key = 'sk-OBKbLVUO4SwqPkeIXecluyNG3UZMTsgwtxkNFMTMXST3BlbkFJ-uqUXp2vOniWxOBFMuRuVHtnA4uH5R7e5NODrDrWkA'
    if not openai.api_key:
        print("Please set your OpenAI API key as the environment variable 'OPENAI_API_KEY'")
        return

    # Set up the database session
    engine = create_engine('sqlite:///resumes_postings.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch resumes and postings from the database
    resumes = fetch_resumes(session, num_resumes=3)
    postings = fetch_postings(session, num_postings=3)

    if not resumes or not postings:
        print("No resumes or postings found in the database.")
        return

    # Preprocess texts
    preprocessed_resumes = [preprocess_text(resume.content) for resume in resumes]
    preprocessed_postings = [preprocess_text(posting.content) for posting in postings]

    # Combine documents for vectorization
    all_documents = preprocessed_resumes + preprocessed_postings

    # Vectorize using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)

    # Separate the TF-IDF vectors
    resume_vectors = tfidf_matrix[:len(preprocessed_resumes)]
    posting_vectors = tfidf_matrix[len(preprocessed_resumes):]

    # Compute cosine similarity
    similarity_matrix = cosine_similarity(resume_vectors, posting_vectors)

    # For each resume and job posting pair where similarity > 0.5
    threshold = 0.5
    for i, resume in enumerate(resumes):
        for j, posting in enumerate(postings):
            similarity_score = similarity_matrix[i][j]
            if similarity_score >= threshold:
                print(f"\nSimilarity between Resume ID {resume.id} and Posting ID {posting.id}: {similarity_score:.2f}")
                # Generate cold email
                cold_email = generate_cold_email(resume.content, posting.content)
                # Print the generated cold email
                print(f"\nGenerated Cold Email for Resume ID {resume.id} and Posting ID {posting.id}:\n")
                print(cold_email)
            else:
                print(f"Similarity between Resume ID {resume.id} and Posting ID {posting.id} is below threshold: {similarity_score:.2f}")

    # Close the database session
    session.close()

if __name__ == '__main__':
    main()
