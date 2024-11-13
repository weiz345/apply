from extensions import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    gmail_email = db.Column(db.String(150))
    gmail_app_password = db.Column(db.String(150))
    resume = db.Column(db.Text)
    verification_code = db.Column(db.String(6))

    def __repr__(self):
        return f"User('{self.email}', verified={self.is_verified})"
