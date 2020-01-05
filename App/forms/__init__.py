from flask_wtf import CSRFProtect
from App import app


csrf = CSRFProtect(app)


from .login_form import LoginForm
from .register_form import RegisterForm
from .profile_form import ProfileForm
from .write_form import WriteForm
from .post_form import PostForm
from .upload_form import UploadForm
from .comm_form import CommentForm