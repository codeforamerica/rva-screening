import os
from datetime import timedelta


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') # Required for Flask sessions
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15) # Used for auto-logout
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgres://@localhost/rva-screener'
    )

    # File upload configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # Flask setting to limit request size
    SMALL_DOCUMENT_IMAGE_SIZE = (100, 100)
    LARGE_DOCUMENT_IMAGE_SIZE = (900, 900)

    # Configuration for assets stored in AWS
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # Flask-Babel configuration
    BABEL_DEFAULT_LOCALE = os.environ.get('BABEL_DEFAULT_LOCALE', 'en_US')
    BABEL_DEFAULT_TIMEZONE = os.environ.get('BABEL_DEFAULT_TIMEZONE', 'America/New_York')

    # Flask-Security configuration
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

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'Quickscreen <richmond@codeforamerica.org>'


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    MAIL_SUPPRESS_SEND = True


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL',
        'postgresql://localhost/screener_test'
    )
    MAIL_SUPPRESS_SEND = True
    SECURITY_PASSWORD_SALT = 'test'
