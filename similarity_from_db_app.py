# similarity_from_db_with_app_context.py

import re
import numpy as np
import pandas as pd
from flask import current_app
from app import app, db, Resume, Posting
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK data (only required once)
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

def main():
    with app.app_context():
        # Fetch resumes and postings from the database
        resumes = Resume.query.order_by(Resume.id).all()
        postings = Posting.query.order_by(Posting.id).all()

        # Check if data exists
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

        # Round the similarity scores
        similarity_matrix = np.round(similarity_matrix, 2)

        # Create a DataFrame
        similarity_df = pd.DataFrame(
            similarity_matrix,
            index=[f'Resume {resume.id}' for resume in resumes],
            columns=[f'Job Posting {posting.id}' for posting in postings]
        )

        # Display the similarity matrix
        print("Similarity Matrix (Resumes vs. Job Postings):\n")
        print(similarity_df)

if __name__ == '__main__':
    main()
