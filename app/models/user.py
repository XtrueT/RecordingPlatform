from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime)
    avatar = db.Column(db.String(256))
    posts = db.relationship('Post',backref='post_user',lazy='dynamic')
    comments = db.relationship('Comment',backref='comment_user',lazy='dynamic')
    articles = db.relationship('Article',backref='article_user',lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'user:{self.user_name}'