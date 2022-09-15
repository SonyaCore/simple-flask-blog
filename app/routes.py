from flask import render_template , url_for, flash , redirect , request
from app import app , db , bcrypt
from app.forms import RegistrationForm , LoginForm , UpdateAccountForm
from app.models import User,Post
from flask_login import login_user , current_user , logout_user , login_required
from PIL import Image

import secrets
import os


posts = [
    {
        'author': 'sonya',
        'date_posted': '2022-04-20',
        'title': 'flask-api',
        'content': '''Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools.'''
    },
]

# Additional Navbar Information
@app.context_processor
def layout():
    url = {
        'github':      'https://github.com/SoniaCore',
        'telegram':    'https://telegram.me/ReiLibre',
        'info':        'Still in Development @SoniaCore',
    }
    return dict(url=url)

# Blog Name
@app.context_processor
def name():
    info = {
        'servername':   'Sonia Blog'
    }
    return dict(info=info)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',
    posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash password

        # Add User
        user = User(username=form.username.data,
        email=form.email.data,
        password=hashed_password)

        # Commit to DB
        db.session.add(user)
        db.session.commit()

        flash(f'{form.username.data} has been created !',
        category='success')

        return redirect(url_for('login'))
    return render_template('register.html',
    title='Register',
    form = form)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You Have been logged in!', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed Check your information!', category='danger')
    return render_template('login.html',
    title='Login',
    form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    # Generate Hex Token for Profile Picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = UpdateAccountForm().username.data + '_' + random_hex + f_ext

    # Join Picture
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)

    # Avatar Picure Resolution
    output_size = (125,125)

    # Final Picture Resolution
    picture = Image.open(form_picture)
    picture.thumbnail(output_size)

    # Save Picture to File System
    picture.save(picture_path)

    return picture_fn


@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            old_pic = current_user.image_file
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            if old_pic != 'default.jpg':
                os.remove(os.path.join(app.root_path, 'static/profile', old_pic))
    
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account has been updated!' , category='success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    imagefile = url_for('static', filename =f"profile/{current_user.image_file}")
    return render_template('account.html',
    title = 'My Profile',
    profile = imagefile ,
    form = form)