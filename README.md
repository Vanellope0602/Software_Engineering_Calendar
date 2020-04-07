# Software_Engineering_Calendar
A calendar web app that can regulate events using python flask

## Tips for run it！
## 系统部署说明

### 简介

- 后端使用Python3.6.8，前端用了Bootstrap模板
- Flask框架以及插件和版本如下所示（命令行在后面）

```
  SQLAlchemy          1.3.15
  sqlalchemy-migrate  0.13.0
  Werkzeug            0.16.0
  Flask               1.1.1
  Flask-Babel         1.0.0
  Flask-Bootstrap     3.3.7.1
  Flask-Datepicker    0.12
  Flask-Login         0.4.1
  Flask-Mail          0.9.1
  Flask-Migrate       2.2.1
  flask-mongoengine   0.9.5
  Flask-OpenID        1.2.5
  Flask-Script        2.0.6
  Flask-SQLAlchemy    2.3.2
  Flask-WhooshAlchemy 0.56
  Flask-WTF           0.14.2
  Jinja2              2.10.3
  WTForms             2.2.1
```



### 1. 配置环境Bash命令

```bash
cd Calendar	# 进入代码所在目录
pip3 install virtualenv
virtualenv calendar_flask # 为了避免混乱，创建一个虚拟环境
source calendar_flask/bin/activate #激活该虚拟环境
# pip --version 查看版本是3.6即可继续安装
pip install -r requirement.txt #安装依赖包
```



### 2. 修改代码中读取sqlite数据库文件为绝对路径

在`main.py`文件中，这一行需要修改：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'
# 注意这里要求database.db文件路径为绝对路径
# 例如：
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/wangshanshan/Desktop/Calendar/database.db'
```



### 3. 初始化数据库后开始运行

```python
# 接着上面的Bash命令
sqlite3 database.db  # 建立数据库文件
.exit
# ---- 分割线 ----
python3 			 # 根据系统不同可能使用python或者py
from main import db 
db.drop_all()
db.create_all()
quit()				# 完成数据库初始化

python3 main.py    # 开始运行
```



### 【Tips】网络连接需要

- 可能需要**科学上网**，不然第一次加载html中使用的一些在线JS/CSS文件会比较慢，并不是后台的问题


