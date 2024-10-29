# Automated Cold Email Sender for Job Applications

This project automates the process of matching resumes to job postings, calculating their similarity, generating personalized cold emails using OpenAI's GPT models, and sending these emails to recruiters or hiring managers. The application also provides a Flask web interface to upload resumes and job postings.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Requirements](#requirements)
- [License](#license)

## Overview

The main goal of this project is to streamline the job application process by automating:

- Matching resumes to relevant job postings based on content similarity.
- Generating personalized cold emails tailored to each job posting and resume.
- Sending these emails to the appropriate recruiters or hiring managers.

## Features

- **Resume and Job Posting Management**: Upload and store resumes and job postings in a database.
- **Content Similarity Calculation**: Use TF-IDF vectorization and cosine similarity to match resumes with job postings.
- **Automated Email Generation**: Generate personalized cold emails using OpenAI's GPT models.
- **Email Sending**: Send generated emails to recruiters using SMTP.
- **Flask Web Interface**: User-friendly interface to upload resumes and job postings.

## Prerequisites

- Python 3.x
- An OpenAI API key
- Gmail account with App Passwords enabled (if using Gmail SMTP)
- SQLite (for the database)

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, you can install the packages individually:

   ```bash
   pip install openai flask flask_sqlalchemy SQLAlchemy pandas numpy scikit-learn nltk pyperclip
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory and add the following:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   SENDER_EMAIL=your_email@example.com
   SENDER_PASSWORD=your_email_password_or_app_password
   ```

   Replace `your_openai_api_key`, `your_email@example.com`, and `your_email_password_or_app_password` with your actual credentials.

   **Note**: If you're using Gmail and have 2FA enabled, you'll need to generate an App Password.

5. **Initialize the database**

   Run the following script to populate the database with initial data:

   ```bash
   python populate_database.py
   ```

## Usage

### Running the Flask App

Start the Flask application:

```bash
python app.py
```

The app will be available at `http://localhost:5000/`.

### Uploading Resumes and Job Postings

- Navigate to `/upload_resume` to upload a resume.
- Navigate to `/upload_posting` to upload a job posting.

### Viewing Database Contents

To print the contents of the database for verification:

```bash
python print_database_contents.py
```

### Calculating Similarity

To calculate the similarity between resumes and job postings:

```bash
python similarity_from_db.py
```

## Project Structure

```
├── app.py
├── app_combined.py
├── generate_cold_email.py
├── gen_prompt.py
├── models.py
├── populate_database.py
├── populate_database_app.py
├── print_database_contents.py
├── print_database_contents_app.py
├── send_email.py
├── similarity_from_db.py
├── similarity_from_db_app.py
├── templates/
│   ├── index.html
│   ├── upload_posting.html
│   └── upload_resume.html
├── static/
├── resume/
│   └── resume_1.txt
├── posting/
│   └── posting_1.txt
├── recruiters/
│   └── recruiters_posting1.txt
├── user_emails/
│   └── user_emails_resume1.txt
└── requirements.txt
```

## File Descriptions

### `app.py`

The main Flask application that provides routes for:

- Index page (`/`)
- Uploading resumes (`/upload_resume`)
- Uploading job postings (`/upload_posting`)

It integrates functionalities like content similarity calculation, email generation using OpenAI's GPT models, and email sending.

### `models.py`

Defines the SQLAlchemy models:

- `Resume`
- `Posting`
- `Recruiter`
- `UserEmail`

These models represent the database tables and their relationships.

### `generate_cold_email.py`

Contains the function `generate_cold_email` that uses OpenAI's GPT models to generate a personalized cold email based on a resume and a job posting.

### `populate_database.py`

Populates the SQLite database with resumes, job postings, recruiters, and user emails from the respective folders (`resume/`, `posting/`, `recruiters/`, `user_emails/`).

### `print_database_contents.py`

Prints the contents of the database tables for verification purposes. Useful for debugging and ensuring data integrity.

### `similarity_from_db.py`

Calculates the similarity between resumes and job postings using TF-IDF vectorization and cosine similarity. Outputs a similarity matrix.

### `send_email.py`

Contains functionality to send emails using SMTP. It constructs an email and sends it to the specified recipient.

### `app_combined.py`

An integrated version of the Flask app that combines multiple functionalities, including email generation and sending directly from the app.

### `gen_prompt.py`

A utility script that combines all Python files in the directory into a single string and copies it to the clipboard. Useful for generating prompts or aggregating code.

### `populate_database_app.py`

An alternative script to `populate_database.py` that uses Flask's application context to interact with the database.

### `print_database_contents_app.py`

Similar to `print_database_contents.py` but uses the Flask application context.

### `similarity_from_db_app.py`

Calculates content similarity using the Flask application's context.

### `templates/`

Contains the HTML templates used by the Flask application.

- `index.html`: The homepage.
- `upload_resume.html`: Form to upload a resume.
- `upload_posting.html`: Form to upload a job posting.

### `static/`

Contains static files like CSS, JavaScript, images, etc.

### `resume/`

Folder containing resume text files.

### `posting/`

Folder containing job posting text files.

### `recruiters/`

Folder containing text files with recruiter emails associated with job postings.

### `user_emails/`

Folder containing text files with user emails associated with resumes.

### `requirements.txt`

Contains all the Python packages required for the project.

## Requirements

The `requirements.txt` file includes the following packages:

```
openai
flask
flask_sqlalchemy
SQLAlchemy
pandas
numpy
scikit-learn
nltk
pyperclip
```

Ensure these packages are installed to run the project successfully.

## License

This project is licensed under the MIT License.

---

Feel free to contribute to this project by opening issues or submitting pull requests.