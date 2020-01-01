from myapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(120),index=True,unique=True)
    password_hash = db.Column(db.String(128))
    # role = db.Column(db.SmallInteger,default=ROLE_USER)
    last_seen = db.Column(db.DateTime)
    profile = db.Column(db.String(140))
    user_img = db.Column(db.String(140))
    #方便查询在 一的一方(一对多)，增加一个关联，不是真实的列
    #backref 给post用的，
    posts = db.relationship('Post',backref='post_username',lazy='dynamic')
    # is_authenticated 通过验证的用户满足login_required
    # is_active 
    # is_anonymous
    # get_id() 返回Unicode 如果id是int 需要转换为Unicode
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
        
    #显示一个可读字符串
    def __repr__(self):
        return f'user:{self.username}'

    #加密密码
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(2000))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))#表名.列名连接外键
    title = db.Column(db.String(100))

    def __repr__(self):
        return '<Post:{}>'.format(self.body)


