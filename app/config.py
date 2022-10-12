# App Config
import os , re
class Config: 

    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Mail
    MAIL_SERVER = os.environ.get('SMTP')
    MAIL_PORT= os.environ.get('SMTP_PORT')
    MAIL_USERNAME = os.environ.get('EMAIL_USER') 
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_USE_TLS = True

# Constant Validation
VALID_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._'
PASSWORD_REGEX = re.compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{6,}\Z')
USERNAME_REGEX = re.compile(r'\A[\w\-\.]{3,}\Z')