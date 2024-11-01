# README: Resume and Job Posting Matching with Automated Email Generation

This project automates resume and job posting matching using cosine similarity on text embeddings and generates personalized cold emails for recruiters. The application includes a Flask web interface for users to upload resumes and job postings, which are stored in an SQLite database. Upon finding high similarity between a resume and a job posting, the app generates and sends a cold email to the recruiter on behalf of the user.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [Usage](#usage)
5. [Database](#database)
6. [Detailed File Explanations](#detailed-file-explanations)
7. [Acknowledgements](#acknowledgements)

---

## Project Structure

The project is organized as follows:

- `app.py`: The main Flask app that handles routes for resume and posting uploads, similarity calculation, email generation, and sending.
- `models.py`: Defines the database models for `Resume`, `Posting`, `UserEmail`, and `Recruiter`.
- `generate_and_send_emails_with_app_context.py`: Matches resumes to job postings based on similarity and sends emails within the Flask app context.
- `populate_database.py`: Populates the database with resume and job posting data from text files.
- `similarity_from_db.py`: Computes the similarity matrix between all resumes and job postings in the database.
- `send_email.py`: Standalone script for sending emails.
- `generate_cold_email.py`: Generates personalized cold emails based on resume and job posting content.
- `rm_except.py`: Utility script to delete unnecessary files, retaining essential files as specified.
- `print_database_contents_app.py`: Prints all data stored in the database for verification.
- `gen_prompt.py`: Utility to combine all Python files for easy sharing or logging.
- `requirements.txt`: Lists all required Python libraries.

## Installation

### Prerequisites
- Python 3.x
- `pip` package manager

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Download NLTK stopwords:
   ```python
   import nltk
   nltk.download('stopwords')
   ```

## Environment Variables

Set the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key for generating emails.
- `SENDER_EMAIL`: The email address that will send emails on behalf of users.
- `SENDER_PASSWORD`: The email account password (use an app password if 2FA is enabled).

Example:
```bash
export OPENAI_API_KEY='your_openai_api_key'
export SENDER_EMAIL='your_email@example.com'
export SENDER_PASSWORD='your_email_password'
```

## Usage

### Running the Application

1. Start the Flask app:
   ```bash
   python app.py
   ```

2. Access the web interface at `http://127.0.0.1:5000/`:
   - **Upload Resume**: Upload resume text and specify associated emails.
   - **Upload Posting**: Upload job posting text and specify recruiter emails.

### Email Generation and Sending

- After uploading, the app calculates similarity between resumes and job postings.
- If similarity exceeds the threshold, a cold email is generated and sent to the recruiters associated with the matched job posting.

## Database

The project uses SQLite (`resumes_postings.db`) for simplicity, managed via SQLAlchemy. Each resume or job posting is associated with one or more user emails or recruiter emails, respectively.

To view all entries:
```bash
python print_database_contents_app.py
```

## Detailed File Explanations

- **`generate_and_send_emails_with_app_context.py`**: Automates matching resumes and job postings and sends emails if similarity exceeds the threshold.
- **`populate_database.py`**: Reads resumes and postings from text files and populates the database.
- **`similarity_from_db.py`**: Calculates and displays a similarity matrix between resumes and job postings.
- **`send_email.py`**: Simple script to send a test email.
- **`generate_cold_email.py`**: Uses OpenAI to create personalized cold emails.
- **`rm_except.py`**: Utility to delete files not on the exceptions list.
- **`gen_prompt.py`**: Utility to combine Python files into one, useful for sharing or generating comprehensive code snippets.
  
## Acknowledgements

This project was inspired by the need for efficient and automated job application processes using modern NLP and ML tools. The `TfidfVectorizer` and `cosine_similarity` functions from `sklearn` enable high-quality resume and job posting matching, while OpenAI's API aids in generating professionally styled emails.