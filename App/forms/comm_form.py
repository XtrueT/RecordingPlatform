from . import FlaskForm
from . import SubmitField,TextAreaField
from . import DataRequired,Length

class CommentForm(FlaskForm):
    content = TextAreaField('留言',validators=[DataRequired(),Length(max=100)])
    submit = SubmitField('完毕')