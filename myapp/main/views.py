import os
from datetime import datetime
from werkzeug.urls import url_parse
from flask import render_template,flash,redirect,url_for,request,g
from flask_login import current_user,login_user,logout_user,login_required
from App import PAGESIZE,DEFAULT_AVATAR
from ..models import db,User,Post,Article
from ..forms import LoginForm,RegisterForm,ProfileForm,UploadForm
from ..utils import upload_img
from . import main


@main.route('/')
@main.route('/home/<int:page>')
def home(page=1):
    users = User.query.order_by(db.desc(User.last_seen)).paginate(page,PAGESIZE,False)
    return render_template(
        'index.html',
        title='Home',
        users=users,
        year = datetime.now().year
    )


@main.route('/login',methods=['GET','POST'])
def login():
    # 判断当前用户是否验证，如果通过验证，返回首页
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    # 创建一个表单实例
    form = LoginForm()
    if form.validate_on_submit():
        # 根据表格里的数据进行查询，查询到返回user对象，否则返回none
        user = User.query.filter_by(email=form.email.data).first()
        # 判断用户存在或者密码正确
        if not user:
            flash("未注册用户")
            return redirect(url_for('main.login'))
        if not user.check_password(form.password.data):
            flash("密码错误")
            return redirect(url_for('main.login'))
        # 登录成功保存是否记住密码状态
        login_user(user,remember=form.remember_me.data)
        flash("登录成功")
        # 记录跳转至登录页的地址
        next_page = request.args.get('next')
        # 记录的地址不存在返回首页
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('main.home')
        return redirect(next_page)    
    return render_template(
        'login.html',
        title='Login',
        form=form,
        year=datetime.now().year
    )


@main.route('/register',methods=['GET','POST'])
def register():
    # 判断当前用户是否验证，如果通过验证，返回首页
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
            avatar=DEFAULT_AVATAR
        )
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            # 登录成功保存是否记住密码状态
            login_user(user)
            flash("登录成功")
            return redirect(url_for('main.home'))
        except:
            flash('注册失败')
            db.rollback()
            return redirect(url_for('main.register'))
    return render_template(
        'register.html',
        title='Register',
        form=form,
        year=datetime.now().year
    )


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('main.home'))    


@main.route('/profile',methods=['GET','POST'])
@main.route('/profile/<int:page>',methods=['GET','POST'])
@login_required
def profile(page=1):
    form = ProfileForm()
    img_form = UploadForm()
    if form.validate_on_submit():
        try:
            current_user.name = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("修改成功")
        except:
            flash("错误")
            db.session.rollback()
    else:
        form.username.data = current_user.name
        form.email.data = current_user.email
        user_posts = Post.query.filter_by(user_id=current_user.id).order_by(db.desc(Post.time)).paginate(page,PAGESIZE,False)
    return render_template(
        'profile.html',
        title='Profile',
        form=form,
        img_form=img_form,
        posts=user_posts,
        year=datetime.now().year
    )


@main.route('/avatar',methods=['POST'])
@login_required
def avatar():
    img_form = UploadForm()
    before_avatar = current_user.avatar
    if img_form.validate_on_submit():
        try:
            # 更新该用户的头像,保存文件并返回url
            current_user.avatar = upload_img(img_form.upload_photo.data,before_avatar)
            db.session.commit()
            flash('成功')
        except:
            flash('失败')
    return redirect(url_for('main.profile'))

