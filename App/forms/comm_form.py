from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

class CommentForm(FlaskForm):
    content = TextAreaField('Write',validators=[DataRequired(),Length(max=100)])
    submit = SubmitField('Submit')