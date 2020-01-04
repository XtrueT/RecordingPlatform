from datetime import datetime
from flask import render_template,flash,redirect,url_for,request,g
from flask_login import current_user,login_required
from App import app,PAGESIZE
from ..models import db,Article,Comment,User,Post
from ..forms import CommentForm
from . import comment

@comment.route('of_articles/<int:article_id>/<int:page>')
def article_comm():
    return  render_template(
        ' '
    )


@comment.route('of_users/<int:user_id>/<int:page>')
@login_required
def user_comm():
    return  render_template(
        ' '
    )


@comment.route('of_articles/<int:article_id>/<int:page>')
@login_required
def new(article_id):
    form = CommentForm()
    if form.validate_on_submit():
        try:
            comm = Comment(
                title=' ',
                content=form.content.data,
                time=datetime.now(),
                form_user_id=current_user.id,
                article_id=article_id
            )
            db.session.add(comm)
            db.session.commit()
            flash("成功")
        except:
            flash('Error')
            db.session.rollback()
    return redirect(url_for('article.articles',id=article_id))