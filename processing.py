# processing.py

from factory import create_app
from models import db, Resume, Posting, UserEmail, Recruiter
import os
import re
import openai
import numpy as np
from sqlalchemy.orm import scoped_session, sessionmaker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Download NLTK stopwords if not already downloaded
nltk.download('stopwords', quiet=True)

# Set your OpenAI API key and email password
openai.api_key = os.getenv('OPENAI_API_KEY')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

app = create_app()

def preprocess_text(text):
    text = re.sub('[^a-zA-Z]', ' ', text)
    text = text.lower()
    words = text.split()
    ps = PorterStemmer()
    words = [ps.stem(w) for w in words if w not in set(stopwords.words('english'))]
    return ' '.join(words)

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
        model="gpt-4",
        messages=messages,
        max_tokens=500,
        temperature=0.7
    )

    email = response['choices'][0]['message']['content'].strip()
    return email

def send_email(sender_email, sender_password, recipient_email, email_body, user_name):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Application for the Position"

    msg.attach(MIMEText(email_body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent successfully from {user_name} to {recipient_email}!")
    except Exception as e:
        print(f"Error sending email from {user_name} to {recipient_email}: {e}")

def process_new_resume(resume_id):
    with app.app_context():
        # Create a new session
        Session = scoped_session(sessionmaker(bind=db.engine))
        session = Session()

        # Fetch the new resume
        resume = session.query(Resume).get(resume_id)
        if not resume:
            print(f"Resume with ID {resume_id} not found.")
            session.remove()
            return

        # Fetch all postings
        postings = session.query(Posting).all()

        if postings:
            preprocessed_resume = preprocess_text(resume.content)
            preprocessed_postings = [preprocess_text(posting.content) for posting in postings]

            documents = [preprocessed_resume] + preprocessed_postings

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

            resume_vector = tfidf_matrix[0]
            posting_vectors = tfidf_matrix[1:]

            similarity_scores = cosine_similarity(resume_vector, posting_vectors)[0]

            threshold = 0.5

            for idx, score in enumerate(similarity_scores):
                if score >= threshold:
                    matching_posting = postings[idx]
                    print(f"Similarity between Resume ID {resume.id} and Posting ID {matching_posting.id}: {score:.2f}")

                    cold_email = generate_cold_email(resume.content, matching_posting.content)
                    print(f"\nGenerated Cold Email for Resume ID {resume.id} and Posting ID {matching_posting.id}:\n")
                    print(cold_email)

                    user_email_entries = resume.user_emails
                    if not user_email_entries:
                        print(f"No user emails associated with Resume ID {resume.id}")
                        continue

                    recruiter_email_entries = matching_posting.recruiters
                    if not recruiter_email_entries:
                        print(f"No recruiter emails associated with Posting ID {matching_posting.id}")
                        continue

                    for user_email_entry in user_email_entries:
                        sender_email = user_email_entry.email
                        user_name = sender_email.split('@')[0]
                        sender_password = SENDER_PASSWORD

                        for recruiter_email_entry in recruiter_email_entries:
                            recipient_email = recruiter_email_entry.email
                            send_email(sender_email, sender_password, recipient_email, cold_email, user_name)
                else:
                    print(f"Similarity between Resume ID {resume.id} and Posting ID {postings[idx].id} is below threshold: {score:.2f}")
        else:
            print("No postings to compare with.")

        session.remove()

def process_new_posting(posting_id):
    with app.app_context():
        # Create a new session
        Session = scoped_session(sessionmaker(bind=db.engine))
        session = Session()

        # Fetch the new posting
        posting = session.query(Posting).get(posting_id)
        if not posting:
            print(f"Posting with ID {posting_id} not found.")
            session.remove()
            return

        # Fetch all resumes
        resumes = session.query(Resume).all()

        if resumes:
            preprocessed_posting = preprocess_text(posting.content)
            preprocessed_resumes = [preprocess_text(resume.content) for resume in resumes]

            documents = [preprocessed_posting] + preprocessed_resumes

            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

            posting_vector = tfidf_matrix[0]
            resume_vectors = tfidf_matrix[1:]

            similarity_scores = cosine_similarity(posting_vector, resume_vectors)[0]

            threshold = 0.5

            for idx, score in enumerate(similarity_scores):
                if score >= threshold:
                    matching_resume = resumes[idx]
                    print(f"Similarity between Posting ID {posting.id} and Resume ID {matching_resume.id}: {score:.2f}")

                    cold_email = generate_cold_email(matching_resume.content, posting.content)
                    print(f"\nGenerated Cold Email for Resume ID {matching_resume.id} and Posting ID {posting.id}:\n")
                    print(cold_email)

                    user_email_entries = matching_resume.user_emails
                    if not user_email_entries:
                        print(f"No user emails associated with Resume ID {matching_resume.id}")
                        continue

                    recruiter_email_entries = posting.recruiters
                    if not recruiter_email_entries:
                        print(f"No recruiter emails associated with Posting ID {posting.id}")
                        continue

                    for user_email_entry in user_email_entries:
                        sender_email = user_email_entry.email
                        user_name = sender_email.split('@')[0]
                        sender_password = SENDER_PASSWORD

                        for recruiter_email_entry in recruiter_email_entries:
                            recipient_email = recruiter_email_entry.email
                            send_email(sender_email, sender_password, recipient_email, cold_email, user_name)
                else:
                    print(f"Similarity between Posting ID {posting.id} and Resume ID {resumes[idx].id} is below threshold: {score:.2f}")
        else:
            print("No resumes to compare with.")

        session.remove()
