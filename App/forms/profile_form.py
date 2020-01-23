from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,Length
from ..models import User

class ProfileForm(FlaskForm): 
    username = StringField('Username',validators=[DataRequired(),Length(2,8)])
    email = StringField('Email',validators=[DataRequired(),Email('must be email address')])
    submit = SubmitField('Submit')

    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None and user.name != g.user.name:
            raise ValidationError('username was be used')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user.email != g.user.email:
            raise ValidationError('email was be used')