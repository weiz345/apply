# app.py

from factory import create_app
from models import db, Resume, Posting, Recruiter, UserEmail
from flask import render_template, request, redirect, url_for

app = create_app()

# Import event listeners to register them
import event_listeners

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

        return redirect(url_for('index'))
    return render_template('upload_posting.html')

if __name__ == '__main__':
    app.run(debug=True)
