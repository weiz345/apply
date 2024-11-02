# models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    content = db.Column(db.Text)
    user_emails = db.relationship(
        'UserEmail',
        back_populates='resume',
        cascade='all, delete-orphan'
    )

class Posting(db.Model):
    __tablename__ = 'postings'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String)
    content = db.Column(db.Text)
    recruiters = db.relationship(
        'Recruiter',
        back_populates='posting',
        cascade='all, delete-orphan'
    )

class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    id = db.Column(db.Integer, primary_key=True)
    posting_id = db.Column(db.Integer, db.ForeignKey('postings.id'))
    email = db.Column(db.String)
    posting = db.relationship('Posting', back_populates='recruiters')

class UserEmail(db.Model):
    __tablename__ = 'user_emails'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    email = db.Column(db.String)
    resume = db.relationship('Resume', back_populates='user_emails')
