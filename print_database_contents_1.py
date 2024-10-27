# print_database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import db, Resume, Posting, Recruiter, UserEmail


def main():
    # Create the database engine and session
    engine = create_engine('sqlite:///resumes_postings.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    print("\n--- Contents of the Database ---\n")

    # Print Resumes with Associated User Emails
    print("Resumes and Associated User Emails:")
    resumes = session.query(Resume).order_by(Resume.id).all()
    for resume in resumes:
        print(f"\nResume ID: {resume.id}, Filename: {resume.filename}")
        print(f"Content:\n{resume.content}\n")
        print("User Emails:")
        for user_email in resume.user_emails:
            print(f" - {user_email.email}")
    print("\n" + "-"*50)

    # Print Job Postings with Associated Recruiters
    print("\nJob Postings and Associated Recruiters:")
    postings = session.query(Posting).order_by(Posting.id).all()
    for posting in postings:
        print(f"\nJob Posting ID: {posting.id}, Filename: {posting.filename}")
        print(f"Content:\n{posting.content}\n")
        print("Recruiters:")
        for recruiter in posting.recruiters:
            print(f" - {recruiter.email}")
    print("\n" + "-"*50)

    # Optionally, print all User Emails
    print("\nAll User Emails:")
    user_emails = session.query(UserEmail).order_by(UserEmail.id).all()
    for user_email in user_emails:
        print(f"ID: {user_email.id}, Email: {user_email.email}, Associated Resume ID: {user_email.resume_id}")
    print("\n" + "-"*50)

    # Optionally, print all Recruiters
    print("\nAll Recruiters:")
    recruiters = session.query(Recruiter).order_by(Recruiter.id).all()
    for recruiter in recruiters:
        print(f"ID: {recruiter.id}, Email: {recruiter.email}, Associated Posting ID: {recruiter.posting_id}")
    print("\n" + "-"*50)

    session.close()

if __name__ == '__main__':
    main()
