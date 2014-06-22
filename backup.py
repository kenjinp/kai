 import os
  2 from flask import Flask
  3 from flask.ext.sqlalchemy import SQLAlchemy
  4 from flask.ext.login import LoginManager
  5 from flask.ext.mail import Mail
  6 from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME,
MAIL_PASSWORD
  7 #from flask.ext.babel import Babel
  8 
  9 
 10 app = Flask(__name__)
 11 app.config.from_object('config')
 12 db = SQLAlchemy(app)
 13 lm = LoginManager()
 14 lm.init_app(app)
 15 lm.login_view = 'login'
 16 mail = Mail(app)
 17 
 18 #error emails
 19 if not app.debug:
 20         import logging
 21         from logging.handlers import SMTPHandler
 22         if MAIL_USERNAME or MAIL_PASSWORD:
 23                 credentials = (MAIL_USERNAME, MAIL_PASSWORD)
 24         mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
 25                  'no-reply@' + MAIL_SERVER,
 26                  ADMINS,
 27                  'Silly Coffee Failure',
 28                  credentials)
 29         mail_handler.setLevel(logging.ERROR)
 30         app.logger.addHandler(mail_handler)
 31 
 32 #logging
 33 if not app.debug:
 34         import logging
 35         from logging.handlers import RotatingFileHandler
 36         file_handler = RotatingFileHandler('tmp/sillycoffee.log', 'a', 1 *
1024 * 1024, 10)
 37         file_handler.setFormatter(logging.Formatter('%(asctime)s
%(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
 38         app.logger.setLevel(logging.INFO)
 39         file_handler.setLevel(logging.INFO)
 40         app.logger.addHandler(file_handler)
 41         app.logger.info('silly coffee startup')
 42 
 43 #babel = Babel(app)
 44 from app import views, models
~                                   
