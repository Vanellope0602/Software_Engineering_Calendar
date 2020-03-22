# Software_Engineering_Calendar
A calendar web app that can regulate events using python flask

## Tips for run it！
### Flask 插件
- 注意有一个版本不能装最新的，werkzeug==0.16.0
- 其余的插件直接`pip3 install` 即可
### 试用功能
- 点击月历上的事件链接可以进入详情页，但是这个功能刚刚做，所以之前database里的数据的URL都是指向一些奇怪的地方，不用在意，ID为25的日程是可以直接点进去的，账号是vanel，密码私戳我；
当然你最好注册一个新账号，可以添加新的日程，都可以实现点击跳转。
- 密码都是加密存储，忘了我也没办法
### database
- sqlite数据库文件路径应该为绝对路径

