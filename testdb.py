from app import db
from app.models import ServerName , NavBar

#NavBar.__table__.create(db.engine)

#ServerName.__table__.drop(db.engine)

# server = ServerName()
#server.servername = 'Sonia Blog'

#db.session.add(server)
#db.session.commit()

# def servername():
#     name = db.session.query(ServerName).all()
#     for query in name: 
#         print(f'{query.servername}')
# servername()

# server = NavBar()
# server.github = 'https://github.com/SoniaCore'
# server.telegram = 'https://telegram.me/ReiLibre'
# server.description = 'Still in Development @SoniaCore'

# db.session.add(server)
# db.session.commit()

# def nav():
#     name = db.session.query(NavBar).all()
#     for query in name: 
#         print(f"'{query.github}','{query.telegram}','{query.instagram}','{query.twitter}','{query.description}'")
# nav()
nav = db.session.query(NavBar).first()
nav.github = 'https://github.com/SoniaCore'
db.session.commit()
print(nav.github)