"""
The flask application package.
"""
from flask import Flask
#导入配置文件
from config import Config
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class

app = Flask(__name__)

#添加配置信息

app.config.from_object(Config)

#登录模块初始化
login = LoginManager(app)
#登录限制
login.login_view = 'login'

#分页初始化
Per_page = 6

#富文本ckeditor

ckeditor = CKEditor(app)

upload_Path =  app.config['UPLOADED_PATH']
#csrf
csrf = CSRFProtect(app)
#上传
#设置上传文件类型为图片,实例化一个photos对象继承save，url方法
#类型是images可以直接过滤
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)
#上传大小限制，默认16MB
patch_request_class(app,size=None)
#设置默认头像
default_img = 'http://localhost:5555/_uploads/photos/s_i3nyfHsH31Q3wWvaWF0iXSvzx1mJK7Kh.jpg'

import App.views,App.models


