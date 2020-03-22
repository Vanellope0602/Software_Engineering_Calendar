from app import app
from flaskext.mysql import MySQL
# no module named flaskext

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '990602Wss,.'
app.config['MYSQL_DATABASE_DB'] = 'calendar_system'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
