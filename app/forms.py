from flask_wtf import FlaskForm
from flask_wtf.file import FileField , FileAllowed 
from flask_login import current_user
from wtforms import StringField , PasswordField , SubmitField , BooleanField , TextAreaField
from wtforms.validators import DataRequired,Length , Email , EqualTo , ValidationError
from app.models import User

global allowed_user
allowed_user = ['Sonya','admin']

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(),
                            Length(min=2,max=10)])
    email = StringField('Email',
                            validators=[DataRequired(),
                            Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
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


    submit = SubmitField('Update')

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

class ServerInfo(FlaskForm):
    github = StringField('GitHub',
                            validators=[DataRequired(),
                            Length(max=80)])
    telegram = StringField('Telegram',
                            validators=[DataRequired(),
                            Length(max=80)])
    instagram = StringField('Instagram',
                            validators=[DataRequired(),
                            Length(max=80)])
    twitter = StringField('Twitter',
                            validators=[DataRequired(),
                            Length(max=80)])
    description = StringField('Description',
                            validators=[DataRequired(),
                            Length(max=240)])
    submit = SubmitField('Update Server Information')


class PostForm(FlaskForm):
    title = StringField('Title',
                            validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit  = SubmitField('Post')
