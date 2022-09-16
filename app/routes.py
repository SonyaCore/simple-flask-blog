from flask import render_template , url_for, flash , redirect , request , abort
from app import app , db , bcrypt
from app.forms import RegistrationForm , LoginForm , UpdateAccountForm , PostForm
from app.models import User,Post
from flask_login import login_user , current_user , logout_user , login_required 
from PIL import Image

import secrets
import os

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
    posts = Post.query.all()
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

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                            content=form.content.data,
                            author = current_user)

        db.session.add(post)
        db.session.commit()
        flash('Post has been created', category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html',
                            title='New Post',
                            form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',
                            title = post.title ,
                            post = post , legend = 'New Post' )

@app.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('your post has been updated!', category='success')
        return redirect(url_for('post',post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                            title='Update Post',
                            form=form , legend = 'Update Post')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('your post has been deleted!', category='success')
    return redirect(url_for('home'))