# populate_database.py

import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Resume, Posting, Recruiter

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
    # Remove existing database file
    if os.path.exists('resumes_postings.db'):
        os.remove('resumes_postings.db')
        print("Existing database removed.")

    # Create the database and establish a session
    engine = create_engine('sqlite:///resumes_postings.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Paths to folders
    resume_folder = 'resume'
    posting_folder = 'posting'
    recruiters_folder = 'recruiters'

    # Insert resumes
    resumes, resume_filenames = read_files_from_folder(resume_folder)
    for filename, content in zip(resume_filenames, resumes):
        resume = Resume(filename=filename, content=content)
        session.add(resume)

    # Insert postings
    postings, posting_filenames = read_files_from_folder(posting_folder)
    postings_dict = {}  # To keep track of postings by posting number
    for filename, content in zip(posting_filenames, postings):
        posting = Posting(filename=filename, content=content)
        session.add(posting)

        # Extract posting number
        match = re.match(r'posting_(\d+)\.txt', filename)
        if match:
            posting_num = match.group(1)
            postings_dict[posting_num] = posting
        else:
            print(f"Warning: Could not extract posting number from filename {filename}")

    session.commit()

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
                        session.add(recruiter)
                else:
                    print(f"Warning: No posting found for recruiter file {recruiter_filename}")
            else:
                print(f"Warning: Could not extract posting number from recruiter file {recruiter_filename}")

    session.commit()
    session.close()

    print("Database 'resumes_postings.db' has been populated with resumes, job postings, and recruiters.")

if __name__ == '__main__':
    main()
