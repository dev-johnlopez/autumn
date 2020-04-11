import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))


class Config(object):
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT') or 1
    SECURITY_USER_IDENTITY_ATTRIBUTES = ('email')
    SECURITY_REGISTERABLE = os.environ.get('SECURITY_REGISTERABLE') or True
    SECURITY_RECOVERABLE = os.environ.get('SECURITY_RECOVERABLE') or True
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_EMAIL_SENDER = os.environ.get('SECURITY_EMAIL_SENDER')
    SECURITY_FLASH_MESSAGES = os.environ.get('SECURITY_FLASH_MESSAGES')
    SECURITY_SEND_REGISTER_EMAIL = os.environ.get('SECURITY_SEND_REGISTER_EMAIL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG') or 0
    ADMINS = ['john@johnlopez.org']
    SECURITY_TRACKABLE = True
    SSL_DISABLE = False


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    WTF_CSRF_METHODS = []
