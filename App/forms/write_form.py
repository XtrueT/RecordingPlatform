from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField



class WriteForm(FlaskForm):
    title = StringField('标题',validators=[DataRequired(),Length(max=12)])
    content = CKEditorField('开始',validators=[DataRequired(),Length(max=1000)]) 
    submit = SubmitField('完毕')