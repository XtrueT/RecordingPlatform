from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField,FormField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from flask_ckeditor import CKEditorField
from myapp import photos
from myapp.models import User


class login_form(FlaskForm):
    #DataRequired,没有在当前表格输入直接到下一个表格输入会提示
    email = StringField('邮箱',validators=[DataRequired(),Email('邮箱格式不正确')],render_kw={'class': 'form-control'})
    password = PasswordField('密码',validators=[DataRequired(message='请输入密码')],render_kw={'class': 'form-control'})
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录',render_kw={'class': 'btn btn-success'})

class signup_form(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()],render_kw={'class': 'form-control'})
    email = StringField('邮箱',validators=[DataRequired(),Email('邮箱格式不正确')],render_kw={'class': 'form-control'})
    password = PasswordField('密码',validators=[DataRequired()],render_kw={'class': 'form-control'})
    password2 = PasswordField('确认密码',validators=[DataRequired(),EqualTo('password','密码不一致')],render_kw={'class': 'form-control'})
    submit = SubmitField('注册',render_kw={'class': 'btn btn-success'})

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复')
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱重复')

class profile_form(FlaskForm): 
    username = StringField('用户名',validators=[DataRequired(message='请输入用户名')],render_kw={'class': 'form-control'}) 
    description = TextAreaField('个人信息', validators=[DataRequired(), Length(max=140),],render_kw={'class': 'form-control'}) 
    submit = SubmitField('确认',render_kw={'class': 'btn btn-success'})

class write_form(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(max=100)],render_kw={'class': 'form-control'})
    content = CKEditorField('开始',validators=[DataRequired()],render_kw={'class': 'form-control'}) 
    submit = SubmitField('完毕',render_kw={'class': 'btn btn-success'})


class upload_form(FlaskForm):
    upload_photo = FileField(validators=[FileAllowed(photos,'只能是图片'),FileRequired('未选择文件')])
    
    submit = SubmitField('上传',render_kw={'class': 'btn btn-success'})


