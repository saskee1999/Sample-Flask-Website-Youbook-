from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from config import Config
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['ENV']='development'
app.config['DEBUG']=True
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'put-your-password-here'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

from app import routes, models
