"""
The flask application package.
"""
from flask import Flask
from flask_login import LoginManager
from config import config
from flask_ckeditor import CKEditor
from flask_uploads import UploadSet,configure_uploads,IMAGES,patch_request_class

app = Flask(__name__)

#添加配置信息
app.config.from_object(config.get('development'))

# 登录模块初始化
login = LoginManager(app)
# 登录限制
login.login_view = 'main.login'


# 富文本ckeditor

ckeditor = CKEditor(app)


#上传
# 设置上传文件类型为图片,实例化一个photos对象继承save，url方法
# 类型是images可以直接过滤
photos = UploadSet('photos',IMAGES)
configure_uploads(app,photos)
#上传大小限制，默认16MB
patch_request_class(app,size=None)


#分页初始化
PAGESIZE = 20

#上传保存地址

UPLOAD_PHOTOS = app.config['UPLOADED_PHOTOS_DEST']


#设置默认头像
DEFAULT_AVATAR = 'http://localhost:5555/_uploads/photos/s_image_EQlM1P1oGrbYZ1yYzYoAAYGAPpfZnDeg.jpg'

import App.views


