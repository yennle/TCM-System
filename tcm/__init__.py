from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY']='2bcc64794f0d49b05f097a8729e353dd'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tcm.db'

db=SQLAlchemy(app)
#import tcm.models
# migrate= Migrate(app,db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

bcrypt =Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from tcm import routes