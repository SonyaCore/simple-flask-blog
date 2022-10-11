from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config
from logging.config import dictConfig 

# App Config
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

# Logging Output
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Routes
from app.routes import servername , name
from app.main.routes import main
from app.posts.routes import posts
from app.users.routes import users

# Main Page
app.register_blueprint(main)

# Posts
app.register_blueprint(posts)

# Users
app.register_blueprint(users)

## Create APP Class (no use for now)

# def createapp(config_class=Config):
#     # App Name
#     app = Flask(__name__)
#     app.config.from_object(Config)

#     # Set init to Flask app
#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)
#     mail.init_app(app)

#     # Routes
#     from app.main.routes import blogname
#     from app.main.routes import main
#     from app.posts.routes import posts
#     from app.users.routes import users

#     app.register_blueprint(blogname)
#     app.register_blueprint(main)
#     app.register_blueprint(posts)
#     app.register_blueprint(users)

#     return app