from . import FlaskForm
from . import StringField,SubmitField,TextAreaField,DateField
from . import DataRequired,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from App import photos

class PostForm(FlaskForm):
    post_img = FileField(validators=[FileAllowed(photos,'只能是图片'),FileRequired('未选择文件')])
    title = StringField('title',validators=[DataRequired(),Length(max=12)])
    time = DateField('time',validators=[DataRequired()])
    address = StringField('address',validators=[DataRequired(),Length(max=24)])
    content = TextAreaField('开始',validators=[DataRequired(),Length(max=300)]) 
    submit = SubmitField('完毕')