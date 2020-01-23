from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from ..models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(2,8)])
    email = StringField('Email',validators=[DataRequired(),Email('must be email address')])
    password = PasswordField('Password',validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password','passwords entered twice are inconsistent')])
    submit = SubmitField('Submit')

    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('username was be used')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email was be used')