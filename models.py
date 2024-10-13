# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)

class Posting(Base):
    __tablename__ = 'postings'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)
    recruiters = relationship('Recruiter', back_populates='posting', cascade='all, delete-orphan')

class Recruiter(Base):
    __tablename__ = 'recruiters'

    id = Column(Integer, primary_key=True)
    posting_id = Column(Integer, ForeignKey('postings.id'))
    email = Column(String)

    posting = relationship('Posting', back_populates='recruiters')
