from . import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(300))
    post_img = db.Column(db.String(256))
    time = db.Column(db.DateTime,index=True)
    address = db.Column(db.String(128),index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    articles = db.relationship('Article',backref='article_post',lazy='dynamic')

    def __repr__(self):
        return f'post:{self.id},{self.title}'