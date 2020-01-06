## 开始

 作为python-flask框架的练手项目，主要是一些过一些流程，实际演练一下。

期待完成：

1. 用户观影记录的收录。
2. 用户观影文章收录。
3. 评论系统的加入。
4. 全站搜索。
5. 管理员系统。

## 相关扩展

```
alembic==1.0.8
aniso8601==6.0.0
Click==7.0
Flask==0.12.4
Flask-CKEditor==0.4.3
Flask-Login==0.4.1
Flask-Migrate==2.4.0
Flask-Script==2.0.6
Flask-SQLAlchemy==2.3.2
Flask-Uploads==0.2.1
Flask-WTF==0.14.2
itsdangerous==1.1.0
Jinja2==2.10
Mako==1.0.8
Markdown==3.1
MarkupSafe==1.1.1
mysql-connector==2.2.9
Pillow==6.0.0
PyMySQL==0.9.3
python-dateutil==2.8.0
python-editor==1.0.4
pytz==2019.1
six==1.12.0
SQLAlchemy==1.3.2
Werkzeug==0.15.2
Whoosh==2.7.4
WhooshAlchemy==0.3.1
WTForms==2.2.1
```
## TODO

- [x] 完成记录平台的登录注册功能模块
- [x] 用户的个人信息维护功能
- [x] CKEditor（文章的撰写，上传图片视频等的富文本编辑器）
- [x] 记录、文章、评论新增功能
- [x] 评论功能
- [ ] 全站搜索
- [ ] 管理员系统

## 项目结构

蓝图，按包的方式进行构建几大模块。

## 数据库设计

目前主要是设计为4个表。

用户表：

```
user:{
	id,
	name(昵称),
	email(帐号),
	password_hash(密码),
	last_seen(最近登录时间),
	avatar(头像),
	// role
	// 以下是不存在的键，只是为其他3表的关系。
	comments(用户评论),
	posts(用户记录),
	articles(用户文章),
}
```

记录表：

```
post:{
	id,
	title(记录名),
	content(简单说明),
	post_img(题图),
	time(时间),
	address(地点),
	user_id(用户外键,提供（post_user）)
}
```

文章表：

```
article:{
	id,
	title,
	content,
	time,
	user_id,
	post_id
}
```

评论表：

```
comment:{
	id,
	title(用于保存被回复者的name),
	content,
	comm_type(评论类型，1或0用于区分是否是回复),
	time,
	to_user_id(是回复则不为null),
	from_user_id(评论者id),
	article_id(关于什么文章的评论)
}
```



user --> post-->article -->comment

