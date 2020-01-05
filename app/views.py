from datetime import datetime
from flask import g,render_template
from flask_login import current_user
from App import app,login
from .models import db,User
from .main import main
from .post import post
from .article import article
from .comment import comment


# 从session里读取用户信息
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.now()
        db.session.add(g.user)
        db.session.commit()


@app.errorhandler(404)
def internal_error(e):
    return render_template('error.html',error=e,code=404)


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('error.html',error=e,code=500)


app.register_blueprint(post,url_prefix='/posts')
app.register_blueprint(article,url_prefix='/articles')
app.register_blueprint(comment,url_prefix='/comments')
app.register_blueprint(main)