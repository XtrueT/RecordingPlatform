from datetime import datetime
from flask import render_template,flash,redirect,url_for,request,g,abort
from flask_login import current_user,login_required
from App import app,PAGESIZE
from ..models import db,Article,Comment,User,Post
from ..forms import CommentForm
from . import comment

@comment.route('/of_articles/<int:article_id>/<int:page>')
def article_comm():
    return  render_template(
        ' '
    )


@comment.route('/of_users/<int:user_id>/<int:page>')
@login_required
def user_comm():
    return  render_template(
        ' '
    )

@comment.route('/of_articles/<int:article_id>/<int:to_user>',methods=['POST'])
@comment.route('/of_articles/<int:article_id>',methods=['POST'])
@login_required
def new(article_id,to_user=None):
    form = CommentForm()
    if form.validate_on_submit():
        try:
            comm = Comment()
            comm.article_id = article_id
            comm.content = form.content.data
            comm.form_user_id = current_user.id
            comm.time = datetime.now()
            if to_user:
                user = User.query.get(to_user)
                if user:
                    comm.title = user.name
                    comm.comm_type = 0
                    comm.to_user_id = to_user
            db.session.add(comm)
            db.session.commit()
            flash("成功")
        except:
            flash('Error')
            db.session.rollback()
    return redirect(url_for('article.articles',id=article_id))

@comment.route('/<int:id>',methods=['DELETE'])
@login_required
def remove(id):
    comment = Comment.query.get(id)
    if comment:
        try:
            db.session.delete(comment)
            db.session.commit()
            flash("删除成功")
            return '删除成功',200
        except:
            flash('Error')
            db.session.rollback()
            abort(500)