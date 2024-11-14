from app import app
from extensions import db
from models import User  # Import all your models here

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database tables created successfully.")
