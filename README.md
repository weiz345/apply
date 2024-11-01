# README: Automated Resume and Job Posting Matching System

This project automates matching between resumes and job postings by calculating cosine similarity on text embeddings and generating cold emails for recruiters when a match is found. Users can upload resumes and job postings through a Flask web interface, where they are stored in an SQLite database. The app then identifies strong matches, generates a cold email for the user, and sends it to the relevant recruiter.

---

## Project Structure

### Key Files

- **`app_respond.py`**: Main Flask application file. Handles resume and job posting uploads, similarity calculation, email generation, and email sending.
- **`populate_database_app.py`**: Populates the database with resumes, job postings, recruiters, and user email data. Pulls text files from designated folders, processes them, and inserts them into the database.
- **`rm_except.py`**: Utility script to delete all files in the project directory except those on a specified exceptions list.
- **`gen_prompt.py`**: Combines all `.py` files into a single string and copies it to the clipboard for easy sharing.
- **`print_database_contents_app.py`**: Prints all contents of the database for verification, displaying resumes, postings, recruiters, and user emails.
- **`models.py`**: Defines SQLAlchemy models for `Resume`, `Posting`, `UserEmail`, and `Recruiter`, which manage the database tables and relationships.

---

## Installation

### Prerequisites
- **Python 3.x**
- **pip** package manager

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK Data**:
   ```python
   import nltk
   nltk.download('stopwords')
   ```

4. **Set Environment Variables**:
   Set your `OpenAI` API key, sender email, and email password as environment variables.

   ```bash
   export OPENAI_API_KEY='your_openai_api_key'
   export SENDER_EMAIL='your_email@example.com'
   export SENDER_PASSWORD='your_email_password'
   ```

---

## Usage

### Running the Application

1. **Start the Flask App**:
   ```bash
   python app_respond.py
   ```
2. **Access the Interface**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.

   - **Upload Resume**: Enter resume text and associated user emails.
   - **Upload Posting**: Enter job posting text and associated recruiter emails.

### Database Population

1. To populate the database with sample data, run:
   ```bash
   python populate_database_app.py
   ```

2. **Verify Data**:
   To view all entries, run:
   ```bash
   python print_database_contents_app.py
   ```

### Automated Email Generation

Upon upload, resumes and job postings are matched based on text similarity. If a match exceeds the similarity threshold, a cold email is generated using OpenAI and sent to the recruiter via SMTP.

---

## Database Structure

- **Resume**: Stores each resume and its associated user emails.
- **Posting**: Stores each job posting and its associated recruiter emails.
- **UserEmail**: Links user emails to resumes.
- **Recruiter**: Links recruiter emails to job postings.

---

## Acknowledgments

This project leverages the **NLTK** library for text processing and **OpenAI's GPT API** to generate professional cold emails. The **TF-IDF Vectorizer** and **cosine similarity** functions from **sklearn** are used for matching resumes to job postings.