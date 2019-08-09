"""
Routes and views for the flask application.
"""

from datetime import datetime
#图片压缩
from PIL import Image
from flask import render_template,flash,redirect,url_for,request,session,g,json,jsonify,send_from_directory
from myapp import app,db,login,Per_page,ckeditor,photos,default_img,upload_Path
from flask_login import current_user,login_user,logout_user,login_required
from myapp.models import User,Post
from myapp.forms import login_form,signup_form,profile_form,write_form,upload_form
from werkzeug.urls import url_parse
from flask_ckeditor import upload_fail,upload_success
import os

#从session里读取用户信息
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

@app.route('/')
@app.route('/home/<int:page>')
def home(page=1):
    """Renders the home page."""
    #1页数，项目数，true返回404，FALSE返回一个空列表
    users = User.query.all()
    #不能获得所有对象
    #blogs = user.posts.paginate(1, Per_page, False).items
    #获得所有人的post
    posts = Post.query.order_by(db.desc(Post.timestamp)).paginate(page,Per_page,False)
    # has_next：如果在目前页后至少还有一页的话，返回 True
    # has_prev：如果在目前页之前至少还有一页的话，返回 True
    # next_num：下一页的页面数
    # prev_num：前一页的页面数
    return render_template(
        'index.html',
        title='Home',
        users=users,
        posts=posts,
        year = datetime.now().year
    )

@app.route('/detail/<post_id>')
def detail(post_id):
    post = Post.query.filter_by(id = post_id).first()
    posts = Post.query.filter_by(user_id=post.user_id).order_by(db.desc(Post.timestamp)).limit(5).all()
    return render_template(
        'detail.html',
        title ='Detail',
        post = post,
        posts = posts,
        year = datetime.now().year
    )


@app.route('/posts/<int:page>')
@login_required
def posts(page=1):
    posts = Post.query.filter_by(user_id=current_user.id).order_by(db.desc(Post.timestamp)).paginate(page,Per_page,False)
    return render_template(
        'userposts.html',
        title='Posts',
        posts=posts,
        year = datetime.now().year
    )


@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    form = profile_form()
    img_form = upload_form()
    if form.validate_on_submit():
        profile_username = form.username.data
        profile_description = form.description.data
        user_en = User.query.filter_by(username=profile_username).first()
        if  profile_description.strip(' ') == '':
            flash("输入错误")
        elif user_en and user_en.username!=current_user.username:
            flash('用户名重复')
            return redirect(url_for('profile'))
        else:
            try:
                current_user.username = profile_username
                current_user.profile = profile_description
                db.session.commit()
                flash("修改成功")
            except:
                flash("DATABASE ERROR")
    else:
        form.username.data = current_user.username
        form.description.data = current_user.profile
    return render_template(
        'profile.html',
        form=form,
        title = 'ChangProfile',
        img_form=img_form,
        year=datetime.now().year
    )

@app.route('/write',methods=['GET','POST'])
@login_required
def write():
    form=write_form()
    if form.validate_on_submit():
        write_title = form.title.data
        write_content = form.content.data
        if  write_content.strip(' ') == '' or write_title.strip(' ') == '' :
            flash("输入错误")
            return redirect(url_for('write'))
        post = Post(title=write_title,body = write_content,timestamp = datetime.now(),user_id = current_user.id)
        try:
            db.session.add(post)
            db.session.commit()
        except:
            flash('数据库异常')
            return redirect(url_for('write'))
        flash("创建新文章成功")
        postnew = Post.query.filter_by(user_id=current_user.id,title=write_title,body=write_content).first()
        return redirect(url_for('detail',post_id=postnew.id))
    return render_template(
        'write.html',
        title = '新文章',
        form = form,
        year=datetime.now().year
    )

@app.route('/delete/<int:post_page>/<string:post_title>',methods=['GET','POST'])
@login_required
def delete(post_page,post_title):
    post = Post.query.filter_by(user_id=current_user.id,title=post_title).first()
    try:
        db.session.delete(post)
        db.session.commit()
        flash("删除成功")
    except:
        flash("数据库错误")
    return redirect(url_for('posts',page=post_page))

@app.route('/updata/<int:post_page>/<string:post_title>',methods=['GET','POST'])
@login_required
def updata(post_page,post_title):
    form = write_form()
    post = Post.query.filter_by(user_id=current_user.id,title=post_title).first()
    if form.validate_on_submit():
        write_title = form.title.data
        write_content = form.content.data
        if  write_content.strip(' ') == '' or write_title.strip(' ') == '' :
            flash("输入错误")
            return redirect(url_for('updata',post_page,post_title))
        try:
            post.body = write_content
            post.title = write_title
            post.timestamp = datetime.now()
            db.session.add(post)
            db.session.commit()
        except:
            flash('数据库异常')
            return redirect(url_for('updata',post_page,post_title))
        flash("修改文章成功")
        return redirect(url_for('posts',page=post_page))
    else:
        form.content.data = post.body
        form.title.data = post.title
    return render_template(
        'write.html',
        title = '修改文章',
        form = form,
        year=datetime.now().year
    )

@app.route('/login',methods=['GET','POST'])
def login():
    #判断当前用户是否验证，如果通过验证，返回首页
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #创建一个表单实例
    form=login_form()
    if form.validate_on_submit():
        #根据表格里的数据进行查询，查询到返回user对象，否则返回none
        user = User.query.filter_by(email=form.email.data).first()
        #判断用户存在或者密码正确
        if user is None or not user.check_password(form.password.data):
            #用户不存在密码不正确
            flash("无效用户名或密码")
            return redirect(url_for('login'))
        # else:
        login_user(user,remember=form.remember_me.data)
        flash("登录成功")
        # print(form.remember_me.data)
        #记录跳转至登录页的地址
        next_page = request.args.get('next')
        #记录的地址不存在返回首页
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('home')
        return redirect(next_page)    
    return render_template(
        'login.html',
        title='Login',
        form=form,
        year=datetime.now().year
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year
    )

@app.route('/logout')
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('home'))    

@app.route('/signup',methods=['GET','POST'])
def signup():
    # 判断当前用户是否验证，如果通过验证，返回首页
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=signup_form()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,user_img=default_img)
        user.set_password(form.password.data)
        try:
                #创建一个user
            db.session.add(user)
                #在数据库里真的创建
            db.session.commit()
                # 删除
                # db.session.delete(user)
                # db.session.commit()
            flash('注册成功')
            return redirect(url_for('login'))
        except:
            flash('注册失败,数据库异常')
            return redirect(url_for('signup'))
    return render_template(
        'signup.html',
        title='Register',
        form=form,
        year=datetime.now().year
    )

#开始上传,获取上传文件的url
@app.route('/files/<filename>')
def uploaded_files(filename):
    path = upload_Path
    return send_from_directory(path,filename)

@app.route('/upload',methods=['POST'])
def upload():
    f = request.files.get('upload')#获取上传图片文件对象,键必须为‘upload’
    #校验
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg','gif','png','jpeg','md','html',]:
        flash('上传失败')
        return upload_fail(message='文件格式不正确')
    f.save(os.path.join(upload_Path,f.filename))
    print(os.path.join(upload_Path,f.filename))
    url = url_for('uploaded_files',filename=f.filename)
    print(url)
    flash('上传成功')
    return upload_success(url=url)

@app.route('/upload_img',methods=['GET','POST'])
@login_required
def upload_img():
    img_form = upload_form()
    user = User.query.filter_by(id=current_user.id).first()
    before_img = user.user_img
    default_img_url=default_img
    if img_form.validate_on_submit():
        #获取后缀
        img = img_form.upload_photo.data
        shuffix = img.filename.split('.')[-1]
        # 获取唯一
        while True:
            #转换图片名称
            newfileName = new_name(shuffix)
            path = os.path.join(app.config['UPLOADED_PHOTOS_DEST'],newfileName)
            print(path)
            if not os.path.exists(path):
                break
        #压缩图片
        photos.save(img,name=newfileName)
        simg_url = img_zoom(path,'s_')
        #拿到压缩图片url
        img_url = photos.url('s_'+newfileName)
        try:
            #更新该用户的头像
            user.user_img = img_url
            db.session.commit()
            os.remove(path)
            print(img_url)
            flash('修改头像成功')
        except:
            print(img_url)
            os.remove(simg_url)
            print(simg_url)
            os.remove(path)
            print(path)
            print("删除成功")
            flash('修改失败,数据库错误')
            return redirect(url_for('profile',page=1))
    else:
        img_url = before_img
    return redirect(url_for('profile',page=1))
#生成随机图片名称
def new_name(shuffix,length=32):
    import string,random
    Str = string.ascii_letters+string.digits
    newname = ''.join(random.choice(Str) for i in range(length))
    return newname+'.'+shuffix
#缩放图片
def img_zoom(path,perfix,width=200,height=200):
    img = Image.open(path)
    img.thumbnail((width,height))
    path_tup = os.path.split(path)
    path = os.path.join(path_tup[0],perfix+path_tup[1])
    img.save(path)
    return path

@app.errorhandler(404)
def internal_error(e):
    return render_template('error.html',error=e,code=404)

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('error.html',error=e,code=500) 