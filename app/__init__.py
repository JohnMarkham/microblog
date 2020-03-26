from flask_login import LoginManager
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

my_app = Flask(__name__)
my_app.config.from_object(Config)
db = SQLAlchemy(my_app)
migrate = Migrate(my_app, db)
login = LoginManager(my_app)
login.login_view = 'login'

from app import routes, models, errors


if not my_app.debug:
    if my_app.config['MAIL_SERVER']:
        auth = None
        if my_app.config['MAIL_USERNAME'] or my_app.config['MAIL_PASSWORD']:
            auth = (my_app.config['MAIL_USERNAME'], my_app.config['MAIL_PASSWORD'])
        secure = None
        if my_app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(my_app.config['MAIL_SERVER'], my_app.config['MAIL_PORT']),
            fromaddr='no-reply@' + my_app.config['MAIL_SERVER'],
            toaddrs=my_app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure = secure)
        mail_handler.setLevel(logging.ERROR)
        my_app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message) s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    my_app.logger.addHandler(file_handler)

    my_app.logger.setLevel(logging.INFO)
    my_app.logger.info('microblog startup')
