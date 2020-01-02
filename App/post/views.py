import os
from datetime import datetime
from werkzeug.urls import url_parse
from flask import render_template,flash,redirect,url_for,request,g
from flask_login import current_user,login_required
from App import PAGESIZE,DEFAULT_AVATAR
from ..models import db,User,Post,Article
from ..forms import PostForm
from ..utils import upload_img
from . import post



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
        except:
            flash('Error')
            db.session.rollback()
    return render_template(
        'add_post.html',
        form=form,
        year=datetime.now().year
    )


@post.route('/<int:id>',methods=['DELETE'])
@login_required
def remove(id):
    post = Post.query.get(id=id)
    if post:
        try:
            db.session.delete(post)
            db.session.commit()
            flash("成功")
        except:
            flash('Error')
            db.session.rollback()


@post.route('/update/<int:id>',methods=['GET','PUT'])
@login_required
def update(id):
    post = Post.query.get(id=id)
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
        else:
            form.title.data = post.title
            form.content.data = post.content
            form.time.data =  post.time
            form.address.data = post.address
    return render_template(
        'add_post.html',
        form=form,
        year=datetime.now().year
    )
