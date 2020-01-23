from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_ckeditor import CKEditorField



class WriteForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(max=12)])
    content = CKEditorField('Write',validators=[DataRequired(),Length(max=1000)]) 
    submit = SubmitField('Submit')