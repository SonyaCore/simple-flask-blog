from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

try :
    print('First Time database creation \n"Press Ctrl + C if you want to cancel the installation')
    sleep(5)
except KeyboardInterrupt:
    exit('\nCanceled')

# DB APP Module import
from app import db , bcrypt
from app import Config as APPCONFIG
from app.models import ServerName , NavBar , User

engine = create_engine(
    APPCONFIG.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

class Config:
    SERVERNAME = 'Simple Blog'
    GITHUB = '#'
    TELEGRAM = '#'
    INSTAGRAM = '#'
    TWITTER = '#'
    DESCRIPTION = ''

class Admin:
    USERNAME = 'admin'
    EMAIL = 'admin@gmail.com'
    PASSWORD = 'admin'

# ServerName
server = ServerName()
server.servername = Config.SERVERNAME
db.session.add(server)
db.session.commit()

print(server.servername)

# NavBar Information
navbar = NavBar()
navbar.github = Config.GITHUB
navbar.telegram = Config.TELEGRAM
navbar.instagram = Config.INSTAGRAM
navbar.twitter = Config.TWITTER
navbar.description = Config.DESCRIPTION
db.session.add(navbar)
db.session.commit()

for query in db.session.query(NavBar).all(): 
    print(str(f"{query.github}\n{query.telegram}\n{query.instagram}\n{query.twitter}\n{query.description}"))

# Admin Creation
admin = User()
PASSWORD = bcrypt.generate_password_hash(Admin.PASSWORD).decode('utf-8')
admin.username = Admin.USERNAME
admin.email = Admin.EMAIL
admin.password = PASSWORD
db.session.add(admin)
db.session.commit()

print('Admin Information:')
print('Email :', Admin.EMAIL)
print('Password :' , Admin.PASSWORD)

## Drop DB's
# ServerName.__table__.drop(db.engine)
# NavBar.__table__.drop(db.engine)
