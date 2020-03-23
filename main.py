import pymysql
import sqlite3
from app import app
from datetime import datetime
from db_config import mysql
from flask import flash, render_template, jsonify, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm	# 版本太高导致无法import url_code werkzeug==0.16.0
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from wtforms.fields.html5 import DateTimeField
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

PROJECT_ROOT = '/Users/fandahao1/Documents/20Spring/SoftwareEngineer/Software_Engineering_Calendar'

# app = Flask(__name__) # 这个已经在app.py里有了
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + PROJECT_ROOT + '/database.db'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/calendar_system'
Bootstrap(app)
db = SQLAlchemy(app)  # 一个代表数据库的class
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True) #
	email = db.Column(db.String(15), unique=True)
	password = db.Column(db.String(80))

class Event(db.Model):
	id = db.Column(db.Integer, primary_key=True)  # unique id
	title = db.Column(db.String)					# biaoti
	url = db.Column(db.String)
	type = db.Column(db.String) # class??
	start_time = db.Column(db.TIMESTAMP)  # datetime
	end_time = db.Column(db.TIMESTAMP)
	author_name = db.Column(db.String, db.ForeignKey("user.username"))
	# user要小写！！

# login_required 的逻辑其实是将user_id传给回调函数
# 然后如果回调函数查得出东西，login_required就给通过，不行就扔回去登录页面
@login_manager.user_loader
def load_user(user_id):		# 这是个函数，不是类
	return User.query.get(int(user_id))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(message='用户名不能为空噢'), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(message='密码不能为空噢'), Length(min=8, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(message='邮箱不能为空噢'),Email(message='这个不是正确格式的邮箱诶'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(message='用户名不能为空噢'), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	submit = SubmitField('Submit')

class EventForm(FlaskForm):
	event_title = StringField('日程名称', validators=[InputRequired(message='日程名称不能为空噢')])
	type = SelectField('请选择类别', validators=[InputRequired()],
					   choices=[('event-info', 'Info蓝色'), ('event-important', '重要-红色'), ('event-error', '普通-灰色')],
					   id='typearea')
	start = DateTimeField('起始时间（格式：yyyy/mm/dd hh:mm）', validators=[InputRequired(message='起始日期不能为空噢')], format='%Y/%m/%d %H:%M',id='datetime-start')
	end = DateTimeField('结束时间（格式：yyyy/mm/dd hh:mm）', validators=[InputRequired(message='结束日期也不能为空噢')], format='%Y/%m/%d %H:%M',id='datetime-end')
	descirbe = StringField('详细备注') # 可以留空
	submit = SubmitField('提交')

class SearchForm(FlaskForm):
	keyword = StringField('关键字搜索日程', validators=[InputRequired()])
	submit = SubmitField('搜索')


@app.route('/')
def index():	# http://127.0.0.1:5000/ 即展示return的页面
	# 我们想要把它改为登陆界面index，calendar只用于展示用户个人的日程
	#return render_template('calendar_events.html')
	return render_template('index.html')

# 只有访问这个页面的时候才是正常的有数据的日历！！！
@app.route('/dashboard',methods=['GET','POST']) # profile
@login_required
def dashboard():
	return render_template('calendar_events.html', message='登陆后看到的', name=current_user.username)

@app.route('/calendar-events')	#并不会直接访问这个route,html中调用这个calendar-events来返回信息
def calendar_events():
	conn = None
	cursor = None
	try:
		conn = sqlite3.connect("database.db")	# 连接sqlite
		cursor = conn.cursor();
		# 原本用的是UNIX_TIMESTAMP，*1000是模板要求的时间戳
		#cursor.execute("SELECT id, title, url, class, UNIX_TIMESTAMP(start_date)*1000 as start, UNIX_TIMESTAMP(end_date)*1000 as end FROM event")

		sql_select = "SELECT id, title, url, type, (strftime('%s', start_time)-28800)*1000 as start, (strftime('%s', end_time)-28800)*1000 as end FROM event where author_name='" + current_user.username + "'";
		rows = cursor.execute(sql_select).fetchall()
		# 如果用sqlite fetchall要直接跟在execute后面, sqlite查询出来的时间多跑了8个小时，所以减去8个小时的秒数28800
		#rows = cursor.fetchall()
		# 两种情况下rows都是一个List，但是Mysql装的是Dict，Sqlite装的是Tuple？

		rows_dict = []
		# 这里会改名叫class，所以不用担心json的问题啦！
		dict_key = ('id','title','url','class','start','end')
		for line in rows:	# 每个line是一个Tuple
			rows_dict.append(dict(zip(dict_key, line)))

		resp = jsonify({'success' : 1, 'result' : rows_dict})	# 转化为，，，便于数据展示
		resp.status_code = 200
		return resp
	except Exception as e:
		print('OH my god! Exception found!')
		print(e)
	finally:
		print("在calendar_event中有个finally不知道干嘛，conn是Nonetype，尚未部署数据库")
		cursor.close() # 关闭游标
		conn.close()


@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()		# 登录表
	if form.validate_on_submit():
		# query database
		user = User.query.filter_by(username=form.username.data).first() # username should be unique
		if user: # 用户存在，比较密码，左侧为数据库中用户密码的哈希，右侧为登录表单时用户输入的密码
			if check_password_hash(user.password, form.password.data):
				# if password correct, redirect to their dashboard
				login_user(user, remember=form.remember.data)
				return redirect(url_for('dashboard')) # 要加单引号，否则跳转失败

		flash('用户名不存在或密码不正确')
		#return '<h1>用户名不存在或密码不正确</h1>'
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET','POST'])
def signup():
	form = RegisterForm()	# 注册表
	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256') # 密码哈希加密
		# 这里new user的数据是从form来的
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		try:
			db.session.add(new_user)
			db.session.commit()
			# 可以不用return，直接闪现一个成功的消息
			flash('注册成功')
			# return '<h1>新用户创建完毕！' + form.username.data + ' , 你好! Welcome</h1>' \
			# 		'<p>你的密码加密后为' + new_user.password +'</p>'
			# return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
		except Exception as e:
			#db.session.rollback()
			flash('该用户已存在') # and pop put a href to login
			#return redirect(url_for('login'))

	return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
def edit(event_id=None):
	form = EventForm()
	# 搜索结果的表单
	search_form = SearchForm()
	result = []
	# 查找出当前用户的所有日程，按起始时间排序
	all_event_list = Event.query.filter_by(author_name=current_user.username).order_by(Event.start_time).all()
	# for ev in all_event_list:
	# 	print(ev.title)
	# 	print(ev.type)
	# 	print(ev.start_time)

	if form.validate_on_submit():
		print("验证成功")
		new_event = Event(title=form.event_title.data,
						  url='http://127.0.0.1:5000/edit',
						  type=form.type.data,
						  start_time=form.start.data,
						  end_time=form.end.data,
						  author_name=current_user.username)
		print(new_event.title)
		print(new_event.type)
		print(new_event.start_time)  # '2020-03-22 12:11:00' 修改为datetime field之后就不需要解析字符串了			print(new_event.end_time)  # '2020-03-23 14:30:28'
		print(new_event.author_name)
		try:
			add(new_event)
			# add之后就有id
			new_id = new_event.id
			tmp_event = Event.query.filter_by(id=new_id).first()
			tmp_event.url = 'http://127.0.0.1:5000/edit/' + str(new_id)
			db.session.commit()  # 这样就算修改完成了？！好像是的
			return redirect(url_for('edit'))
		except Exception as e:  # 这里基本不太可能出现Exception了
			print(e)
			print("加入这个事件的时候出现了一些问题！")
			return '加入这个事件的时候出现了一些问题！'
	elif search_form.validate_on_submit():
		keyword = search_form.keyword.data
		sql_search = '%' + keyword + '%'
		result = Event.query.filter_by(author_name=current_user.username).filter(Event.title.ilike(sql_search)).order_by(Event.start_time).all()

		flash('搜索完毕。', 'info')
		print("搜索表是合法的！！搜索了" + sql_search + "下面输出搜索结果")
		print(result)
		for ev in result:
			print("下面展示查询结果")
			print(ev.id)
			print(ev.title)
			print(ev.type)
			print(ev.start_time)			# result是一个装有 <Event x> List
		return render_template('search_result.html', keyword=keyword, search=result, res_len=len(result))

	print("进入了edit函数即将返回list_and_edit html, 此时搜索结果为：")
	# 传参数，表格，当前用户，以及用户的所有事件
	return render_template('list_and_edit.html', form=form, search_form=search_form,
						   user=current_user, event_list=all_event_list, len=len(all_event_list),
						   search=result,res_len=len(result))

@app.route('/edit/<int:event_id>')
def descirbe(event_id):
	# 打算在这个页面进行"修改"功能
	print("此时传入了Event ID % i" % event_id)
	one_event = Event.query.filter_by(id=event_id).first()  # 只会有一个Event，返回一个class
	print("查找该Event成功: " + one_event.title)
	return render_template('one_event.html', event=one_event)

def add(new_event):
	# 所以这个方法必须登录了之后才可以使用
	db.session.add(new_event) # 现在加入日期还有问题
	db.session.commit()
	# 添加完之后应该跳转回edit页面，也就是全展示的页面
	#return redirect(url_for('edit'))

def delete(Event):
	db.delete(Event)

def check(event_name):
	# event name is a string
	tmp_e = db.session.query(Event).filter_by(title=event_name).first()
	check_list_event = db.session.query(Event).filter(Event.title.ilike(event_name)).all()



if __name__ == "__main__":
    app.run(debug=True)
