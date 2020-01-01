from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand 
from app.models import db,app

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

# db.drop_all()#删除所有表
# db.create_all()#创建所有表
if __name__ == '__main__':
    manager.run()
# 1.    python manage.py db init  初始化出migrations的文件，只调用一次

# 2.    python manage.py db migrate  生成迁移文件

# 3.    python manage.py db upgrade 执行迁移文件中的升级(需要先进行2在进行3)

# 4.    python manage.py db downgrade 执行迁移文件中的降级(需要先进行2在进行4)
#(第一次生成表，依次执行1234)
# 5.    python manage.py db --help 帮助文档

