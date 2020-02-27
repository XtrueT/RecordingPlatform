import os
from datetime import datetime
from flask import render_template,flash,redirect,url_for,request,g,send_from_directory,current_app,abort
from flask_login import current_user,login_required
from flask_ckeditor import upload_fail,upload_success
from sqlalchemy import and_
from App import app,PAGESIZE
from ..models import db,Article,Comment
from ..forms import WriteForm,CommentForm
from ..utils import new_name
from . import article


@article.route('/<int:id>')
def articles(id):
    article = Article.query.get(id)
    form = CommentForm()
    articles = Article.query.filter(and_(Article.post_id==article.post_id,Article.id != article.id)).limit(5)
    return render_template(
        'article_detail.html',
        article = article,
        articles = articles,
        form=form,
        year = datetime.now().year
    )


@article.route('/of_posts')
@article.route('/of_posts/<int:post_id>/<int:page>')
def post_articles(post_id,page=1):
    articles = Article.query.filter_by(post_id=post_id).order_by(db.desc(Article.time)).paginate(page,PAGESIZE,False)
    return render_template(
        'articles.html',
        article = article,
        year = datetime.now().year
    )


@article.route('/of_users')
@article.route('/of_users/<int:user_id>/<int:page>')
@login_required
def user_articles(user_id,page=1):
    articles = Article.query.filter_by(user_id=user_id).order_by(db.desc(Article.time)).paginate(page,PAGESIZE,False)
    return render_template(
        'articles.html',
        article = article,
        year = datetime.now().year
    )


@article.route('/new/<int:post_id>',methods=['GET','POST'])
@login_required
def new(post_id):
    form = WriteForm ()
    if form.validate_on_submit():
        article = Article(
            title=form.title.data,
            content=form.content.data,
            time=datetime.now(),
            user_id=current_user.id,
            post_id=post_id
        )
        try:
            db.session.add(article)
            # 返回新建的id
            db.session.flush()
            db.session.commit()
        except:
            flash('新建失败')
            return redirect(url_for('article.new',post_id=post_id))
        flash("创建新文章成功")
        return redirect(url_for('article.articles',id=article.id))
    return render_template(
        'add_article.html',
        title = '新文章',
        form = form,
        year=datetime.now().year
    )


@article.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def update(id):
    form = WriteForm ()
    article = Article.query.get(id)
    if form.validate_on_submit():
        try:
            article.title = form.title.data
            article.content = form.content.data
            article.time = datetime.now()
            db.session.commit()
            flash("成功")
            return redirect(url_for('article.articles',id=article.id))
        except:
            flash('失败')
    form.title.data = article.title 
    form.content.data = article.content
    return render_template(
        'add_article.html',
        title = '修改文章',
        form = form,
        year=datetime.now().year
    )


@article.route('/<int:id>',methods=['DELETE'])
@login_required
def remove(id):
    article = Article.query.get(id)
    if article:
        try:
            db.session.delete(article)
            db.session.commit()
            flash("删除成功")
            return '删除成功',200
        except:
            flash('Error')
            db.session.rollback()
            abort(500)
    


#开始上传,获取上传文件的url
@article.route('/files/<filename>')
def uploaded_files(filename):
    path = app.config['UPLOADED_PATH']
    return send_from_directory(path,filename)


@article.route('/upload',methods=['POST'])
def upload():
    f = request.files.get('upload')
    #获取上传图片文件对象,键必须为‘upload’
    #校验
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg','gif','png','jpeg','md','html',]:
        flash('上传失败')
        return upload_fail(message='文件格式不正确')
    filepath = os.path.join(app.config['UPLOADED_PATH'],f.filename)
    dirname = os.path.dirname(filepath)
    # 直接存可能会出现错误，原因是os不能
    # 原因是os.mkdir 只能生成下一级的目录文件. 若要想生成多个子路径下的文件，需要将os.mkdir 改成 os.makedirs
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except:
            raise OSError('create error')
    elif not os.access(dirname, os.W_OK):
        raise OSError('ERROR_DIR_NOT_WRITEABLE')
    while True:
        # 转换图片名称
        newfileName = 'article_'+new_name(extension)
        # 图片image路径
        path = os.path.join(app.config['UPLOADED_PATH'] ,newfileName)
        if not os.path.exists(path):
            break
    f.save(path)
    url = url_for('article.uploaded_files',filename=newfileName)
    print(url)
    flash('上传成功')
    return upload_success(url=url)