from flask_wtf import FlaskForm

from wtforms import StringField , SubmitField , TextAreaField
from wtforms.validators import DataRequired 

class ServerInfo(FlaskForm):
    github = StringField('GitHub',
                            validators=[DataRequired()])
    telegram = StringField('Telegram',
                            validators=[DataRequired()])
    instagram = StringField('Instagram',
                            validators=[DataRequired()])
    twitter = StringField('Twitter',
                            validators=[DataRequired()])
    description = StringField('Description',
                            validators=[DataRequired()])
    submitserver = SubmitField('Update Server Information')


class PostForm(FlaskForm):
    title = StringField('Title',
                            validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit  = SubmitField('Post')

