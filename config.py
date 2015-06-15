import os

class Config(object):
    SECRET_KEY = 'some-secret'
    SCREENER_ENVIRONMENT = os.environ.get('SCREENER_ENVIRONMENT', 'dev')
    IS_PRODUCTION = os.environ.get('IS_PRODUCTION', False)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql://root:password@localhost/rva_screening')

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

