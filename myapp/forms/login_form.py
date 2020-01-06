from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    #DataRequired,没有在当前表格输入直接到下一个表格输入会提示
    email = StringField('邮箱',validators=[DataRequired(),Email('邮箱格式不正确')])
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')