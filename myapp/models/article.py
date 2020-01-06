from . import db

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(1000))
    time = db.Column(db.DateTime,index=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    comments = db.relationship('Comment',backref='comment_article',lazy='dynamic')

    def __repr__(self):
        return f'article:{self.id},{self.title},{self.user_id}'