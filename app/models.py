from datetime import datetime
from app import db , login_manager , app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def get_user(user_id):
    return User.query.get(int(user_id))

class ServerName(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    servername = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"ServerName('{self.servername}')"

class NavBar(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    github = db.Column(db.String(80), unique=True, nullable=False,default='#')
    telegram = db.Column(db.String(80), unique=True, nullable=False,default='#')
    instagram = db.Column(db.String(80), unique=True, nullable=False,default='#')
    twitter = db.Column(db.String(80), unique=True, nullable=False,default='#')
    description = db.Column(db.String(80), unique=True, nullable=True,default=None)

    def __repr__(self):
        return f"NavBar('{self.github}','{self.telegram}','{self.instagram}','{self.twitter}','{self.description}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
