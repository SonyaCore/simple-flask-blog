from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed
from flask_login import current_user

from wtforms import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired,Length , Email , EqualTo , ValidationError

from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),
                            Length(min=2,max=10)])
    email = StringField('Email',
                            validators=[DataRequired(),
                            Email()])
    password = PasswordField('Password',
                            validators=[DataRequired(),
                            Length(min=5,max=64)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),
                            EqualTo('password')])
    
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('ََThe username already exist!')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email already exist!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(),
                            Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),
                            Length(min=2,max=10)])
    email = StringField('Email',
                            validators=[DataRequired(),
                            Email()])

    picture = FileField('Update Porfile Picture',
                            validators=[FileAllowed(['jpg','png','jpeg'])])


    submitupdate = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('ََThe username already exist!')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email already exist!')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(),
                            EqualTo('password')])
    submit  = SubmitField('Request Password')