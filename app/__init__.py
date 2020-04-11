import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, redirect, url_for
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_admin import Admin
from flask_mail import Mail
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_cors import CORS


app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
security = Security()
admin = Admin()
cors = CORS()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config_class)
    #app.url_map.default_subdomain = "www"

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    cors.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)


    from app.auth.models import User, Role

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app=app,
                      register_blueprint=False,
                      datastore=user_datastore)

    from app.admin import create_admin
    admin = create_admin(app, db)

    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/autumn.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Assignably startup')

    return app
