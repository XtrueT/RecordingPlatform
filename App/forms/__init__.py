from flask_wtf import FlaskForm,CSRFProtect
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField,FormField,DateField
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms.validators import DataRequired,ValidationError,Email,EqualTo,Length
from App import app


csrf = CSRFProtect(app)


from .login_form import LoginForm
from .register_form import RegisterForm
from .profile_form import ProfileForm
from .write_form import WriteForm
from .post_form import PostForm
from .upload_form import UploadForm
from .comm_form import CommentForm