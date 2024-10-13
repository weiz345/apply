import sqlite3
import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

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

def fetch_data_from_database():
    conn = sqlite3.connect('resumes_postings.db')
    cursor = conn.cursor()

    # Fetch resumes
    cursor.execute('SELECT filename, content FROM resumes ORDER BY id')
    resumes_data = cursor.fetchall()
    resume_filenames = [row[0] for row in resumes_data]
    resumes = [row[1] for row in resumes_data]

    # Fetch postings
    cursor.execute('SELECT filename, content FROM postings ORDER BY id')
    postings_data = cursor.fetchall()
    posting_filenames = [row[0] for row in postings_data]
    postings = [row[1] for row in postings_data]

    conn.close()
    return resumes, resume_filenames, postings, posting_filenames

def main():
    # Fetch resumes and job postings from the database
    resumes, resume_filenames, postings, posting_filenames = fetch_data_from_database()

    # Preprocess the texts
    preprocessed_resumes = [preprocess_text(resume) for resume in resumes]
    preprocessed_postings = [preprocess_text(posting) for posting in postings]

    # Combine documents for vectorization
    all_documents = preprocessed_resumes + preprocessed_postings

    # Vectorize the documents using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(all_documents)

    # Separate the TF-IDF vectors for resumes and postings
    resume_vectors = tfidf_matrix[:len(preprocessed_resumes)]
    posting_vectors = tfidf_matrix[len(preprocessed_resumes):]

    # Compute the cosine similarity matrix
    similarity_matrix = cosine_similarity(resume_vectors, posting_vectors)

    # Round the similarity scores for better readability
    similarity_matrix = np.round(similarity_matrix, 2)

    # Create a DataFrame for the similarity matrix
    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=[f'Resume {i+1}' for i in range(len(preprocessed_resumes))],
        columns=[f'Job Posting {j+1}' for j in range(len(preprocessed_postings))]
    )

    # Display the similarity matrix
    print("Similarity Matrix (Resumes vs. Job Postings):\n")
    print(similarity_df)

if __name__ == '__main__':
    main()
