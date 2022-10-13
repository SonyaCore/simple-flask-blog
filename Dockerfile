FROM python:3.10.7-alpine3.16

# SECRET KEY
ENV SECRET_KEY=''

# SQL DATABASE URI
# Default : sqlite:///site.db
ENV SQLALCHEMY_DATABASE_URI=''

# SMTP URL
ENV MAIL_SERVER=''
ENV SMTP_PORT=''

# SMTP PASS
ENV MAIL_USERNAME=''
ENV MAIL_PASSWORD=''

WORKDIR /flask-app

COPY . .

RUN pip3 install -r requirements.txt && python3 dbinit.py


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=80"]

EXPOSE 80