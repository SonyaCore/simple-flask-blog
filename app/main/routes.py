from flask import render_template , request , Blueprint
from app.models import Post
from app.main.utils import servername , nav
main = Blueprint('main',__name__)

blogname = Blueprint('blogname',__name__)

@blogname.context_processor
def name():
    info = {
         'servername':   f'{servername()}'
     }
    return dict(info=info)


@main.route('/')
@main.route('/home')
def home():
    # Load Posts 
    page = request.args.get ('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page , per_page = 5)

    return render_template('home.html',
    posts=posts , nav=nav)

@main.route('/about')
def about():
    return render_template('about.html',nav=nav)