# Automated Cold Email Generator for Job Applications

## Introduction

This project is an automated system designed to help job seekers generate and send personalized cold emails to recruiters based on the content of their resumes and job postings. It utilizes Natural Language Processing (NLP) techniques to compute the similarity between resumes and job postings and leverages OpenAI's GPT-4 model to craft persuasive emails tailored to each opportunity.

## Features

- **Resume and Job Posting Management**: Store and manage multiple resumes and job postings in a SQLite database.
- **Similarity Computation**: Use TF-IDF vectorization and cosine similarity to match resumes with relevant job postings.
- **Email Generation**: Generate personalized cold emails using OpenAI's GPT-4 model.
- **Automated Email Sending**: Send generated emails to recruiters via SMTP.
- **Web Interface**: Interact with the system using a Flask web application.

## Prerequisites

- Python 3.x
- An OpenAI API key
- A Gmail account with an App Password (if using Gmail with two-factor authentication)
- Required Python packages (listed in `requirements.txt`)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
SENDER_EMAIL=your_email@example.com
SENDER_PASSWORD=your_email_password_or_app_password
```

- Replace `your_openai_api_key` with your actual OpenAI API key.
- Replace `your_email@example.com` with your email address.
- Replace `your_email_password_or_app_password` with your email password or app password.

**Note**: For security reasons, do not hardcode your API keys or passwords in the code. Use environment variables instead.

### 2. Configure SMTP Settings

If you are using an email service other than Gmail, update the SMTP server settings in the `send_email` function within the code:

```python
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    # ...
```

## Usage

### 1. Populate the Database

First, populate the SQLite database with resumes, job postings, recruiters, and user emails.

```bash
python populate_database.py
```

Alternatively, if you are using the Flask web application, you can upload resumes and job postings via the web interface.

### 2. Compute Similarity and Generate Emails

To compute the similarity between resumes and job postings, and generate cold emails for matching pairs:

```bash
python generate_and_send_emails.py
```

This script will:

- Fetch resumes and job postings from the database.
- Compute the similarity between each resume and job posting.
- For pairs exceeding the similarity threshold, generate a cold email using OpenAI's GPT-4 model.
- Send the generated emails to the associated recruiters.

### 3. View the Database Contents (Optional)

To print the contents of the database for verification:

```bash
python print_database_contents.py
```

### 4. Run the Web Application (Optional)

You can run the Flask web application to interact with the system via a web interface.

```bash
python app.py
```

Access the application by navigating to `http://localhost:5000` in your web browser.

## Directory Structure

```
├── app.py                         # Flask web application
├── app_combined.py                # Combined app with all functionalities
├── app_respond.py                 # App with additional response handling
├── gen_prompt.py                  # Script to generate prompt
├── generate_and_print_email.py    # Generate and print emails from the database
├── generate_and_send_emails.py    # Generate and send emails from the database
├── generate_and_send_emails_with_app_context.py
├── generate_cold_email.py         # Generate cold email based on resume and posting
├── models.py                      # Database models
├── populate_database.py           # Populate the database
├── populate_database_app.py       # Populate the database with app context
├── print_database_contents.py     # Print database contents
├── print_database_contents_app.py
├── requirements.txt               # Python dependencies
├── send_email.py                  # Script to send a test email
├── similarity_from_db.py          # Compute similarity from the database
├── similarity_from_db_app.py      # Compute similarity with app context
├── templates/
│   ├── index.html                 # Home page template
│   ├── upload_posting.html        # Template for uploading postings
│   └── upload_resume.html         # Template for uploading resumes
```

## Security Considerations

- **API Keys and Passwords**: Never commit your API keys or passwords to source control. Use environment variables or a configuration file that is excluded from version control (e.g., include it in your `.gitignore` file).
- **Email Sending Limitations**: Be aware of your email service provider's sending limits and policies to avoid being flagged for spam.
- **Data Privacy**: Ensure you have the right to use and store any resumes and job postings, and comply with all relevant data protection regulations.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## Acknowledgments

- **OpenAI GPT-4**: For powering the email generation.
- **Flask**: A lightweight WSGI web application framework.
- **NLTK**: Natural Language Toolkit for text processing.
- **scikit-learn**: For machine learning algorithms and tools.
- **SQLite**: A lightweight disk-based database.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.