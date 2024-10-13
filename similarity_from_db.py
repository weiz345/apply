# similarity_from_db.py

import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Resume, Posting
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download NLTK data (only the first time)
nltk.download('stopwords')

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
    # Create the database session
    engine = create_engine('sqlite:///resumes_postings.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch resumes and postings
    resumes = session.query(Resume).order_by(Resume.id).all()
    postings = session.query(Posting).order_by(Posting.id).all()

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
        index=[f'Resume {i+1}' for i in range(len(resumes))],
        columns=[f'Job Posting {j+1}' for j in range(len(postings))]
    )

    # Display the similarity matrix
    print("Similarity Matrix (Resumes vs. Job Postings):\n")
    print(similarity_df)

    session.close()

if __name__ == '__main__':
    main()
