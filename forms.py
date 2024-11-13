from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email is already registered.')

class VerificationForm(FlaskForm):
    code = StringField('Verification Code', validators=[DataRequired()])
    submit = SubmitField('Verify')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class InfoForm(FlaskForm):
    gmail_email = StringField('Gmail Email', validators=[DataRequired(), Email()])
    gmail_app_password = PasswordField('Gmail App Password', validators=[DataRequired()])
    resume = TextAreaField('Resume', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditInfoForm(FlaskForm):
    gmail_email = StringField('Gmail Email', validators=[DataRequired(), Email()])
    gmail_app_password = PasswordField('Gmail App Password', validators=[DataRequired()])
    resume = TextAreaField('Resume', validators=[DataRequired()])
    submit = SubmitField('Update')
