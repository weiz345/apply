from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message  # Add this import
from forms import RegistrationForm, VerificationForm, LoginForm, InfoForm, EditInfoForm
from config import Config
from extensions import db, mail, login_manager
from models import User
import random
import string


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if not email.endswith('@mail.utoronto.ca'):
            flash('You must use a @mail.utoronto.ca email.', 'danger')
            return render_template('register.html', form=form)
        code = generate_verification_code()
        user = User(email=email, verification_code=code)
        db.session.add(user)
        db.session.commit()
        # Send verification email
        msg = Message('Your Verification Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = f'Your verification code is {code}'
        mail.send(msg)
        flash('A verification code has been sent to your email.', 'info')
        return redirect(url_for('verify', email=email))
    return render_template('register.html', form=form)

@app.route('/verify/<email>', methods=['GET', 'POST'])
def verify(email):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    user = User.query.filter_by(email=email).first_or_404()
    form = VerificationForm()
    if form.validate_on_submit():
        if form.code.data == user.verification_code:
            user.is_verified = True
            user.verification_code = None
            db.session.commit()
            flash('Your email has been verified. You can now log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid verification code.', 'danger')
    return render_template('verify.html', form=form, email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.is_verified:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and verify your account.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.gmail_email:
        form = InfoForm()
        if form.validate_on_submit():
            current_user.gmail_email = form.gmail_email.data
            current_user.gmail_app_password = form.gmail_app_password.data
            current_user.resume = form.resume.data
            db.session.commit()
            flash('Your information has been saved.', 'success')
            return redirect(url_for('dashboard'))
        return render_template('dashboard.html', form=form)
    else:
        return render_template('dashboard.html')

@app.route('/edit_info', methods=['GET', 'POST'])
@login_required
def edit_info():
    form = EditInfoForm()
    if request.method == 'GET':
        form.gmail_email.data = current_user.gmail_email
        form.gmail_app_password.data = current_user.gmail_app_password
        form.resume.data = current_user.resume
    if form.validate_on_submit():
        current_user.gmail_email = form.gmail_email.data
        current_user.gmail_app_password = form.gmail_app_password.data
        current_user.resume = form.resume.data
        db.session.commit()
        flash('Your information has been updated.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_info.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
