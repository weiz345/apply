import os
from pathlib import Path

basedir = Path(__file__).resolve().parent  # Sets the base directory for the app
DATABASE = 'site.db'  # Define the database filename

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'
    url = os.getenv('DATABASE_URL', f'sqlite:///{Path(basedir).joinpath(DATABASE)}')
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'zhengweihang79@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'pnps vkxl pgvi djfx'
