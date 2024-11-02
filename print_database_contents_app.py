# print_database_contents_app.py

from factory import create_app
from models import db, Resume, Posting, Recruiter, UserEmail

# Import event listeners to ensure they are registered
import event_listeners

def print_table_contents():
    app = create_app()
    with app.app_context():
        # Print all resumes
        resumes = Resume.query.all()
        print("Resumes:")
        for resume in resumes:
            print(f"ID: {resume.id}, Filename: {resume.filename}, Content: {resume.content}")

        # Print all postings
        postings = Posting.query.all()
        print("\nPostings:")
        for posting in postings:
            print(f"ID: {posting.id}, Filename: {posting.filename}, Content: {posting.content}")

        # Print all recruiters
        recruiters = Recruiter.query.all()
        print("\nRecruiters:")
        for recruiter in recruiters:
            print(f"ID: {recruiter.id}, Email: {recruiter.email}, Posting ID: {recruiter.posting_id}")

        # Print all user emails
        user_emails = UserEmail.query.all()
        print("\nUser Emails:")
        for user_email in user_emails:
            print(f"ID: {user_email.id}, Email: {user_email.email}, Resume ID: {user_email.resume_id}")

if __name__ == "__main__":
    print_table_contents()
