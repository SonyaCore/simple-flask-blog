from flask import Flask , request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import APIKEY , SQLDB
from logging.config import dictConfig 

# App Name
app = Flask(__name__)

# App Config
app.config['SECRET_KEY'] = APIKEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# App Database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

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
from app import routes