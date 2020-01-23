from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    #DataRequired,没有在当前表格输入直接到下一个表格输入会提示
    email = StringField('Email',validators=[DataRequired(),Email('must be email address')])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField()
    submit = SubmitField('Submit')