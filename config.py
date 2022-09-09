from app import app
from flaskext.mysql import MySQL

mysql = MySQL(app,prefix='mysql',user='root',password='mysql@123',host='localhost')
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql@123'
# # app.config['MYSQL_DATABASE_DB'] = 'production'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)