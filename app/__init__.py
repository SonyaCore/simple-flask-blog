from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import APIKEY , SQLDB

# App Name
app = Flask(__name__)

# App Config
app.config['SECRET_KEY'] = APIKEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# App Database
db = SQLAlchemy(app)

from app import routes