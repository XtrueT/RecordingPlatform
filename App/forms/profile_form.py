from flask import g
from . import FlaskForm
from . import StringField,SubmitField
from . import DataRequired,Email,EqualTo,Length
from ..models import User


class ProfileForm(FlaskForm): 
    username = StringField('用户名',validators=[DataRequired(),Length(2,8,'在2-8字符之间'),])
    email = StringField('邮箱',validators=[DataRequired(),Email('邮箱格式不正确')])
    submit = SubmitField('确认')

    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None and user.name != g.user.name:
            raise ValidationError('用户名已被使用')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user.email != g.user.email:
            raise ValidationError('邮箱已被使用')