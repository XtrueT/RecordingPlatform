from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from ..models import User

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(2,8,'在2-8字符之间'),])
    email = StringField('邮箱',validators=[DataRequired(),Email('邮箱格式不正确')])
    password = PasswordField('密码',validators=[DataRequired()])
    password2 = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password','密码不一致')])
    submit = SubmitField('注册')

    def validate_username(self,username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复')