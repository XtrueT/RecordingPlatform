import os
from datetime import datetime
from werkzeug.urls import url_parse
from flask import render_template,flash,redirect,url_for,request,g,abort
from flask_login import current_user,login_required
from App import PAGESIZE,DEFAULT_AVATAR
from ..models import db,User,Post,Article
from ..forms import PostForm
from ..utils import upload_img
from . import post

@post.route('/<int:id>')
def posts(id):
    post = Post.query.get(id)
    articles = Article.query.filter_by(post_id=id).order_by(db.desc(Article.time)).limit(5).all()
    return render_template(
        'post_detail.html',
        post = post,
        articles = articles,
        year = datetime.now().year
    )

@post.route('/of_users/<int:id>')
@post.route('/of_users/<int:id>/<int:page>')
def user_posts(id,page=1):
    paginate = Post.query.filter_by(user_id=id).order_by(db.desc(Post.time)).paginate(page,PAGESIZE,False)
    user = User.query.get(id)
    tab = request.args.get('tab')
    if tab == 'article':
        paginate = Article.query.filter_by(user_id=id).order_by(db.desc(Article.time)).paginate(page,PAGESIZE,False)
    return render_template(
        'user_posts.html',
        paginate=paginate,
        tab=tab,
        user=user
    )


@post.route('/new',methods=['GET','POST'])
@login_required
def new():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                post_img=upload_img(form.post_img.data,before=None,not_s=True),
                time=form.time.data,
                address=form.address.data,
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            flash("成功")
            return redirect(url_for('main.home'))
        except:
            flash('Error')
            db.session.rollback()
    return render_template(
        'add_post.html',
        title='新动态',
        form=form,
        year=datetime.now().year
    )


@post.route('/<int:id>',methods=['DELETE'])
@login_required
def remove(id):
    post = Post.query.get(id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("删除成功")
            return '删除成功',200
        except:
            flash('Error')
            abort(500)


@post.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if post:
        form = PostForm()
        if form.validate_on_submit():
            try:        
                post.title = form.title.data
                post.content = form.content.data
                post.post_img = upload_img(form.post_img.data,before=None,not_s=True)
                post.time = form.time.data
                post.address = form.address.data
                post.user_id = current_user.id
                db.session.commit()
                flash("成功")
            except:
                flash('Error')
                db.session.rollback()
            return redirect(url_for('post.posts',id=post.id))
        else:
            form.title.data = post.title
            form.content.data = post.content
            form.time.data =  post.time
            form.address.data = post.address
            post_img_src = post.post_img
    return render_template(
        'add_post.html',
        form=form,
        post_img_src=post_img_src,
        year=datetime.now().year
    )
