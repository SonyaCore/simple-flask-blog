from flask import render_template , url_for, flash , redirect , request , abort
from app import app , db , bcrypt , mail
from app.forms import RegistrationForm , LoginForm , UpdateAccountForm , PostForm
from app.forms import ResetPasswordForm , RequestResetForm
from app.forms import ServerInfo , allowed_user
from app.models import User,Post , ServerName , NavBar
from flask_login import login_user , current_user , logout_user , login_required
from flask_mail import Message 
from PIL import Image
import secrets
import os

# Blog Name
def servername():
    name = db.session.query(ServerName).all()
    for query in name: 
        return query.servername

# Additional Navbar Information
nav = db.session.query(NavBar).all()

# Information
# def information():
#     global github
#     for data in nav:
#         tableinfo = [f'{data.github}',f'{data.telegram}',f'{data.instagram}',f'{data.twitter}',f'{data.description}']
#         github = {data.github}
#     return tableinfo , github

@app.context_processor
def name():
    info = {
         'servername':   f'{servername()}'
     }
    return dict(info=info)

# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s\n', request.headers)
#     app.logger.debug('Body: %s\n', request.get_data())

@app.route('/')
@app.route('/home')
def home():
    # Load Posts 
    page = request.args.get ('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page , per_page = 5)

    return render_template('home.html',
    posts=posts , nav=nav)

@app.route('/about')
def about():
    return render_template('about.html',nav=nav)

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
    form = form,
    nav=nav)

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
    form = form,
    nav=nav)

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
    updateinfo = ServerInfo()
    navbar = db.session.query(NavBar).first()

    if form.submitupdate.data and form.validate_on_submit():
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

    if current_user.username in allowed_user: # admin mode
        if updateinfo.submitserver.data and updateinfo.validate_on_submit():
            navbar.github = updateinfo.github.data
            navbar.telegram = updateinfo.telegram.data
            navbar.instagram = updateinfo.instagram.data
            navbar.twitter = updateinfo.twitter.data
            navbar.description = updateinfo.description.data   

            db.session.merge(navbar)
            db.session.commit()
            flash('your blog information been updated!' , category='success')
            
        elif request.method == 'GET':
            updateinfo.github.data = navbar.github
            updateinfo.telegram.data = navbar.telegram
            updateinfo.instagram.data = navbar.instagram
            updateinfo.twitter.data = navbar.twitter
            updateinfo.description.data = navbar.description

    imagefile = url_for('static', filename =f"profile/{current_user.image_file}")
    return render_template('account.html',
    title = 'My Profile',
    profile = imagefile ,
    form = form ,
    updateinfo = updateinfo ,
    allowed_user = allowed_user,
    nav = nav)

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
                            form=form,
                            nav=nav)

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


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get ('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page , per_page = 5)

    return render_template('user_posts.html',
    posts=posts , user=user)


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


@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent for reset password.' , category='info')
        return redirect(url_for('login'))

    return render_template('reset_request.html',
                            title = 'Reset Password ',  form = form)

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token!', category='warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash password
        user.password = hashed_password
        # Commit to DB
        db.session.commit()

        flash('Your password has been Updated !',
        category='success')

        return redirect(url_for('login'))
    return render_template('reset_token.html',
    title = 'Reset Password ',  form = form)