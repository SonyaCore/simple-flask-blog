from app.models import ServerName , NavBar
from app import db

# Blog Name
def servername():
    name = db.session.query(ServerName).all()
    for query in name: 
        return query.servername

# Additional Navbar Information
nav = db.session.query(NavBar).all()

# Debug Mode

# @app.before_request
# def log_request_info():
#     app.logger.debug('Headers: %s\n', request.headers)
#     app.logger.debug('Body: %s\n', request.get_data())

