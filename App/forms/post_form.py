from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,DateField
from wtforms.validators import DataRequired,Length
from flask_wtf.file import FileField,FileAllowed,FileRequired
from App import photos

class PostForm(FlaskForm):
    post_img = FileField(validators=[FileAllowed(photos,'only images'),FileRequired()])
    title = StringField('Title',validators=[DataRequired(),Length(min=0,max=12)])
    time = DateField('Time',validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired(),Length(max=24)])
    content = TextAreaField('Write',validators=[DataRequired(),Length(max=300)]) 
    submit = SubmitField('Submit')