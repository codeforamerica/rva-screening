import os
from datetime import timedelta


class Config(object):
    DEBUG = True
    SECRET_KEY = 'some-secret'
    SCREENER_ENVIRONMENT = os.environ.get('SCREENER_ENVIRONMENT', 'dev')
    IS_PRODUCTION = os.environ.get('IS_PRODUCTION', False)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgres://@localhost/rva-screener')

    UPLOAD_FOLDER = 'var/uploads/documentimages'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_FILE_UPLOAD_DIR = 'uploads'
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'rva-screener')
    S3_ONLY_MODIFIED = False

    BABEL_DEFAULT_LOCALE = os.environ.get('BABEL_DEFAULT_LOCALE', 'en_US')
    BABEL_DEFAULT_TIMEZONE = os.environ.get('BABEL_DEFAULT_TIMEZONE', 'America/New_York')

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_EMAIL_SENDER = 'Quickscreen <richmond@codeforamerica.org>'
    SECURITY_POST_LOGIN_VIEW = '/'
    SECURITY_POST_LOGOUT_VIEW = '/login'
    SECURITY_UNAUTHORIZED_VIEW = '/403'
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = 'Quickscreen password reset instructions'
    SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = 'Your Quickscreen password has been reset'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Quickscreen <richmond@codeforamerica.org>'

    LARGE_DOCUMENT_IMAGE_SIZE = (900, 900)
    SMALL_DOCUMENT_IMAGE_SIZE = (100, 100)


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    MAIL_SUPPRESS_SEND = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost/screener_test'
    )
    MAIL_SUPPRESS_SEND = True
    SECURITY_PASSWORD_SALT = 'test'
