from . import db

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(1000))
    comm_type = db.Column(db.SmallInteger,default=1)
    time = db.Column(db.DateTime,index=True)
    to_user_id = db.Column(db.Integer)
    form_user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer,db.ForeignKey('article.id'))

    def __repr__(self):
        return f'comment:{self.id},{self.title},{self.user_id}'