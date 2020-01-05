import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    #flash需要设置密钥
    SECRET_KEY = "POiuytreqwdbfg#@$%213"
    #格式为mysql + pymysql: // 数据库用户名:密码@数据库地址:端口号/数据库名字？数据库格式
    #出现bug，更换mysql +mysqlconnector
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:7845@localhost:3306/oneappflask?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #设置ckeditor配置,
    # 上传
    CKEDITOR_FILE_UPLOADER ='article.upload'
    # UPLOADED_PATH = os.path.join(BASE_DIR)
    UPLOADED_PATH = BASE_DIR + '\\App\\static\\uploads\\cke'
    #开启Markdown 插件默认关闭
    CKEDITOR_ENABLE_MARKDOWN = True
    #开启代码块
    CKEDITOR_ENABLE_CODESNIPPET = True
    # CSRF
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_SERVE_LOCAL = True
    #全文检索
    # WHOOSH_BASE = os.path.join(basedir, 'db')
    #上传文件存储地址
    UPLOADED_PHOTOS_DEST = BASE_DIR +'/App/static/uploads/photos'
    #图片大小设置
    MAX_CONTENT_LENGTH = 1024*1024*64
