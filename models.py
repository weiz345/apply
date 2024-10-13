# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Resume(Base):
    """
    Represents a resume.
    """
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)

    # Relationship to user emails
    user_emails = relationship(
        'UserEmail',
        back_populates='resume',
        cascade='all, delete-orphan'
    )

class Posting(Base):
    """
    Represents a job posting.
    """
    __tablename__ = 'postings'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)

    # Relationship to recruiters
    recruiters = relationship(
        'Recruiter',
        back_populates='posting',
        cascade='all, delete-orphan'
    )

class Recruiter(Base):
    """
    Represents a recruiter associated with a job posting.
    """
    __tablename__ = 'recruiters'

    id = Column(Integer, primary_key=True)
    posting_id = Column(Integer, ForeignKey('postings.id'))
    email = Column(String)

    # Relationship back to the posting
    posting = relationship('Posting', back_populates='recruiters')

class UserEmail(Base):
    """
    Represents a user email associated with a resume.
    """
    __tablename__ = 'user_emails'

    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id'))
    email = Column(String)

    # Relationship back to the resume
    resume = relationship('Resume', back_populates='user_emails')
