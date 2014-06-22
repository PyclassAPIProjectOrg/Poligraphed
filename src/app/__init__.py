# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import basedir
from flask.ext.mail import Mail

# create the application
# if os.environ.get("HEROKU") is None:
#      pass
# else:
#       print 'This app is on heroku'
#       app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

Bootstrap(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

mail = Mail(app)

from app import views, models
