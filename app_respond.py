# app.py

from flask import Flask, render_template, request, redirect, url_for
from models import db, Resume, Posting, Recruiter, UserEmail
import os
import re
import openai
import numpy as np
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

app = Flask(__name__)

# Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resumes_postings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Set your OpenAI API key and email password as environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

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

def send_email(sender_email, sender_password, recipient_email, email_body, user_name):
    # Create the message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = "Application for the Position"

    # Add body to the message
    msg.attach(MIMEText(email_body, "plain"))

    try:
        # Connect to the server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent successfully from {user_name} to {recipient_email}!")
    except Exception as e:
        print(f"Error sending email from {user_name} to {recipient_email}: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        # Get data from form
        resume_filename = request.form.get('filename')
        resume_content = request.form.get('content')
        user_emails = request.form.get('user_emails')  # Should be a comma-separated string

        # Create Resume object
        resume = Resume(filename=resume_filename, content=resume_content)
        db.session.add(resume)
        db.session.commit()  # Commit to get the resume.id

        # Split user_emails by comma and create UserEmail objects
        if user_emails:
            emails = [email.strip() for email in user_emails.split(',') if email.strip()]
            for email in emails:
                user_email = UserEmail(email=email, resume_id=resume.id)
                db.session.add(user_email)
            db.session.commit()

        # Now proceed to compute similarity and send emails
        postings = Posting.query.all()

        if postings:
            preprocessed_resume = preprocess_text(resume.content)
            preprocessed_postings = [preprocess_text(posting.content) for posting in postings]

            # Combine documents for vectorization
            documents = [preprocessed_resume] + preprocessed_postings

            # Vectorize using TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

            # Separate the vectors
            resume_vector = tfidf_matrix[0]
            posting_vectors = tfidf_matrix[1:]

            # Compute cosine similarity
            similarity_scores = cosine_similarity(resume_vector, posting_vectors)[0]

            # Define threshold
            threshold = 0.5  # You can adjust this value

            # For each posting where similarity is above threshold
            for idx, score in enumerate(similarity_scores):
                if score >= threshold:
                    matching_posting = postings[idx]
                    print(f"Similarity between uploaded resume and Posting ID {matching_posting.id}: {score:.2f}")
                    # Generate cold email
                    cold_email = generate_cold_email(resume.content, matching_posting.content)
                    # Print the generated cold email
                    print(f"\nGenerated Cold Email for Resume ID {resume.id} and Posting ID {matching_posting.id}:\n")
                    print(cold_email)

                    # Get user emails associated with the resume
                    user_email_entries = resume.user_emails
                    if not user_email_entries:
                        print(f"No user emails associated with Resume ID {resume.id}")
                        continue

                    # Get recruiter emails associated with the posting
                    recruiter_email_entries = matching_posting.recruiters
                    if not recruiter_email_entries:
                        print(f"No recruiter emails associated with Posting ID {matching_posting.id}")
                        continue

                    for user_email_entry in user_email_entries:
                        sender_email = user_email_entry.email
                        user_name = sender_email.split('@')[0]  # Simple way to get user's name
                        sender_password = SENDER_PASSWORD  # Assuming same password for simplicity

                        for recruiter_email_entry in recruiter_email_entries:
                            recipient_email = recruiter_email_entry.email
                            # Send the email
                            send_email(sender_email, sender_password, recipient_email, cold_email, user_name)
                else:
                    print(f"Similarity with Posting ID {postings[idx].id} is below threshold: {score:.2f}")

        return redirect(url_for('index'))
    return render_template('upload_resume.html')

@app.route('/upload_posting', methods=['GET', 'POST'])
def upload_posting():
    if request.method == 'POST':
        # Get data from form
        posting_filename = request.form.get('filename')
        posting_content = request.form.get('content')
        recruiter_emails = request.form.get('recruiter_emails')  # Should be a comma-separated string

        # Create Posting object
        posting = Posting(filename=posting_filename, content=posting_content)
        db.session.add(posting)
        db.session.commit()  # Commit to get the posting.id

        # Split recruiter_emails by comma and create Recruiter objects
        if recruiter_emails:
            emails = [email.strip() for email in recruiter_emails.split(',') if email.strip()]
            for email in emails:
                recruiter = Recruiter(email=email, posting_id=posting.id)
                db.session.add(recruiter)
            db.session.commit()

        # Now proceed to compute similarity and send emails
        resumes = Resume.query.all()

        if resumes:
            preprocessed_posting = preprocess_text(posting.content)
            preprocessed_resumes = [preprocess_text(resume.content) for resume in resumes]

            # Combine documents for vectorization
            documents = [preprocessed_posting] + preprocessed_resumes

            # Vectorize using TF-IDF
            tfidf_vectorizer = TfidfVectorizer()
            tfidf_matrix = tfidf_vectorizer.fit_transform(documents)

            # Separate the vectors
            posting_vector = tfidf_matrix[0]
            resume_vectors = tfidf_matrix[1:]

            # Compute cosine similarity
            similarity_scores = cosine_similarity(posting_vector, resume_vectors)[0]

            # Define threshold
            threshold = 0.5  # You can adjust this value

            # For each resume where similarity is above threshold
            for idx, score in enumerate(similarity_scores):
                if score >= threshold:
                    matching_resume = resumes[idx]
                    print(f"Similarity between uploaded posting and Resume ID {matching_resume.id}: {score:.2f}")
                    # Generate cold email
                    cold_email = generate_cold_email(matching_resume.content, posting.content)
                    # Print the generated cold email
                    print(f"\nGenerated Cold Email for Resume ID {matching_resume.id} and Posting ID {posting.id}:\n")
                    print(cold_email)

                    # Get user emails associated with the resume
                    user_email_entries = matching_resume.user_emails
                    if not user_email_entries:
                        print(f"No user emails associated with Resume ID {matching_resume.id}")
                        continue

                    # Get recruiter emails associated with the posting
                    recruiter_email_entries = posting.recruiters
                    if not recruiter_email_entries:
                        print(f"No recruiter emails associated with Posting ID {posting.id}")
                        continue

                    for user_email_entry in user_email_entries:
                        sender_email = user_email_entry.email
                        user_name = sender_email.split('@')[0]  # Simple way to get user's name
                        sender_password = SENDER_PASSWORD  # Assuming same password for simplicity

                        for recruiter_email_entry in recruiter_email_entries:
                            recipient_email = recruiter_email_entry.email
                            # Send the email
                            send_email(sender_email, sender_password, recipient_email, cold_email, user_name)
                else:
                    print(f"Similarity with Resume ID {resumes[idx].id} is below threshold: {score:.2f}")

        return redirect(url_for('index'))
    return render_template('upload_posting.html')

if __name__ == '__main__':
    app.run(debug=True)
