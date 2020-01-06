from flask_sqlalchemy import SQLAlchemy
from App import app


db = SQLAlchemy(app)

def create_app():
    db.init_app(app)
    db.create_all()
    return app

from .user import User
from .post import Post
from .article import Article
from .comment import Comment

