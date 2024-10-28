# populate_database_with_app_context.py

import os
import re
from flask import current_app
from app import app, db, Resume, Posting, Recruiter, UserEmail

def read_files_from_folder(folder_path):
    documents = []
    filenames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                documents.append(content)
                filenames.append(filename)
    return documents, filenames

def main():
    with app.app_context():
        # Remove existing database file
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Existing database removed.")

        # Create the database
        db.create_all()

        # Paths to folders
        resume_folder = 'resume'
        posting_folder = 'posting'
        recruiters_folder = 'recruiters'
        user_emails_folder = 'user_emails'

        # Insert resumes
        resumes, resume_filenames = read_files_from_folder(resume_folder)
        resumes_dict = {}  # To keep track of resumes by resume number
        for filename, content in zip(resume_filenames, resumes):
            resume = Resume(filename=filename, content=content)
            db.session.add(resume)

            # Extract resume number
            match = re.match(r'resume_(\d+)\.txt', filename)
            if match:
                resume_num = match.group(1)
                resumes_dict[resume_num] = resume
            else:
                print(f"Warning: Could not extract resume number from filename {filename}")

        # Insert postings
        postings, posting_filenames = read_files_from_folder(posting_folder)
        postings_dict = {}  # To keep track of postings by posting number
        for filename, content in zip(posting_filenames, postings):
            posting = Posting(filename=filename, content=content)
            db.session.add(posting)

            # Extract posting number
            match = re.match(r'posting_(\d+)\.txt', filename)
            if match:
                posting_num = match.group(1)
                postings_dict[posting_num] = posting
            else:
                print(f"Warning: Could not extract posting number from filename {filename}")

        db.session.commit()

        # Insert recruiters
        recruiter_files = sorted(os.listdir(recruiters_folder))
        for recruiter_filename in recruiter_files:
            if recruiter_filename.endswith('.txt'):
                file_path = os.path.join(recruiters_folder, recruiter_filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    emails = [line.strip() for line in file]

                # Extract posting number from recruiter filename
                match = re.match(r'recruiters_posting(\d+)\.txt', recruiter_filename)
                if match:
                    posting_num = match.group(1)
                    posting = postings_dict.get(posting_num)
                    if posting:
                        for email in emails:
                            recruiter = Recruiter(email=email, posting=posting)
                            db.session.add(recruiter)
                    else:
                        print(f"Warning: No posting found for recruiter file {recruiter_filename}")
                else:
                    print(f"Warning: Could not extract posting number from recruiter file {recruiter_filename}")

        # Insert user emails
        user_email_files = sorted(os.listdir(user_emails_folder))
        for user_email_filename in user_email_files:
            if user_email_filename.endswith('.txt'):
                file_path = os.path.join(user_emails_folder, user_email_filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    emails = [line.strip() for line in file]

                # Extract resume number from user email filename
                match = re.match(r'user_emails_resume(\d+)\.txt', user_email_filename)
                if match:
                    resume_num = match.group(1)
                    resume = resumes_dict.get(resume_num)
                    if resume:
                        for email in emails:
                            user_email = UserEmail(email=email, resume=resume)
                            db.session.add(user_email)
                    else:
                        print(f"Warning: No resume found for user email file {user_email_filename}")
                else:
                    print(f"Warning: Could not extract resume number from user email file {user_email_filename}")

        db.session.commit()

        # Verification: Print out the associations
        print("\n--- Associations for Verification ---\n")

        # Print resumes with their user emails
        print("Resumes and Associated User Emails:")
        for resume in Resume.query.order_by(Resume.id).all():
            print(f"\nResume ID: {resume.id}, Filename: {resume.filename}")
            print("User Emails:")
            for user_email in resume.user_emails:
                print(f" - {user_email.email}")

        # Print postings with their recruiters
        print("\nPostings and Associated Recruiters:")
        for posting in Posting.query.order_by(Posting.id).all():
            print(f"\nJob Posting ID: {posting.id}, Filename: {posting.filename}")
            print("Recruiters:")
            for recruiter in posting.recruiters:
                print(f" - {recruiter.email}")

        print("\nDatabase 'resumes_postings.db' has been populated with resumes, job postings, recruiters, and user emails.")

if __name__ == '__main__':
    main()
