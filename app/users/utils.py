import secrets
import os
from PIL import Image

from flask import current_app
from flask_mail import Message 

from app.users.routes import url_for , mail
from app.config import PASSWORD_REGEX , USERNAME_REGEX

def password_regex(password):
    return PASSWORD_REGEX.match(password) is not None

def username_regex(username):
    return USERNAME_REGEX.match(username) is not None

def save_picture(form_picture):
    # Generate Hex Token for Profile Picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    from app.users.forms import UpdateAccountForm
    picture_fn = UpdateAccountForm().username.data + '_' + random_hex + f_ext

    # Join Picture
    picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)

    # Avatar Picure Resolution
    output_size = (125,125)

    # Final Picture Resolution
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)

    # Save Picture to File System
    picture.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password , click the following link:
{url_for('reset_token',token=token , _external=True)}

If you did not make this request then ignore this message
    '''
    mail.send(msg)

global allowed_user
allowed_user = ['Sonya','admin']

