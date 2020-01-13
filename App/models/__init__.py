from flask_sqlalchemy import SQLAlchemy
from App import app


db = SQLAlchemy(app)

from .user import User
from .post import Post
from .article import Article
from .comment import Comment

