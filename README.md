# Resume & Job Posting Matching System

This project is a Flask-based application for managing resumes, job postings, and associated user and recruiter emails. It allows users to upload resumes and job postings, automatically match them based on content similarity, generate customized cold emails, and send these emails to recruiters on behalf of the user. The database is managed with SQLAlchemy, and text processing is handled using natural language processing (NLP) techniques.

## Features
1. **Resume & Posting Uploads**: Users can upload resumes and job postings through the web interface.
2. **Database Management**: Resumes, job postings, user emails, and recruiter emails are stored in a SQLite database.
3. **Automatic Matching**: Resumes and job postings are matched based on content similarity using TF-IDF and cosine similarity.
4. **Cold Email Generation**: OpenAI's GPT-4 is used to generate personalized cold emails.
5. **Email Sending**: Cold emails are sent to recruiters using the specified user’s email address.
6. **File Structure Management**: Unwanted files in the project directory can be removed with a safe cleanup script.

## File Descriptions

### 1. `app.py`
The main entry point for the Flask application. Defines routes for uploading resumes and postings. Registers event listeners for new database inserts.

### 2. `populate_database_app.py`
Script to populate the database by reading files from specific folders for resumes, job postings, recruiters, and user emails. Verifies associations between entries and prints summaries.

### 3. `rm_except.py`
A utility script that removes files and directories in the root project folder except for those specified in an exceptions list.

### 4. `factory.py`
Factory function to create and configure the Flask app, including database initialization.

### 5. `processing.py`
Processes and matches resumes to job postings using TF-IDF and cosine similarity. Generates cold emails using OpenAI and sends emails to recruiters associated with matched job postings.

### 6. `event_listeners.py`
Defines SQLAlchemy event listeners that trigger automatic processing when new resumes or postings are inserted into the database.

### 7. `gen_prompt.py`
Combines the contents of all Python files in the directory into a single output, facilitating easy sharing of the entire codebase.

### 8. `print_database_contents_app.py`
A debugging tool to print the contents of the database tables to the console, allowing verification of database entries.

### 9. `models.py`
Defines the SQLAlchemy models for `Resume`, `Posting`, `Recruiter`, and `UserEmail`, along with their relationships.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/resume-matching-app.git
   cd resume-matching-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - `OPENAI_API_KEY`: API key for OpenAI.
   - `SENDER_PASSWORD`: Password for the email account used to send cold emails.
   - Save these in a `.env` file or set them directly in the terminal.

4. **Initialize Database**:
   Run `populate_database_app.py` to create the database and populate it with data from the `resume`, `posting`, `recruiters`, and `user_emails` folders:
   ```bash
   python populate_database_app.py
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://localhost:5000`.

6. **Clean Up Project Directory**:
   Run `rm_except.py` to remove unnecessary files from the directory, preserving essential files only:
   ```bash
   python rm_except.py
   ```

## Usage

1. **Uploading Resumes and Postings**:
   - Access the app's interface to upload resumes and job postings.
   - Specify user and recruiter emails as comma-separated values in the upload form.

2. **Database Management**:
   - Use `print_database_contents_app.py` to print current database entries for verification:
     ```bash
     python print_database_contents_app.py
     ```

3. **File Processing**:
   - Trigger resume and posting processing automatically through event listeners when new entries are added to the database.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.

## Acknowledgements
- OpenAI for their API.
- NLTK and Scikit-Learn for text preprocessing and similarity calculations.

---

This readme should provide clear instructions and overview for using the resume matching system. Let me know if you need more customization!