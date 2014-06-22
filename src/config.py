CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
DEBUG=True
import os
basedir = os.path.abspath(os.path.dirname(__file__))

#variables for ingestion by flask app
if os.environ.get("HEROKU") is None:
      SQLALCHEMY_DATABASE_URI = u'sqlite:///' + os.path.join(basedir, 'app.db')
      SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
      from apikey import _API_KEY
      API_KEY = _API_KEY
      print ' This app is on a local server'
else:
      app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
      # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","postgresql://pguser:password/dbname")
      API_KEY = str(os.environ.get("theapikey"))
      SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
class _DefaultSettings(object):
    USERNAME = 'world'
    SECRET_KEY = 'development key'
    DEBUG = True

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_SUBJECT_PREFIX = '[Poligraphed]'
MAIL_SENDER = 'Poligraphed poligraphed@gmail.com'


# administrator list
MAIL_ADMIN = os.environ.get('MAIL_ADMIN')
