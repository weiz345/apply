import os

# Directory structure
dirs = [
    "templates",
]

# File contents
files = {
    "requirements.txt": """Flask\nFlask-WTF\nFlask-Mail\nFlask-Login\nFlask-SQLAlchemy\nemail-validator\n""",

    "config.py": """import os\n\nclass Config:\n    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key_here'\n    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'\n    SQLALCHEMY_TRACK_MODIFICATIONS = False\n    MAIL_SERVER = 'smtp.gmail.com'\n    MAIL_PORT = 587\n    MAIL_USE_TLS = True\n    MAIL_USERNAME = 'your_email@gmail.com'\n    MAIL_PASSWORD = 'your_email_app_password'\n""",

    "extensions.py": """from flask_sqlalchemy import SQLAlchemy\nfrom flask_mail import Mail\nfrom flask_login import LoginManager\n\ndb = SQLAlchemy()\nmail = Mail()\nlogin_manager = LoginManager()\n""",

    "models.py": """from extensions import db, login_manager\nfrom flask_login import UserMixin\n\n@login_manager.user_loader\ndef load_user(user_id):\n    return User.query.get(int(user_id))\n\nclass User(db.Model, UserMixin):\n    id = db.Column(db.Integer, primary_key=True)\n    email = db.Column(db.String(150), unique=True, nullable=False)\n    is_verified = db.Column(db.Boolean, default=False)\n    gmail_email = db.Column(db.String(150))\n    gmail_app_password = db.Column(db.String(150))\n    resume = db.Column(db.Text)\n    verification_code = db.Column(db.String(6))\n\n    def __repr__(self):\n        return f\"User('{self.email}', verified={self.is_verified})\"\n""",

    "forms.py": """from flask_wtf import FlaskForm\nfrom wtforms import StringField, PasswordField, SubmitField, TextAreaField\nfrom wtforms.validators import DataRequired, Email, ValidationError\nfrom models import User\n\nclass RegistrationForm(FlaskForm):\n    email = StringField('Email', validators=[DataRequired(), Email()])\n    submit = SubmitField('Register')\n\n    def validate_email(self, email):\n        user = User.query.filter_by(email=email.data.lower()).first()\n        if user:\n            raise ValidationError('Email is already registered.')\n\nclass VerificationForm(FlaskForm):\n    code = StringField('Verification Code', validators=[DataRequired()])\n    submit = SubmitField('Verify')\n\nclass LoginForm(FlaskForm):\n    email = StringField('Email', validators=[DataRequired(), Email()])\n    submit = SubmitField('Login')\n\nclass InfoForm(FlaskForm):\n    gmail_email = StringField('Gmail Email', validators=[DataRequired(), Email()])\n    gmail_app_password = PasswordField('Gmail App Password', validators=[DataRequired()])\n    resume = TextAreaField('Resume', validators=[DataRequired()])\n    submit = SubmitField('Submit')\n\nclass EditInfoForm(FlaskForm):\n    gmail_email = StringField('Gmail Email', validators=[DataRequired(), Email()])\n    gmail_app_password = PasswordField('Gmail App Password', validators=[DataRequired()])\n    resume = TextAreaField('Resume', validators=[DataRequired()])\n    submit = SubmitField('Update')\n""",

    "app.py": """from flask import Flask, render_template, url_for, redirect, flash, request\nfrom flask_login import login_user, current_user, logout_user, login_required\nfrom forms import RegistrationForm, VerificationForm, LoginForm, InfoForm, EditInfoForm\nfrom config import Config\nfrom extensions import db, mail, login_manager\nfrom models import User\nimport random\nimport string\n\napp = Flask(__name__)\napp.config.from_object(Config)\n\ndb.init_app(app)\nmail.init_app(app)\nlogin_manager.init_app(app)\nlogin_manager.login_view = 'login'\n\ndef generate_verification_code():\n    return ''.join(random.choices(string.digits, k=6))\n\n@app.route('/register', methods=['GET', 'POST'])\ndef register():\n    if current_user.is_authenticated:\n        return redirect(url_for('dashboard'))\n    form = RegistrationForm()\n    if form.validate_on_submit():\n        email = form.email.data.lower()\n        if not email.endswith('@mail.utoronto.ca'):\n            flash('You must use a @mail.utoronto.ca email.', 'danger')\n            return render_template('register.html', form=form)\n        code = generate_verification_code()\n        user = User(email=email, verification_code=code)\n        db.session.add(user)\n        db.session.commit()\n        # Send verification email\n        msg = Message('Your Verification Code', sender=app.config['MAIL_USERNAME'], recipients=[email])\n        msg.body = f'Your verification code is {code}'\n        mail.send(msg)\n        flash('A verification code has been sent to your email.', 'info')\n        return redirect(url_for('verify', email=email))\n    return render_template('register.html', form=form)\n\n@app.route('/verify/<email>', methods=['GET', 'POST'])\ndef verify(email):\n    if current_user.is_authenticated:\n        return redirect(url_for('dashboard'))\n    user = User.query.filter_by(email=email).first_or_404()\n    form = VerificationForm()\n    if form.validate_on_submit():\n        if form.code.data == user.verification_code:\n            user.is_verified = True\n            user.verification_code = None\n            db.session.commit()\n            flash('Your email has been verified. You can now log in.', 'success')\n            return redirect(url_for('login'))\n        else:\n            flash('Invalid verification code.', 'danger')\n    return render_template('verify.html', form=form, email=email)\n\n# ... more routes as above\n\nif __name__ == '__main__':\n    app.run(debug=True)\n""",

    "templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask App</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
</head>
<body>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        <div class="container mt-4">
          {% for category, message in messages %}
            <div class="alert alert-{{ category }}">{{ message }}</div>
          {% endfor %}
        </div>
      {% endif %}
    {% endwith %}

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <a class="navbar-brand" href="{{ url_for('dashboard') }}">FlaskApp</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ml-auto">
          {% if current_user.is_authenticated %}
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('edit_info') }}">Edit Info</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
            </li>
          {% else %}
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('register') }}">Register</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{ url_for('login') }}">Login</a>
            </li>
          {% endif %}
        </ul>
      </div>
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
""",

    "templates/register.html": """{% extends "base.html" %}
{% block content %}
    <h2>Register</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.email.label(class="form-control-label") }}
            {{ form.email(class="form-control") }}
            {% for error in form.email.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        {{ form.submit(class="btn btn-primary") }}
    </form>
{% endblock %}
""",

    "templates/verify.html": """{% extends "base.html" %}
{% block content %}
    <h2>Verify Email</h2>
    <p>A verification code has been sent to {{ email }}. Please enter it below.</p>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.code.label(class="form-control-label") }}
            {{ form.code(class="form-control") }}
            {% for error in form.code.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        {{ form.submit(class="btn btn-primary") }}
    </form>
{% endblock %}
""",

    "templates/login.html": """{% extends "base.html" %}
{% block content %}
    <h2>Login</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.email.label(class="form-control-label") }}
            {{ form.email(class="form-control") }}
            {% for error in form.email.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        {{ form.submit(class="btn btn-primary") }}
    </form>
{% endblock %}
""",

    "templates/dashboard.html": """{% extends "base.html" %}
{% block content %}
    <h2>Dashboard</h2>
    {% if not current_user.gmail_email %}
        <p>Please provide your Gmail email, app password, and resume.</p>
        <form method="POST" action="">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.gmail_email.label(class="form-control-label") }}
                {{ form.gmail_email(class="form-control") }}
                {% for error in form.gmail_email.errors %}
                    <span style="color: red;">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.gmail_app_password.label(class="form-control-label") }}
                {{ form.gmail_app_password(class="form-control") }}
                {% for error in form.gmail_app_password.errors %}
                    <span style="color: red;">[{{ error }}]</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.resume.label(class="form-control-label") }}
                {{ form.resume(class="form-control") }}
                {% for error in form.resume.errors %}
                    <span style="color: red;">[{{ error }}]</span>
                {% endfor %}
            </div>
            {{ form.submit(class="btn btn-primary") }}
        </form>
    {% else %}
        <p>Your information:</p>
        <ul>
            <li>Gmail Email: {{ current_user.gmail_email }}</li>
            <li>Resume:</li>
            <p>{{ current_user.resume }}</p>
        </ul>
    {% endif %}
{% endblock %}
""",

    "templates/edit_info.html": """{% extends "base.html" %}
{% block content %}
    <h2>Edit Your Information</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.gmail_email.label(class="form-control-label") }}
            {{ form.gmail_email(class="form-control") }}
            {% for error in form.gmail_email.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        <div class="form-group">
            {{ form.gmail_app_password.label(class="form-control-label") }}
            {{ form.gmail_app_password(class="form-control") }}
            {% for error in form.gmail_app_password.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        <div class="form-group">
            {{ form.resume.label(class="form-control-label") }}
            {{ form.resume(class="form-control") }}
            {% for error in form.resume.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        {{ form.submit(class="btn btn-primary") }}
    </form>
{% endblock %}
""",
}

# Create directories
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

# Create files
for filename, content in files.items():
    with open(filename, "w") as file:
        file.write(content)

print("Project files created.")
