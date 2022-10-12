from flask import render_template , request , Blueprint

from app.config import USER_REGISTER
from app.models import Post
from app.main.utils import  nav

main = Blueprint('main',__name__)

@main.route('/')
@main.route('/home')
def home():
    # Load Posts 
    page = request.args.get ('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page , per_page = 5)

    return render_template('home.html',
    posts=posts , nav=nav , USER_REGISTER=USER_REGISTER)

@main.route('/about')
def about():
    return render_template('about.html',nav=nav)