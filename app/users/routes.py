import os

from flask import render_template , url_for, flash , redirect , request , abort , Blueprint
from app import app , db , bcrypt , mail

from app.main.utils import NavBar , nav
from app.posts.forms import ServerInfo

from app.users.forms import RegistrationForm , LoginForm , UpdateAccountForm , User , ResetPasswordForm , RequestResetForm
from app.users.utils import allowed_user , save_picture , send_reset_email , username_regex , password_regex
from app.models import Post
from flask_login import current_user , login_required , logout_user , login_user

users = Blueprint('users',__name__)

## Registering Users
@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
            return redirect(url_for('main.home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        # Username Check
        if username_regex(form.username.data):
            pass
        else:
            flash("Illegal characters in username.",category='warning')
            return render_template('register.html',
            form = form)

        # Password Check
        if password_regex(form.password.data):
            pass
        else:
            flash("Password must be 6+ chars and have 1 lowercase letter, 1 uppercase letter and 1 digit.",category='warning')
            return render_template('register.html',
            form = form)

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

        return redirect(url_for('users.login'))
    return render_template('register.html',
    title='Register',
    form = form,
    nav=nav)

@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user,remember=form.remember.data)
            flash('You Have been logged in!', category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Failed Check your information!', category='danger')
    return render_template('login.html',
    title='Login',
    form = form,
    nav=nav)

@users.route('/account',methods=['GET','POST'])
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
        return redirect(url_for('users.account'))

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

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get ('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page , per_page = 5)

    return render_template('user_posts.html',
    posts=posts , user=user)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent for reset password.' , category='info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html',
                            title = 'Reset Password ',  form = form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token!', category='warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash password
        user.password = hashed_password
        # Commit to DB
        db.session.commit()

        flash('Your password has been Updated !',
        category='success')

        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
    title = 'Reset Password ',  form = form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
