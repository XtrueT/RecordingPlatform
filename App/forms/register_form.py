from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from ..models import User

class RegisterForm(FlaskForm):
    username = StringField('昵称',validators=[DataRequired(),Length(2,8)])
    email = StringField('邮箱',validators=[DataRequired(),Email('must be email address')])
    password = PasswordField('密码',validators=[DataRequired()])
    password2 = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password','passwords entered twice are inconsistent')])
    submit = SubmitField('注册')

    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('username was be used')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('email was be used')