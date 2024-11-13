from app import app
from extensions import db
from models import User

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f'ID: {user.id}')
        print(f'Email: {user.email}')
        print(f'Password Hash: {user.password_hash}')
        print(f'Verified: {user.is_verified}')
        print(f'Gmail Email: {user.gmail_email}')
        print(f'Gmail App Password: {user.gmail_app_password}')
        print(f'Resume: {user.resume}')
        print('-' * 40)
