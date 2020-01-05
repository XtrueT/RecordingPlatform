from flask_wtf import FlaskForm
from wtforms import SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length

class CommentForm(FlaskForm):
    content = TextAreaField('评论',validators=[DataRequired(),Length(max=100)])
    submit = SubmitField('评论/回复')