from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from App import photos


class UploadForm(FlaskForm):
    upload_photo = FileField(validators=[FileAllowed(photos,'only images'),FileRequired()])
    submit = SubmitField('Submit')