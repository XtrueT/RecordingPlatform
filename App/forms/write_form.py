from . import FlaskForm
from . import StringField,SubmitField
from . import DataRequired,Length
from flask_ckeditor import CKEditorField

class WriteForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(max=12)])
    content = CKEditorField('开始',validators=[DataRequired(),Length(max=900)]) 
    submit = SubmitField('完毕')