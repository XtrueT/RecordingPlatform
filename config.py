import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #flash需要设置密钥
    SECRET_KEY = os.urandom(24)

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
    UPLOADED_PHOTOS_DEST = BASE_DIR +'\\App\\static\\uploads\\photos'
    #图片大小设置
    MAX_CONTENT_LENGTH = 1024*1024*64



class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    """
        数据库连接配置
        格式为mysql +mysqlconnector: // 数据库用户名:密码@数据库地址:端口号/数据库名字？数据库格式
    """
    conn_type = 'mysql+mysqlconnector'
    user = 'root'
    password = 'Mh123456!'
    host = 'localhost:3306'
    base_name = 'zeez'
    query = 'charset=utf8'

    SQLALCHEMY_DATABASE_URI = f'{conn_type}://{user}:{password}@{host}/{base_name}?{query}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    """
        数据库连接配置
        格式为mysql +mysqlconnector: // 数据库用户名:密码@数据库地址:端口号/数据库名字？数据库格式
    """
    conn_type = 'mysql+mysqlconnector'
    user = 'root'
    password = '7845'
    host = 'localhost:3306'
    base_name = 'oneappflask'
    query = 'charset=utf8'

    SQLALCHEMY_DATABASE_URI = f'{conn_type}://{user}:{password}@{host}/{base_name}?{query}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
