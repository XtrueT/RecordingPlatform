from . import FlaskForm
from . import SubmitField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from App import photos


class UploadForm(FlaskForm):
    upload_photo = FileField(validators=[FileAllowed(photos,'只能是图片'),FileRequired('未选择文件')])
    submit = SubmitField('上传')