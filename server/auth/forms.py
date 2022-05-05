from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import Email, DataRequired

# login and Sign Up


class LoginForm(FlaskForm):
    email = EmailField('Username',
                         id='email_login',
                         validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")

    #password2 = PasswordField('Re-Type Password', validators=[DataRequired()])


class SignUpForm(FlaskForm):
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = EmailField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
