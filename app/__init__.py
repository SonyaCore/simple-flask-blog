from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.config import APIKEY , SQLDB

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

from app import routes